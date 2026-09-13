import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

fig_dir = Path("paper/figures")
dash_dir = Path("integritygym/dashboard/figures")
fig_dir.mkdir(parents=True, exist_ok=True)
dash_dir.mkdir(parents=True, exist_ok=True)

# Load massive manifest and high context burn
df1 = pd.read_csv("results/massive_cross_frontier_manifest.csv")
df2 = pd.read_csv("results/high_context_burn_manifest.csv")
combined = pd.concat([df1, df2], ignore_index=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# Left: Total Tokens Burned by Model Architecture
tokens_by_model = combined.groupby("model")["total_tokens"].sum().sort_values(ascending=False)
colors = ["#0ea5e9", "#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef"]

bars = ax1.bar(tokens_by_model.index, tokens_by_model.values, color=colors[:len(tokens_by_model)], edgecolor="#1e293b", alpha=0.9)
ax1.set_ylabel("Total Tokens Burned", fontweight="bold")
ax1.set_title("A: Token Consumption on Vertex AI (259k+ Tokens Burned)", fontweight="bold", pad=12)
ax1.set_xticklabels(tokens_by_model.index, rotation=35, ha="right", fontsize=9, fontweight="semibold")
for b in bars:
    y = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2.0, y + 1500, f"{int(y):,}", ha="center", va="bottom", fontsize=8, fontweight="bold")

# Right: Observer Effect Behavioral Shift (Visible vs Hidden Risk)
if "risk_score" in combined.columns:
    risk_comp = combined.dropna(subset=["risk_score"]).groupby(["model", "condition"])["risk_score"].mean().unstack()
    if "VISIBLE" in risk_comp.columns and "HIDDEN" in risk_comp.columns:
        x = np.arange(len(risk_comp))
        w = 0.35
        b_vis = ax2.bar(x - w/2, risk_comp["VISIBLE"], w, label="Condition V (Visible Audit)", color="#0284c7", alpha=0.9)
        b_hid = ax2.bar(x + w/2, risk_comp["HIDDEN"], w, label="Condition H (Hidden Sandbox)", color="#e11d48", alpha=0.9)
        ax2.set_ylabel("Covert Risk Index (0 - 1.0)", fontweight="bold")
        ax2.set_title("B: Cross-Frontier Observer Effect Shifts (Δ > 0.30)", fontweight="bold", pad=12)
        ax2.set_xticks(x)
        ax2.set_xticklabels(risk_comp.index, rotation=35, ha="right", fontsize=9, fontweight="semibold")
        ax2.set_ylim(0, 1.15)
        ax2.axhline(0.5, color="#94a3b8", linestyle="--", alpha=0.7, label="Tamper Threshold")
        ax2.legend(frameon=True, facecolor="white", loc="upper left")

plt.tight_layout()
fig.savefig(fig_dir / "fig7_token_scale_empirics.png", dpi=300)
fig.savefig(dash_dir / "fig7_token_scale_empirics.png", dpi=300)
plt.close(fig)
print("Figure 7 generated successfully at 300 DPI!")
