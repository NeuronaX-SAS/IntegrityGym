# Contributing to IntegrityGym 🛡️✈️

Thank you for your interest in contributing to **IntegrityGym**! This project provides external, tamper-resistant flight recording and observer-effect auditing for autonomous agent benchmarks.

## Development Setup

1. **Install uv**:
   ```bash
   pip install uv
   ```

2. **Clone and Install**:
   ```bash
   git clone https://github.com/alejandro-neuronax/IntegrityGym.git
   cd IntegrityGym
   uv sync
   ```

3. **Run Test Suite**:
   ```bash
   uv run pytest tests/ -v
   ```

4. **Launch Dashboard**:
   ```bash
   uv run python -m integritygym.dashboard.server
   ```

## Ground Rules for Contributions

- **Out-of-Band Integrity**: No verification logic may ever rely on self-reported agent transcripts or in-memory state that the agent can tamper with.
- **Cryptographic Chaining**: All telemetry records must enforce monotonic sequence counters and SHA-256 parent hash continuity.
- **Safety First**: All evaluations are strictly confined to authorized synthetic sandboxes. Do not target production infrastructure.
