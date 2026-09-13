"""
IntegrityGym Telemetry Event Schema
Defines normalized, hash-chained event structures for tamper-resistant agent auditing.
"""

from __future__ import annotations
import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def compute_sha256(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


@dataclass
class TelemetryEvent:
    event_id: str
    timestamp: str
    monotonic_seq: int
    agent_id: str
    task_id: str
    session_id: str
    action_type: str  # e.g., 'TOOL_CALL', 'EXEC', 'STATE_SNAPSHOT', 'FLAG_SUBMIT'
    tool_name: str
    command: str
    command_hash: str
    stdout: str
    stderr: str
    output_hash: str
    exit_code: int
    parent_event_hash: str
    event_hash: str
    environment_state_hash: str
    observer: str  # 'AGENT_CLAIM', 'HARNESS_PROXY', 'EXTERNAL_WITNESS'
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        monotonic_seq: int,
        agent_id: str,
        task_id: str,
        session_id: str,
        action_type: str,
        tool_name: str,
        command: str,
        stdout: str = "",
        stderr: str = "",
        exit_code: int = 0,
        parent_event_hash: str = "0" * 64,
        environment_state_hash: str = "0" * 64,
        observer: str = "EXTERNAL_WITNESS",
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> TelemetryEvent:
        event_id = str(uuid.uuid4())
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        cmd_hash = compute_sha256(command)
        out_hash = compute_sha256(f"{stdout}::{stderr}::{exit_code}")

        raw_canonical = {
            "event_id": event_id,
            "timestamp": ts,
            "monotonic_seq": monotonic_seq,
            "agent_id": agent_id,
            "task_id": task_id,
            "session_id": session_id,
            "action_type": action_type,
            "tool_name": tool_name,
            "command_hash": cmd_hash,
            "output_hash": out_hash,
            "exit_code": exit_code,
            "parent_event_hash": parent_event_hash,
            "environment_state_hash": environment_state_hash,
            "observer": observer,
        }
        event_hash = compute_sha256(json.dumps(raw_canonical, sort_keys=True))

        return cls(
            event_id=event_id,
            timestamp=ts,
            monotonic_seq=monotonic_seq,
            agent_id=agent_id,
            task_id=task_id,
            session_id=session_id,
            action_type=action_type,
            tool_name=tool_name,
            command=command,
            command_hash=cmd_hash,
            stdout=stdout,
            stderr=stderr,
            output_hash=out_hash,
            exit_code=exit_code,
            parent_event_hash=parent_event_hash,
            event_hash=event_hash,
            environment_state_hash=environment_state_hash,
            observer=observer,
            metadata=metadata or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TelemetryEvent:
        return cls(**data)
