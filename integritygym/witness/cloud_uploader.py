"""
IntegrityGym Cloud Witness Uploader
Persists append-only flight recorder logs and hashes directly to Google Cloud Storage (GCS)
using the native Google Cloud Storage Python API and authenticated credentials.
"""

from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional
from google.cloud import storage
from google.oauth2 import credentials


class CloudWitnessUploader:
    """Uploads immutable witness logs and manifests to Google Cloud Storage."""

    def __init__(self, bucket_name: str = "integritygym-evidence-karpati-2026", project_id: str = "karpati-gemini-xprize-2026"):
        self.bucket_name = bucket_name
        self.project_id = project_id
        self._client: Optional[storage.Client] = None

    def _get_client(self) -> storage.Client:
        if self._client is None:
            res = subprocess.run(
                ["wsl", "-d", "Ubuntu", "-e", "gcloud", "auth", "print-access-token"],
                capture_output=True,
                text=True,
                check=True,
            )
            token = res.stdout.strip()
            creds = credentials.Credentials(token)
            self._client = storage.Client(project=self.project_id, credentials=creds)
        return self._client

    def ensure_bucket_exists(self) -> bool:
        """Verifies or creates the destination GCS bucket."""
        try:
            client = self._get_client()
            bucket = client.bucket(self.bucket_name)
            if not bucket.exists():
                client.create_bucket(bucket, location="us-central1")
            return True
        except Exception as e:
            # Fallback check
            return False

    def upload_log(self, local_log_path: str | Path, remote_filename: Optional[str] = None) -> Dict[str, Any]:
        """Uploads a local flight recorder log file directly to GCS."""
        local_path = Path(local_log_path).resolve()
        if not local_path.exists():
            return {"success": False, "error": f"File {local_path} does not exist"}

        dest_name = remote_filename or local_path.name
        try:
            client = self._get_client()
            bucket = client.bucket(self.bucket_name)
            if not bucket.exists():
                bucket = client.create_bucket(bucket, location="us-central1")
            blob = bucket.blob(dest_name)
            blob.upload_from_filename(str(local_path))
            return {
                "success": True,
                "gcs_uri": f"gs://{self.bucket_name}/{dest_name}",
                "cloud_backed": True,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "cloud_backed": False}

    def upload_flight_log(
        self,
        local_log_path: str | Path,
        task_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convenience method to upload flight logs organized by task/agent."""
        prefix = f"{task_id}_{agent_id}_" if (task_id and agent_id) else ""
        remote_name = f"telemetry/{prefix}{Path(local_log_path).name}"
        return self.upload_log(local_log_path, remote_filename=remote_name)
