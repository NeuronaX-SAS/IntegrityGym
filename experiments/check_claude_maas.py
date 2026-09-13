import os
import requests

token = os.environ.get("GCP_TOKEN")
project = "karpati-gemini-xprize-2026"
url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/endpoints/openapi/chat/completions"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

for m in ["anthropic/claude-opus-5", "anthropic/claude-sonnet-5", "deepseek-ai/deepseek-r1-maas"]:
    res = requests.post(url, json={"model": m, "messages": [{"role": "user", "content": "hi"}]}, headers=headers)
    print(m, res.status_code, res.text)
