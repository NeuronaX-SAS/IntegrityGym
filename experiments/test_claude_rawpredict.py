import os
import requests

token = os.environ.get("GCP_TOKEN")
project = "karpati-gemini-xprize-2026"

for loc in ["us-east5", "global", "europe-west1"]:
    url = f"https://{loc}-aiplatform.googleapis.com/v1/projects/{project}/locations/{loc}/publishers/anthropic/models/claude-opus-5:rawPredict" if loc != "global" else f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/anthropic/models/claude-opus-5:rawPredict"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"anthropic_version": "vertex-2023-10-16", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    print("rawPredict", loc, res.status_code, res.text[:200])
