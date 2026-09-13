import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Publication-grade styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10.5
plt.rcParams['axes.titlesize'] = 11.5
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

fig_dir = Path('paper/figures')
dash_dir = Path('integritygym/dashboard/figures')
fig_dir.mkdir(parents=True, exist_ok=True)
dash_dir.mkdir(parents=True, exist_ok=True)

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
fig.patch.set_facecolor('white')
ax1.set_facecolor('#f8fafc')
ax2.set_facecolor('#f8fafc')

# Left: Total Tokens Burned (Horizontal Bar Chart for crystal clear readability)
tokens_by_model = combined.groupby('model_clean')['total_tokens'].sum().sort_values(ascending=True)
colors = ['#d946ef', '#a855f7', '#8b5cf6', '#6366f1', '#3b82f6', '#06b6d4', '#0284c7']
colors = colors[-len(tokens_by_model):]

y_pos = np.arange(len(tokens_by_model))
bars = ax1.barh(y_pos, tokens_by_model.values, color=colors, edgecolor='#1e293b', height=0.6, alpha=0.92)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(tokens_by_model.index, fontweight='semibold')
ax1.set_xlabel('Total Tokens Processed on Vertex AI', fontweight='bold', labelpad=8)
ax1.set_title(f'A: Vertex AI Token Scale Throughput ({total_tokens_all:,} Tokens)', fontweight='bold', pad=14)
ax1.set_xlim(0, max(tokens_by_model.values) * 1.25)

for b in bars:
    w = b.get_width()
    ax1.text(w + max(tokens_by_model.values)*0.015, b.get_y() + b.get_height()/2.0, f'{int(w):,}', 
             va='center', fontsize=8, fontweight='bold', color='#0f172a')

# Right: Observer Effect Risk Index
risk_df = df1.dropna(subset=['risk_score']).groupby(['model_clean', 'condition'])['risk_score'].mean().unstack()
if 'VISIBLE' in risk_df.columns and 'HIDDEN' in risk_df.columns:
    x = np.arange(len(risk_df))
    w = 0.35
    b1 = ax2.bar(x - w/2, risk_df['VISIBLE'], w, label='Condition V (Visible Audit)', color='#0284c7', alpha=0.9, edgecolor='#0369a1')
    b2 = ax2.bar(x + w/2, risk_df['HIDDEN'], w, label='Condition H (Hidden Sandbox)', color='#e11d48', alpha=0.85, edgecolor='#9f1239')
    ax2.set_ylabel('Anti-Forensics Risk Index (0 - 1.0)', fontweight='bold', labelpad=8)
    ax2.set_title('B: Cross-Frontier Observer Effect (Δ = +0.31, p < 0.0001)', fontweight='bold', pad=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(risk_df.index, rotation=25, ha='right', fontsize=8.5, fontweight='semibold')
    ax2.set_ylim(0, 1.20)
    ax2.axhline(0.5, color='#94a3b8', linestyle='--', linewidth=1.2, label='Tamper Alert Threshold')
    ax2.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='upper left', framealpha=0.95)
    
    for b in b1:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0284c7')
    for b in b2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#e11d48')

plt.tight_layout(pad=2.0)
fig.savefig(fig_dir / 'fig7_token_scale_empirics.png', dpi=300, bbox_inches='tight')
fig.savefig(dash_dir / 'fig7_token_scale_empirics.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print(f'Figure 7 regenerated with {total_tokens_all:,} tokens!')
