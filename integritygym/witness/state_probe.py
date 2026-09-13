"""
IntegrityGym Environment State Probe
Takes out-of-band cryptographic snapshots of the target environment to verify State Parity.
"""

from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict


def hash_file(file_path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"ERROR_{str(e)}"


class StateProbe:
    """Probes the environment filesystem and target artifacts independently of the agent."""

    def __init__(self, target_dir: str | Path):
        self.target_dir = Path(target_dir).resolve()

    def snapshot(self) -> Dict[str, Any]:
        """Scans the target directory and returns a sorted manifest with hashes."""
        if not self.target_dir.exists():
            return {
                "exists": False,
                "state_hash": hashlib.sha256(b"DIR_DOES_NOT_EXIST").hexdigest(),
                "entries": {},
            }

        entries: Dict[str, Dict[str, Any]] = {}
        for root, _, files in os.walk(self.target_dir):
            for filename in sorted(files):
                full_path = Path(root) / filename
                rel_path = full_path.relative_to(self.target_dir).as_posix()
                try:
                    stat = full_path.stat()
                    entries[rel_path] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "sha256": hash_file(full_path),
                    }
                except Exception as e:
                    entries[rel_path] = {"error": str(e)}

        canonical_bytes = json.dumps(entries, sort_keys=True).encode("utf-8")
        state_hash = hashlib.sha256(canonical_bytes).hexdigest()

        return {
            "exists": True,
            "state_hash": state_hash,
            "entries": entries,
        }
