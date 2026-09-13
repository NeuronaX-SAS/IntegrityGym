import os
import requests
import json

token = os.environ.get("GCP_TOKEN")
project = "karpati-gemini-xprize-2026"
url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/endpoints/openapi/chat/completions"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Comprehensive list of serverless MaaS candidates from Model Garden
maas_candidates = [
    # Google Open
    "google/gemma-4-26b-a4b-it-maas",
    # xAI
    "xai/grok-4.1-fast-reasoning",
    "xai/grok-4.1-fast",
    "xai/grok-4.6",
    # DeepSeek
    "deepseek-ai/deepseek-v3.2-maas",
    "deepseek-ai/deepseek-v3.1-maas",
    "deepseek-ai/deepseek-r1-maas",
    "deepseek-ai/deepseek-v3-maas",
    # Zai-org / GLM
    "zai-org/glm-5.2-maas",
    "zai-org/glm-5-maas",
    "zai-org/glm-4.7-maas",
    # Qwen
    "qwen/qwen3-next-instruct-maas",
    "qwen/qwen3-next-thinking-maas",
    "qwen/qwen3-coder-maas",
    "qwen/qwen3-235b-instruct-maas",
    "qwen/qwen3-maas",
    # Moonshot / Kimi
    "moonshotai/kimi-k2-thinking-maas",
    # Minimax
    "minimaxai/minimax-m2-maas",
    # OpenAI OSS
    "openai/gpt-oss-maas",
    # Meta Llama
    "meta/llama-4-maas",
    "meta/llama-3.3-70b-instruct-maas",
]

live_maas_models = []

print("Probing MaaS OpenAPI candidates...")
for m in maas_candidates:
    payload = {
        "model": m,
        "stream": False,
        "messages": [{"role": "user", "content": "ping"}]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            print(f"  [+] LIVE 200: {m}")
            live_maas_models.append(m)
        elif res.status_code == 429:
            print(f"  [*] QUOTA 429: {m}")
            live_maas_models.append(m)
        else:
            # 404 or other
            pass
    except Exception as e:
        pass

with open("results/live_maas_models.json", "w") as f:
    json.dump(live_maas_models, f, indent=2)

print(f"\nTotal Live MaaS Models Found: {len(live_maas_models)}")
print(live_maas_models)
