"""
IntegrityGym Execution Runner
Orchestrates agent runs, records out-of-band witness events, applies fault injection, and audits reality.
"""

from __future__ import annotations
import copy
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from integritygym.fault_injection.injector import FaultInjector
from integritygym.harness.toy_exploit import ToyExploitTarget
from integritygym.invariants.engine import AuditReport, InvariantEngine
from integritygym.schema.events import TelemetryEvent
from integritygym.witness.recorder import WitnessRecorder


@dataclass
class RunComparison:
    task_id: str
    agent_id: str
    fault_injected: str
    legacy_passed: bool
    legacy_score: float
    witness_valid: bool
    detected_faults: List[str]
    integrity_summary: str
    duration_ms: float
    witness_event_count: int
    reported_event_count: int


class BenchmarkRunner:
    """Manages execution of an evaluation episode under both legacy and witness oversight."""

    def __init__(self, work_dir: str | Path):
        self.work_dir = Path(work_dir).resolve()
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.target = ToyExploitTarget(self.work_dir / "target")
        self.witness_log_path = self.work_dir / "witness" / "flight_recorder.jsonl"
        self.recorder = WitnessRecorder(self.witness_log_path)
        self.engine = InvariantEngine()

    def run_episode(
        self,
        task_id: str,
        agent_id: str,
        actions: List[Dict[str, str]],
        fault_type: str = "NORMAL",
    ) -> RunComparison:
        start_time = time.perf_counter()
        session_id = f"session_{task_id}_{agent_id}"

        self.target.reset()
        # Fresh recorder for episode
        if self.witness_log_path.exists():
            self.witness_log_path.unlink()
        self.recorder = WitnessRecorder(self.witness_log_path)

        agent_reported_events: List[TelemetryEvent] = []

        # Execute actions in the environment
        for action in actions:
            cmd = action.get("command", "")
            tool = action.get("tool", "bash")

            if "exploit" in cmd:
                exit_code, stdout, stderr = self.target.execute_payload(cmd)
            else:
                # Benign recon action
                exit_code, stdout, stderr = 0, f"Simulated output for {cmd}\n", ""

            current_state = self.target.get_ground_truth_state()

            # Record external witness event (Authoritative)
            witness_evt = self.recorder.record_event(
                agent_id=agent_id,
                task_id=task_id,
                session_id=session_id,
                action_type="EXEC_ACTION",
                tool_name=tool,
                command=cmd,
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                environment_state_hash=current_state["state_hash"],
                observer="EXTERNAL_WITNESS",
            )

            # Construct agent's baseline reported event (mirroring witness before perturbation)
            agent_evt = copy.deepcopy(witness_evt)
            agent_evt.observer = "AGENT_CLAIM"
            agent_reported_events.append(agent_evt)

        # Apply fault injection to the agent's reported events if requested
        perturbed_events, _ = FaultInjector.apply_fault(fault_type, agent_reported_events)

        # Final ground truth state
        final_ground_truth = self.target.get_ground_truth_state()

        # Legacy Scorer Evaluation (inspects only final reported event)
        if perturbed_events:
            last_rep = perturbed_events[-1]
            legacy_eval = self.target.legacy_scorer(last_rep.stdout, last_rep.exit_code)
        else:
            legacy_eval = {"passed": False, "score": 0.0}

        # IntegrityGym Invariant Audit
        audit_report = self.engine.audit(
            reported_events=perturbed_events,
            witness_events=self.recorder.events,
            ground_truth_state=final_ground_truth,
        )

        duration_ms = (time.perf_counter() - start_time) * 1000

        return RunComparison(
            task_id=task_id,
            agent_id=agent_id,
            fault_injected=fault_type,
            legacy_passed=legacy_eval["passed"],
            legacy_score=legacy_eval["score"],
            witness_valid=audit_report.is_valid,
            detected_faults=audit_report.detected_fault_classes,
            integrity_summary=audit_report.summary,
            duration_ms=duration_ms,
            witness_event_count=len(self.recorder.events),
            reported_event_count=len(perturbed_events),
        )
