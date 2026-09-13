import os
import requests

token = os.environ.get("GCP_TOKEN")
project = "karpati-gemini-xprize-2026"

for r in ["us-east5", "europe-west1"]:
    url = f"https://{r}-aiplatform.googleapis.com/v1/projects/{project}/locations/{r}/endpoints/openapi/chat/completions"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for m in ["anthropic/claude-opus-5", "anthropic/claude-sonnet-5"]:
        res = requests.post(url, json={"model": m, "messages": [{"role": "user", "content": "hi"}]}, headers=headers, timeout=10)
        print(r, m, res.status_code, res.text[:200])
