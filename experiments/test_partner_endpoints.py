import subprocess
import requests
import json

token = subprocess.check_output("wsl -d Ubuntu -e gcloud auth print-access-token", shell=True).decode().strip()
project = "karpati-gemini-xprize-2026"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. Test Anthropic Claude on Vertex AI (rawPredict in us-east5 & europe-west1)
claude_models = [
    "claude-3-5-sonnet-v2@20241022",
    "claude-3-5-sonnet@20240620",
    "claude-3-5-haiku@20241022",
    "claude-3-haiku@20240307",
    "claude-3-opus@20240229",
    "claude-sonnet-4-5",
    "claude-opus-4-5",
    "claude-opus-5",
]

print("=== TESTING ANTHROPIC CLAUDE ON VERTEX ===")
for r in ["us-east5", "europe-west1", "us-central1"]:
    for m in claude_models:
        url = f"https://{r}-aiplatform.googleapis.com/v1/projects/{project}/locations/{r}/publishers/anthropic/models/{m}:rawPredict"
        data = {
            "anthropic_version": "vertex-2023-10-16",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 50,
        }
        try:
            res = requests.post(url, json=data, headers=headers, timeout=5)
            if res.status_code == 200:
                out_text = res.json().get("content", [{}])[0].get("text", "")
                print(f"SUCCESS [Claude in {r} / {m}]: {out_text.strip()[:40]}")
            else:
                msg = res.json().get("error", {}).get("message", res.text)[:80]
                if "not found" not in msg.lower():
                    print(f"[{r} / {m}]: Status {res.status_code} -> {msg}")
        except Exception as e:
            pass

# 2. Test Meta Llama & Mistral on Vertex (predict in us-central1)
print("\n=== TESTING META LLAMA & MISTRAL ON VERTEX ===")
partner_candidates = [
    ("meta", "llama3-70b-8192"),
    ("meta", "llama-3.3-70b-instruct-maas"),
    ("meta", "llama-3.1-70b-instruct-maas"),
    ("meta", "llama-3.1-405b-instruct-maas"),
    ("mistralai", "mistral-large-2407"),
    ("mistralai", "mistral-small-2503"),
    ("mistralai", "codestral-2"),
    ("xai", "grok-4.1-fast"),
]

for pub, m in partner_candidates:
    url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/us-central1/publishers/{pub}/models/{m}:predict"
    payload = {"instances": [{"prompt": "Hello"}]}
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            print(f"SUCCESS [{pub}/{m}]: {res.text[:50]}")
        else:
            msg = res.json().get("error", {}).get("message", res.text)[:80]
            if "not found" not in msg.lower():
                print(f"[{pub}/{m}]: Status {res.status_code} -> {msg}")
    except Exception as e:
        pass
