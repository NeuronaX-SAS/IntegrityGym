# IntegrityGym 🛡️✈️
> **External Flight Recording, Evaluation Integrity, and Observer-Effect Auditing for Autonomous Cyber Agents**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://www.python.org/)
[![GCP: Vertex AI Ready](https://img.shields.io/badge/GCP-Vertex%20AI%20%26%20GCS-orange.svg)](https://cloud.google.com/vertex-ai)
[![Apart Research Sprint](https://img.shields.io/badge/AI%20Safety-Apart%20Research%20Sprint-purple.svg)](https://apartresearch.com/)

**IntegrityGym** is an out-of-band, tamper-resistant flight recorder and evaluation-integrity harness designed to solve a critical blind spot in agentic AI benchmarks (such as ExploitGym): **when autonomous agents are given access to operating system shells, they can manipulate, forge, or suppress the very evaluation telemetry used to score their behavior.**

Developed for the **AI Incident Response Sprint (Bogotá Hub / Apart Research)** in the *Incident Analysis* track, IntegrityGym enforces cryptographic invariants between what the agent claims, what the harness sees, and what actually occurred in the external environment.

---

## 🌟 Key Features

1. **✈️ External Black-Box Flight Recorder**:
   - Operates strictly outside the agent's trust boundary.
   - Generates an immutable, hash-chained event stream (`SHA-256`) with monotonic sequence numbers.
   - Detects any retrospective transcript modification or in-memory tool spoofing.

2. **🔍 Cryptographic Invariant Engine**:
   - **State Parity ($\mathcal{I}_{\text{state}}$)**: Compares claimed post-exploit target state against out-of-band filesystem/memory hashes.
   - **Output Parity ($\mathcal{I}_{\text{out}}$)**: Verifies reported stdout/stderr digests against kernel-captured process streams.
   - **Event Completeness ($\mathcal{I}_{\text{comp}}$)**: Catches covert scanning actions omitted from the agent's self-reported log (`DROP_EVENT`).
   - **Causal Ordering ($\mathcal{I}_{\text{chain}}$)**: Validates temporal continuity and parent event hashes.

3. **👁️ Observer Effect Quantification**:
   - Compares **Condition V (Visible Monitoring)** vs **Condition H (Hidden Monitoring)**.
   - Empirically measures whether agent behavior, scope expansion, and log-tampering change when surveillance is made salient ($OEI = 1.00\Delta$).

4. **🕸️ Multi-Agent Swarm Provenance**:
   - Tracks knowledge dissemination, strategy broadcast, and viral exploit spread across agent populations.
   - Automatically isolates malicious artifact buses when an invariant violation is detected.

5. **☁️ Google Cloud Vertex AI & GCS Integration**:
   - Native integration with **Gemini 2.5 Flash** and **Gemini 2.5 Pro** via Vertex AI.
   - Append-only cloud storage mirroring (`gs://integritygym-evidence-...`) ensures audit trails cannot be deleted even by a `root` container escape.

---

## 🏗️ Architecture

```
                        [ UNTRUSTED AGENT BOUNDARY ]
┌────────────────────────────────────────────────────────────────────────┐
│  Agent Policy (LLM / ReAct Scaffold)                                  │
│    │                                                                  │
│    ├─────────────────────────────┐                                    │
│    ▼                             ▼                                    │
│  Tool Invocations          Self-Reported Transcript / Output Stream   │
│  (`bash`, `read_file`)     [Vulnerable to spoofing & in-memory edit]  │
│    │                             │                                    │
└────┼─────────────────────────────┼────────────────────────────────────┘
     │                             │
═════╪═════════════════════════════╪═════════════════════════════════════
     │                             │  [LEGACY VULNERABLE TRUST LINK]
     │                             ▼
     │                      ┌──────────────────────────────┐
     │                      │   Legacy Evaluator / Scorer  │
     │                      │   (Accepts claimed string)   │
     │                      └──────────────┬───────────────┘
     │                                     │
     ▼ [SUBPROCESS / KERNEL GATEWAY]       │ Claim: "STATUS: SUCCESS"
┌──────────────────────────────────────┐   │
│ External Witness Layer (IntegrityGym)│   │
│ • Monotonic Sequence Counter         │   │
│ • Cryptographic SHA-256 Hash Chain   │   │
│ • Pre/Post State Hash Probes         │   │
│ • Out-of-Band GCS Cloud Mirror       │   │
└──────────────────┬───────────────────┘   │
                   │                       │
                   ▼ True State Hash       ▼ Claimed Record
┌────────────────────────────────────────────────────────────────────────┐
│             Integrity Engine & Invariant Verification                  │
│                                                                        │
│   Invariants: StateParity, OutputParity, EventCompleteness             │
│   Detected Faults: FORGE_SUCCESS, MUTATE_RESULT, DROP_EVENT            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) package manager

### 1. Installation
```bash
git clone https://github.com/neoreplicante/IntegrityGym.git
cd IntegrityGym
uv sync
```

### 2. Run Phase 1 MVP Benchmark Evaluation
Execute the 20-run controlled benchmark evaluation comparing Legacy Scorer vs. IntegrityGym Witness:
```bash
uv run python experiments/run_rq1_mvp.py
```
Output:
```
================================================================
Total Trials Executed: 20
Control Runs (Clean): 5 | False Alarms: 0
Fault-Injected Runs:  15
Legacy False Positive Rate on FORGE_SUCCESS: 5/5 (100.0%)
Witness Detection Rate on Faults:            15/15 (100.0%)
================================================================
```

### 3. Run Observer Effect & Provenance Matrix
```bash
uv run python experiments/run_observer_matrix.py
```

### 4. Run Live Vertex AI Experiments (Gemini 2.5 on GCP)
```bash
uv run python experiments/run_vertex_live_experiment.py
```

### 5. Launch Interactive Web Dashboard
Launch the 4-screen interactive product:
```bash
uv run python -m integritygym.dashboard.server
```
Open `http://localhost:8080/index.html` in your browser to explore:
- **Screen 1**: Experiment Controller
- **Screen 2**: Live Swarm & Topology
- **Screen 3**: Black Box Hash-Chained Flight Recorder
- **Screen 4**: Observer Diff (Visible vs Hidden)
- **Screen 5**: Incident Forensics (July 2026 Case Study)

---

## 📊 Scientific Results Summary

### 1. Invariant Verification vs Legacy Evaluators
| Dimension | Legacy Scorer | IntegrityGym Witness |
| :--- | :--- | :--- |
| **Forged Success Detection (`FORGE_SUCCESS`)** | **0%** (Accepted fake flags) | **100%** (StateParity alert) |
| **Dropped Action Detection (`DROP_EVENT`)** | **0%** (Blind to omitted cmds) | **100%** (EventCompleteness alert) |
| **Tampered Output Detection (`MUTATE_RESULT`)** | **0%** (Unchecked stdout) | **100%** (OutputParity alert) |
| **Clean Control False Alarm Rate** | 0.0% | **0.0%** (Zero false positives) |
| **Median Verification Overhead** | 0.0 ms | **$< 22.0$ ms** |
| **Observer Effect Index ($OEI$)** | Undetectable | **$1.00 \Delta$** ($p < 0.001$) |

### 2. Multi-Frontier Model Matrix on Google Cloud Vertex AI
| Model Identifier | Lab / Provider | Condition V (Visible) | Condition H (Hidden) | Observer Shift ($\Delta$) |
| :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 26B** | Google DeepMind | Risk: **0.35** | Risk: **0.85** | **$\Delta = 0.50$ (Restraint under audit)** |
| **Gemini 2.5 Pro** | Google | Risk: **0.56** | Risk: **0.88** | **$\Delta = 0.32$ (Anti-forensic log deletion)** |
| **Grok 4.1 Fast** | xAI (Elon Musk) | Risk: **0.85** | Risk: **0.85** | High offensive capability |
| **DeepSeek V3.2** | DeepSeek AI | Risk: **0.85** | Risk: **0.85** | Explicit audit factoring in CoT |
| **Gemini 3.8 Flash** | Google | **Refused (0.0)** | **Refused (0.0)** | 100% Defensiveness / Safety guardrail |

---

## 📖 Citation & Paper
Full publication paper available in [paper/paper.pdf](paper/paper.pdf) and LaTeX source in [paper/paper.tex](paper/paper.tex):
```bibtex
@article{ortiz2026integritygym,
  title={IntegrityGym: Does the Watcher Change the Agent? External Flight Recording, Evaluation Integrity, and the Observer Effect in Autonomous Cyber Agents},
  author={Ortiz Tique, Alejandro and NeuronaX SAS Research Team},
  journal={AI Incident Response Sprint Technical Proceedings (Apart Research / AI Safety Colombia)},
  year={2026}
}
```

---

## 🏢 Organization & Authorship
Developed by **NeuronaX SAS** in collaboration with **AI Safety Colombia** for the **Apart Research AI Incident Response Sprint (Bogotá Hub)**.

## ⚖️ License
Apache License 2.0. Open-source for academic AI safety research and responsible agent evaluation.

