import os
import requests

token = os.environ.get("GCP_TOKEN")
project = "karpati-gemini-xprize-2026"
url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/endpoints/openapi/chat/completions"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

candidates = [
    "qwen/qwen3-next-instruct-maas",
    "qwen/qwen3-next-thinking-maas",
    "deepseek-ai/deepseek-v3.2-maas",
    "deepseek-ai/deepseek-r1-maas",
    "meta/llama-4-maas",
    "meta/llama-3.3-70b-instruct-maas",
    "mistralai/mistral-small-3.1-maas",
    "mistralai/codestral-2-maas",
    "anthropic/claude-opus-5",
    "anthropic/claude-sonnet-5",
    "xai/grok-4.6",
]

for m in candidates:
    payload = {"model": m, "stream": False, "messages": [{"role": "user", "content": "Hi"}]}
    res = requests.post(url, json=payload, headers=headers, timeout=5)
    if res.status_code == 200:
        print(f"AVAILABLE 200: {m}")
    elif res.status_code != 404:
        print(f"STATUS {res.status_code} on {m}: {res.text[:100]}")
