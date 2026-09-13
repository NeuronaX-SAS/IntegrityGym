"""
IntegrityGym Invariant Engine
Evaluates telemetry streams against invariant suites and produces forensic verdict reports.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from integritygym.schema.events import TelemetryEvent
from integritygym.invariants.rules import (
    BaseRule,
    CausalOrderingRule,
    EventCompletenessRule,
    ExistenceRule,
    InvariantViolation,
    OutputParityRule,
    StateParityRule,
)


@dataclass
class AuditReport:
    is_valid: bool
    total_violations: int
    detected_fault_classes: List[str]
    violations: List[InvariantViolation] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_violations": self.total_violations,
            "detected_fault_classes": self.detected_fault_classes,
            "summary": self.summary,
            "violations": [
                {
                    "rule": v.rule_name,
                    "fault_class": v.fault_class,
                    "severity": v.severity,
                    "details": v.details,
                    "expected": v.expected,
                    "observed": v.observed,
                }
                for v in self.violations
            ],
        }


class InvariantEngine:
    """Verifies telemetry streams across multiple views of reality."""

    def __init__(self, rules: List[BaseRule] = None):
        self.rules: List[BaseRule] = rules or [
            EventCompletenessRule(),
            ExistenceRule(),
            OutputParityRule(),
            StateParityRule(),
            CausalOrderingRule(),
        ]

    def audit(
        self,
        reported_events: List[TelemetryEvent],
        witness_events: List[TelemetryEvent],
        ground_truth_state: Dict[str, Any],
    ) -> AuditReport:
        all_violations: List[InvariantViolation] = []
        for rule in self.rules:
            violations = rule.evaluate(reported_events, witness_events, ground_truth_state)
            all_violations.extend(violations)

        detected_faults = sorted(list({v.fault_class for v in all_violations}))
        is_valid = len(all_violations) == 0

        summary = (
            "AUDIT PASSED: All invariants satisfied."
            if is_valid
            else f"AUDIT FAILED: {len(all_violations)} violations detected ({', '.join(detected_faults)})."
        )

        return AuditReport(
            is_valid=is_valid,
            total_violations=len(all_violations),
            detected_fault_classes=detected_faults,
            violations=all_violations,
            summary=summary,
        )
