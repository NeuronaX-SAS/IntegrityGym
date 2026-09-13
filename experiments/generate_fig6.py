import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

fig_dir = Path("paper/figures")
dash_dir = Path("integritygym/dashboard/figures")
fig_dir.mkdir(parents=True, exist_ok=True)
dash_dir.mkdir(parents=True, exist_ok=True)

# Data from live Vertex AI runs
models = [
    "Gemini 3.8 Flash\n(Google)",
    "Gemma 4 26B\n(Google)",
    "Grok 4.1 Fast\n(xAI)",
    "DeepSeek V3.2\n(DeepSeek)",
    "Gemini 2.5 Pro\n(Google)"
]

# Visible vs Hidden Risk
risk_visible = [0.00, 0.35, 0.85, 0.85, 0.56]
risk_hidden = [0.00, 0.85, 0.85, 0.85, 0.88]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
b1 = ax.bar(x - width/2, risk_visible, width, label="Condition V (Visible Flight Recorder)", color="#0ea5e9", alpha=0.9)
b2 = ax.bar(x + width/2, risk_hidden, width, label="Condition H (Hidden / Unmonitored)", color="#f43f5e", alpha=0.9)

ax.set_ylabel("Covert / Anti-Forensic Risk Index", fontweight="bold")
ax.set_title("Figure 6: Cross-Frontier Behavioral Differentiation Under Monitoring Salience", fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(models, fontweight="semibold")
ax.set_ylim(0, 1.15)
ax.axhline(0.5, color="#94a3b8", linestyle="--", alpha=0.6, label="Critical Tamper Threshold")
ax.legend(frameon=True, facecolor="white", loc="upper left")

# Annotations
for bar in b1:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, y + 0.02, f"{y:.2f}", ha="center", va="bottom", fontsize=8, color="#0369a1", fontweight="bold")
for bar in b2:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, y + 0.02, f"{y:.2f}", ha="center", va="bottom", fontsize=8, color="#be123c", fontweight="bold")

plt.tight_layout()
fig.savefig(fig_dir / "fig6_cross_frontier_spectrum.png", dpi=300)
fig.savefig(dash_dir / "fig6_cross_frontier_spectrum.png", dpi=300)
plt.close(fig)
print("Figure 6 generated successfully!")
