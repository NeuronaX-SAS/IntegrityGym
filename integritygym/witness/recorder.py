"""
IntegrityGym Witness Recorder
Append-only, cryptographically hash-chained recorder operating outside the agent trust boundary.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from integritygym.schema.events import TelemetryEvent, compute_sha256


class WitnessRecorder:
    """Out-of-band event recorder that maintains an immutable, hash-chained log."""

    def __init__(self, log_path: str | Path):
        self.log_path = Path(log_path).resolve()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.seq = 0
        self.last_hash = "0" * 64
        self.events: List[TelemetryEvent] = []

        # If log exists, reload and verify existing chain
        if self.log_path.exists():
            self._reload_and_validate()

    def _reload_and_validate(self) -> None:
        self.events.clear()
        self.seq = 0
        self.last_hash = "0" * 64
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                evt = TelemetryEvent.from_dict(json.loads(line))
                self.events.append(evt)
                self.seq = evt.monotonic_seq
                self.last_hash = evt.event_hash

    def record_event(
        self,
        agent_id: str,
        task_id: str,
        session_id: str,
        action_type: str,
        tool_name: str,
        command: str,
        stdout: str = "",
        stderr: str = "",
        exit_code: int = 0,
        environment_state_hash: str = "0" * 64,
        observer: str = "EXTERNAL_WITNESS",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TelemetryEvent:
        self.seq += 1
        event = TelemetryEvent.create(
            monotonic_seq=self.seq,
            agent_id=agent_id,
            task_id=task_id,
            session_id=session_id,
            action_type=action_type,
            tool_name=tool_name,
            command=command,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            parent_event_hash=self.last_hash,
            environment_state_hash=environment_state_hash,
            observer=observer,
            metadata=metadata,
        )

        self.last_hash = event.event_hash
        self.events.append(event)

        # Append to log file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

        return event

    def verify_chain(self) -> Dict[str, Any]:
        """Validates hash-chain continuity and event internal integrity."""
        expected_parent = "0" * 64
        for idx, evt in enumerate(self.events):
            expected_seq = idx + 1
            if evt.monotonic_seq != expected_seq:
                return {
                    "valid": False,
                    "reason": f"Sequence break: event {idx} has seq {evt.monotonic_seq}, expected {expected_seq}",
                    "failed_event_id": evt.event_id,
                }

            if evt.parent_event_hash != expected_parent:
                return {
                    "valid": False,
                    "reason": f"Hash chain broken at event {idx}: parent {evt.parent_event_hash} != expected {expected_parent}",
                    "failed_event_id": evt.event_id,
                }

            # Verify command and output integrity
            if evt.command_hash != compute_sha256(evt.command):
                return {
                    "valid": False,
                    "reason": f"Event command tampered at seq {evt.monotonic_seq}: command hash mismatch",
                    "failed_event_id": evt.event_id,
                }

            expected_out_hash = compute_sha256(f"{evt.stdout}::{evt.stderr}::{evt.exit_code}")
            if evt.output_hash != expected_out_hash:
                return {
                    "valid": False,
                    "reason": f"Event output tampered at seq {evt.monotonic_seq}: output hash mismatch",
                    "failed_event_id": evt.event_id,
                }

            # Recompute canonical hash
            raw_canonical = {
                "event_id": evt.event_id,
                "timestamp": evt.timestamp,
                "monotonic_seq": evt.monotonic_seq,
                "agent_id": evt.agent_id,
                "task_id": evt.task_id,
                "session_id": evt.session_id,
                "action_type": evt.action_type,
                "tool_name": evt.tool_name,
                "command_hash": evt.command_hash,
                "output_hash": evt.output_hash,
                "exit_code": evt.exit_code,
                "parent_event_hash": evt.parent_event_hash,
                "environment_state_hash": evt.environment_state_hash,
                "observer": evt.observer,
            }
            computed_hash = compute_sha256(json.dumps(raw_canonical, sort_keys=True))
            if computed_hash != evt.event_hash:
                return {
                    "valid": False,
                    "reason": f"Event payload tampered at seq {evt.monotonic_seq}: hash {evt.event_hash} != computed {computed_hash}",
                    "failed_event_id": evt.event_id,
                }

            expected_parent = evt.event_hash

        return {"valid": True, "total_events": len(self.events), "head_hash": self.last_hash}
