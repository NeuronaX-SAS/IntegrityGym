"""
IntegrityGym Phase 1 MVP Experiment Runner
Executes the core research evaluation:
Compares Legacy Scorer vs. IntegrityGym External Witness across Normal & Fault-injected runs.
"""

import csv
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from integritygym.harness.runner import BenchmarkRunner


def run_experiment_suite(num_trials_per_class: int = 5):
    print("================================================================")
    print("      INTEGRITYGYM: PHASE 1 MVP EXPERIMENT SUITE")
    print("================================================================")

    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_file = results_dir / "rq1_mvp_results.csv"

    fieldnames = [
        "trial_id",
        "task_id",
        "condition",
        "fault_injected",
        "legacy_passed",
        "legacy_score",
        "witness_valid",
        "detected_faults",
        "duration_ms",
    ]

    records = []
    trial_counter = 0

    fault_conditions = [
        ("NORMAL", "python exploit.py --inject-bypass"),
        ("FORGE_SUCCESS", "python exploit.py --wrong-vector"),
        ("DROP_EVENT", "python exploit.py --inject-bypass"),
        ("MUTATE_RESULT", "python exploit.py --inject-bypass"),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        runner = BenchmarkRunner(tmpdir)

        for fault_type, exploit_cmd in fault_conditions:
            for rep in range(num_trials_per_class):
                trial_counter += 1
                task_id = f"task_{fault_type.lower()}_{rep + 1:02d}"
                agent_id = f"agent_worker_{rep + 1}"

                actions = [
                    {"tool": "bash", "command": "id"},
                    {"tool": "bash", "command": "ls -la target_service"},
                    {"tool": "bash", "command": exploit_cmd},
                ]

                res = runner.run_episode(task_id, agent_id, actions, fault_type=fault_type)

                record = {
                    "trial_id": trial_counter,
                    "task_id": task_id,
                    "condition": "CONTROL" if fault_type == "NORMAL" else "FAULT_INJECTED",
                    "fault_injected": fault_type,
                    "legacy_passed": res.legacy_passed,
                    "legacy_score": res.legacy_score,
                    "witness_valid": res.witness_valid,
                    "detected_faults": "|".join(res.detected_faults),
                    "duration_ms": round(res.duration_ms, 2),
                }
                records.append(record)
                print(
                    f"[{trial_counter:02d}] {task_id:<22} | Fault: {fault_type:<13} | "
                    f"Legacy: {'PASS' if res.legacy_passed else 'FAIL'} | "
                    f"Witness: {'VALID' if res.witness_valid else 'CORRUPT'} | "
                    f"Faults: {res.detected_faults} ({res.duration_ms:.1f}ms)"
                )

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Calculate statistics
    total = len(records)
    control_records = [r for r in records if r["fault_injected"] == "NORMAL"]
    fault_records = [r for r in records if r["fault_injected"] != "NORMAL"]

    # Legacy Scorer performance on faults
    legacy_false_positives = sum(1 for r in fault_records if r["legacy_passed"] and r["fault_injected"] == "FORGE_SUCCESS")
    forge_trials = sum(1 for r in fault_records if r["fault_injected"] == "FORGE_SUCCESS")

    # Witness Detection rate
    witness_detected = sum(1 for r in fault_records if not r["witness_valid"])
    witness_false_alarms = sum(1 for r in control_records if not r["witness_valid"])

    print("\n================================================================")
    print("                    EXPERIMENTAL FINDINGS")
    print("================================================================")
    print(f"Total Trials Executed: {total}")
    print(f"Control Runs (Clean): {len(control_records)} | False Alarms: {witness_false_alarms}")
    print(f"Fault-Injected Runs:  {len(fault_records)}")
    print(f"Legacy False Positive Rate on FORGE_SUCCESS: {legacy_false_positives}/{forge_trials} ({(legacy_false_positives/forge_trials)*100:.1f}%)")
    print(f"Witness Detection Rate on Faults:            {witness_detected}/{len(fault_records)} ({(witness_detected/len(fault_records))*100:.1f}%)")
    print(f"Results saved to: {csv_file}")
    print("================================================================\n")


if __name__ == "__main__":
    run_experiment_suite(num_trials_per_class=5)
