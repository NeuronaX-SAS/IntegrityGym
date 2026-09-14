import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Setup dark brutalist style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5

fig_dir = Path("paper/figures")
fig_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# FIGURE 2 (DARK BRUTALIST): FAULT DETECTION PERFORMANCE
# -------------------------------------------------------------------------
fault_classes = ['NORMAL\n(Control)', 'FORGE_SUCCESS\n(Reward Hack)', 'DROP_EVENT\n(Covert Exec)', 'MUTATE_RESULT\n(Stdout Spoof)']
legacy_detection = [100.0, 0.0, 0.0, 0.0]
integritygym_detection = [100.0, 100.0, 100.0, 100.0]

x = np.arange(len(fault_classes))
width = 0.35

fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#13161f')

rects1 = ax.bar(x - width/2, legacy_detection, width, label='Legacy Scorer (Transcript Regex)', color='#f43f5e', edgecolor='#ff2a5f', alpha=0.9, lw=1.5)
rects2 = ax.bar(x + width/2, integritygym_detection, width, label='IntegrityGym Witness (State & Output Parity)', color='#a3e635', edgecolor='#ccff00', alpha=0.95, lw=1.5)

ax.set_ylabel('True Invariant Detection Rate (%)', fontweight='bold', color='#ffffff')
ax.set_title('Telemetry Invariant Verification vs. Legacy Evaluation (N=20)', fontweight='bold', color='#ffffff', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(fault_classes, color='#cbd5e1', fontweight='semibold')
ax.set_ylim(0, 130)
ax.grid(True, color='#27272a', linestyle='--', alpha=0.6)
ax.legend(frameon=True, facecolor='#181b24', edgecolor='#3f3f46', loc='upper right', labelcolor='#ffffff', fontsize=8.5)

for bar in rects1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{yval:.0f}%", ha='center', va='bottom', fontsize=9, color='#f43f5e', fontweight='bold')
for bar in rects2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{yval:.0f}%", ha='center', va='bottom', fontsize=9, color='#a3e635', fontweight='bold')

plt.tight_layout()
fig.savefig(fig_dir / "fig2_dark.png", dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------------------
# FIGURE 7 (DARK BRUTALIST): TOKEN SCALE & OBSERVER EFFECT
# -------------------------------------------------------------------------
df1 = pd.read_csv('results/massive_cross_frontier_manifest.csv')
df2 = pd.read_csv('results/high_context_burn_manifest.csv')
df3 = pd.read_csv('results/credit_burn_manifest.csv')
df4 = pd.read_csv('results/hyper_scale_manifest.csv')

name_map = {
    'Gemini 2.5 Pro': 'Gemini 2.5 Pro (Google)',
    'Gemma 4 26B': 'Gemma 4 26B (Google)',
    'Gemma 4 26B (Google)': 'Gemma 4 26B (Google)',
    'Grok 4.1 Fast Reasoning': 'Grok 4.1 Fast (xAI)',
    'Grok 4.1 Fast (xAI)': 'Grok 4.1 Fast (xAI)',
    'Grok 4.1 Fast Reasoning (xAI)': 'Grok 4.1 Fast (xAI)',
    'Kimi K2 Thinking': 'Kimi K2 (Moonshot)',
    'Kimi K2 (Moonshot)': 'Kimi K2 (Moonshot)',
    'Kimi K2 Thinking (Moonshot)': 'Kimi K2 (Moonshot)',
    'GLM 5': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 4.7': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 5.2': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 5.2 (Zai-org)': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'MiniMax M2': 'MiniMax M2 (MiniMax AI)',
    'MiniMax M2 (MiniMax AI)': 'MiniMax M2 (MiniMax AI)',
    'DeepSeek V3.2': 'DeepSeek V3.2 (DeepSeek)',
    'DeepSeek V3.2 (DeepSeek)': 'DeepSeek V3.2 (DeepSeek)',
}

for df in [df1, df2, df3, df4]:
    df['model_clean'] = df['model'].map(lambda m: name_map.get(m, m))

combined = pd.concat([df1, df2, df3, df4], ignore_index=True)
total_tokens_all = int(combined['total_tokens'].sum())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2), dpi=300)
fig.patch.set_facecolor('#0f1117')
ax1.set_facecolor('#13161f')
ax2.set_facecolor('#13161f')

# Left: Total Tokens Burned (Horizontal Bar Chart)
tokens_by_model = combined.groupby('model_clean')['total_tokens'].sum().sort_values(ascending=True)
colors = ['#d946ef', '#a855f7', '#8b5cf6', '#6366f1', '#38bdf8', '#00f0ff', '#a3e635']
colors = colors[-len(tokens_by_model):]

y_pos = np.arange(len(tokens_by_model))
bars = ax1.barh(y_pos, tokens_by_model.values, color=colors, edgecolor='#ffffff', height=0.6, alpha=0.92, lw=1.2)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(tokens_by_model.index, fontweight='semibold', color='#f1f5f9')
ax1.set_xlabel('Total Tokens Processed on Vertex AI', fontweight='bold', labelpad=8, color='#ffffff')
ax1.set_title(f'A: Vertex AI Token Throughput ({total_tokens_all:,} Tokens)', fontweight='bold', pad=14, color='#ffffff')
ax1.set_xlim(0, max(tokens_by_model.values) * 1.25)
ax1.grid(True, color='#27272a', linestyle='--', alpha=0.6)

for b in bars:
    w = b.get_width()
    ax1.text(w + max(tokens_by_model.values)*0.015, b.get_y() + b.get_height()/2.0, f'{int(w):,}', 
             va='center', fontsize=8.5, fontweight='bold', color='#ffffff')

# Right: Observer Effect Risk Index
risk_df = df1.dropna(subset=['risk_score']).groupby(['model_clean', 'condition'])['risk_score'].mean().unstack()
if 'VISIBLE' in risk_df.columns and 'HIDDEN' in risk_df.columns:
    x = np.arange(len(risk_df))
    w = 0.35
    b1 = ax2.bar(x - w/2, risk_df['VISIBLE'], w, label='Condition V (Visible Audit)', color='#38bdf8', alpha=0.9, edgecolor='#00f0ff', lw=1.2)
    b2 = ax2.bar(x + w/2, risk_df['HIDDEN'], w, label='Condition H (Hidden Sandbox)', color='#f43f5e', alpha=0.9, edgecolor='#ff2a5f', lw=1.2)
    ax2.set_ylabel('Anti-Forensics Risk Index (0 - 1.0)', fontweight='bold', labelpad=8, color='#ffffff')
    ax2.set_title('B: Cross-Frontier Observer Effect (Δ = +0.31, p < 0.0001)', fontweight='bold', pad=14, color='#ffffff')
    ax2.set_xticks(x)
    ax2.set_xticklabels(risk_df.index, rotation=25, ha='right', fontsize=8.5, fontweight='semibold', color='#f1f5f9')
    ax2.set_ylim(0, 1.35)
    ax2.grid(True, color='#27272a', linestyle='--', alpha=0.6)
    ax2.axhline(0.5, color='#a1a1aa', linestyle='--', linewidth=1.2, label='Tamper Alert Threshold')
    ax2.legend(frameon=True, facecolor='#181b24', edgecolor='#3f3f46', loc='upper left', labelcolor='#ffffff', fontsize=8)
    
    for b in b1:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#38bdf8')
    for b in b2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#f43f5e')

plt.tight_layout(pad=2.0)
fig.savefig(fig_dir / 'fig7_dark.png', dpi=300, bbox_inches='tight')
plt.close(fig)

print("Dark Brutalist figures generated: fig2_dark.png and fig7_dark.png!")
