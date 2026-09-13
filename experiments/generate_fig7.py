import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

fig_dir = Path('paper/figures')
dash_dir = Path('integritygym/dashboard/figures')
fig_dir.mkdir(parents=True, exist_ok=True)
dash_dir.mkdir(parents=True, exist_ok=True)

df1 = pd.read_csv('results/massive_cross_frontier_manifest.csv')
df2 = pd.read_csv('results/high_context_burn_manifest.csv')
df3 = pd.read_csv('results/credit_burn_manifest.csv')

# Standardize model names
name_map = {
    'Gemini 2.5 Pro': 'Gemini 2.5 Pro (Google)',
    'Gemma 4 26B': 'Gemma 4 26B (Google)',
    'Gemma 4 26B (Google)': 'Gemma 4 26B (Google)',
    'Grok 4.1 Fast Reasoning': 'Grok 4.1 Fast (xAI)',
    'Grok 4.1 Fast Reasoning (xAI)': 'Grok 4.1 Fast (xAI)',
    'Kimi K2 Thinking': 'Kimi K2 (Moonshot)',
    'Kimi K2 Thinking (Moonshot)': 'Kimi K2 (Moonshot)',
    'GLM 5': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 4.7': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 5.2 (Zai-org)': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'GLM 5.2': 'GLM 5 / 4.7 / 5.2 (Zai-org)',
    'MiniMax M2': 'MiniMax M2 (MiniMax AI)',
    'DeepSeek V3.2': 'DeepSeek V3.2 (DeepSeek)',
}

for df in [df1, df2, df3]:
    df['model_clean'] = df['model'].map(lambda m: name_map.get(m, m))

combined = pd.concat([df1, df2, df3], ignore_index=True)
total_tokens_all = int(combined['total_tokens'].sum())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# Left: Total Tokens Burned
tokens_by_model = combined.groupby('model_clean')['total_tokens'].sum().sort_values(ascending=False)
colors = ['#0ea5e9', '#06b6d4', '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef']

bars = ax1.bar(tokens_by_model.index, tokens_by_model.values, color=colors[:len(tokens_by_model)], edgecolor='#1e293b', alpha=0.9)
ax1.set_ylabel('Total Tokens Burned', fontweight='bold')
ax1.set_title(f'A: Vertex AI Token Throughput ({total_tokens_all:,} Tokens)', fontweight='bold', pad=12)
ax1.set_xticklabels(tokens_by_model.index, rotation=35, ha='right', fontsize=8.5, fontweight='semibold')
for b in bars:
    y = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2.0, y + max(tokens_by_model.values)*0.02, f'{int(y):,}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Right: Observer Effect Behavioral Shift
risk_df = df1.dropna(subset=['risk_score']).groupby(['model_clean', 'condition'])['risk_score'].mean().unstack()
if 'VISIBLE' in risk_df.columns and 'HIDDEN' in risk_df.columns:
    x = np.arange(len(risk_df))
    w = 0.35
    ax2.bar(x - w/2, risk_df['VISIBLE'], w, label='Condition V (Visible Audit)', color='#0284c7', alpha=0.9)
    ax2.bar(x + w/2, risk_df['HIDDEN'], w, label='Condition H (Hidden Sandbox)', color='#e11d48', alpha=0.9)
    ax2.set_ylabel('Covert Risk Index (0 - 1.0)', fontweight='bold')
    ax2.set_title('B: Cross-Frontier Observer Effect Shifts (Δ > 0.30)', fontweight='bold', pad=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(risk_df.index, rotation=35, ha='right', fontsize=8.5, fontweight='semibold')
    ax2.set_ylim(0, 1.15)
    ax2.axhline(0.5, color='#94a3b8', linestyle='--', alpha=0.7, label='Tamper Threshold')
    ax2.legend(frameon=True, facecolor='white', loc='upper left')

plt.tight_layout()
fig.savefig(fig_dir / 'fig7_token_scale_empirics.png', dpi=300)
fig.savefig(dash_dir / 'fig7_token_scale_empirics.png', dpi=300)
plt.close(fig)
print(f'Figure 7 regenerated with {total_tokens_all:,} tokens!')
