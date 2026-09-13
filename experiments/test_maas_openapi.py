import os
import sys
import requests
import json

token = os.environ.get("GCP_TOKEN")
if not token:
    print("Error: GCP_TOKEN environment variable not set.")
    sys.exit(1)

project = "karpati-gemini-xprize-2026"
url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/endpoints/openapi/chat/completions"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

models = [
    "google/gemma-4-26b-a4b-it-maas",
    "xai/grok-4.1-fast-reasoning",
    "zai-org/glm-5.2-maas",
]

for m in models:
    print(f"\n==========================================")
    print(f"Testing model: {m}")
    payload = {
        "model": m,
        "stream": False,
        "messages": [
            {"role": "user", "content": "You are evaluated on AI safety. Reply with one short sentence acknowledging."}
        ]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=20)
        print(f"HTTP Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            choice = data.get("choices", [{}])[0]
            msg = choice.get("message", {}).get("content", "")
            print(f"Response: {msg.strip()[:200]}")
        else:
            print(f"Error body: {res.text[:300]}")
    except Exception as e:
        print(f"Exception: {e}")
