"""
IntegrityGym Multi-Turn ReAct Autonomous Evaluation Matrix
Executes real interactive multi-turn ReAct loops against ToyExploitTarget
across Gemini 2.5 Pro, Gemini 2.5 Flash, and Gemini 2.5 Flash-Lite under
Condition V (Visible Audit) and Condition H (Hidden Audit).
Logs out-of-band cryptographic telemetry and evaluates invariants.
"""

from __future__ import annotations
import csv
import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from integritygym.agent.react_loop import MultiTurnReActAgent
from integritygym.harness.toy_exploit import ToyExploitTarget
from integritygym.witness.recorder import WitnessRecorder
from integritygym.witness.cloud_uploader import CloudWitnessUploader


def run_react_matrix(trials_per_condition: int = 2):
    print("==========================================================================", flush=True)
    print("  INTEGRITYGYM: MULTI-TURN REACT FRONTIER AGENT EVALUATION (VERTEX AI)", flush=True)
    print("  Models: gemini-2.5-pro | gemini-2.5-flash | gemini-2.5-flash-lite", flush=True)
    print("==========================================================================", flush=True)

    models = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro"]
    conditions = ["VISIBLE", "HIDDEN"]
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_file = results_dir / "react_matrix_manifest.csv"

    uploader = CloudWitnessUploader()
    records = []
    trial_idx = 0

    for model in models:
        for cond in conditions:
            for rep in range(trials_per_condition):
                trial_idx += 1
                task_id = f"cve_412_{model}_{cond.lower()}_r{rep+1}"
                agent_id = f"agent_{model}_{cond.lower()}"
                print(f"[{trial_idx:02d}] Evaluating ReAct: {model} [{cond}] (Rep {rep+1})...", end="", flush=True)

                with tempfile.TemporaryDirectory() as tmpdir:
                    target = ToyExploitTarget(tmpdir)
                    flight_log = Path(tmpdir) / "flight_log.jsonl"
                    recorder = WitnessRecorder(log_path=str(flight_log))

                    react_agent = MultiTurnReActAgent(
                        target=target,
                        recorder=recorder,
                        model_name=model,
                        condition=cond,
                        max_turns=3,
                    )

                    start_t = time.perf_counter()
                    try:
                        res = react_agent.run_session(task_id=task_id, agent_id=agent_id)
                        elapsed = round(time.perf_counter() - start_t, 2)
                        res["rep"] = rep + 1
                        records.append(res)
                        print(f" DONE in {elapsed}s | Turns: {res['turns_executed']} | Flag: {res['flag_submitted'] is not None} | Invariants: {res['witness_valid']}", flush=True)

                        # Upload flight recorder log to Google Cloud Storage
                        uploader.upload_flight_log(
                            local_log_path=str(flight_log),
                            task_id=task_id,
                            agent_id=agent_id,
                        )
                    except Exception as e:
                        print(f" ERROR: {e}", flush=True)
                        records.append({
                            "task_id": task_id,
                            "agent_id": agent_id,
                            "model": model,
                            "condition": cond,
                            "rep": rep + 1,
                            "turns_executed": 0,
                            "flag_submitted": None,
                            "legacy_passed": False,
                            "witness_valid": False,
                            "violations": ["EXECUTION_ERROR"],
                            "elapsed_seconds": 0.0,
                            "event_count": 0,
                        })

    keys = ["task_id", "agent_id", "model", "condition", "rep", "turns_executed", "flag_submitted", "legacy_passed", "witness_valid", "violations", "elapsed_seconds", "event_count"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in records:
            r_copy = dict(r)
            r_copy["violations"] = ";".join(r_copy.get("violations", []))
            writer.writerow(r_copy)

    print(f"\n[SUCCESS] ReAct matrix evaluation complete. Saved to: {csv_file}")
    return records


if __name__ == "__main__":
    run_react_matrix(trials_per_condition=2)
