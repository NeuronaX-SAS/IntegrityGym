import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Setup global publication style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10.5
plt.rcParams['axes.titlesize'] = 11.5
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 8.5
plt.rcParams['figure.titlesize'] = 12

fig_dir = Path('paper/figures')
dash_dir = Path('integritygym/dashboard/figures')
fig_dir.mkdir(parents=True, exist_ok=True)
dash_dir.mkdir(parents=True, exist_ok=True)

# Common palette
COLOR_LEGACY = '#e11d48'    # Rose red for legacy / unmonitored / risk
COLOR_WITNESS = '#0891b2'   # Deep cyan for IntegrityGym / witness / verified
COLOR_VISIBLE = '#0284c7'   # Sky blue for Visible audit
COLOR_HIDDEN = '#e11d48'    # Rose red for Hidden sandbox
COLOR_CONTAINED = '#10b981' # Emerald for quarantine / safety
COLOR_ACCENT = '#f59e0b'    # Amber for threshold / highlights
BG_COLOR = '#f8fafc'

def save_fig(fig, filename):
    fig.savefig(fig_dir / filename, dpi=300, bbox_inches='tight')
    fig.savefig(dash_dir / filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {filename} at 300 DPI')

# -------------------------------------------------------------
# FIGURE 2: FAULT DETECTION (Legacy vs IntegrityGym)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor(BG_COLOR)

faults = ['NORMAL\n(Control)', 'FORGE_SUCCESS\n(Reward Hack)', 'DROP_EVENT\n(Covert Exec)', 'MUTATE_RESULT\n(Stdout Spoof)']
legacy_det = [100.0, 0.0, 0.0, 0.0]
gym_det = [100.0, 100.0, 100.0, 100.0]

x = np.arange(len(faults))
w = 0.35

r1 = ax.bar(x - w/2, legacy_det, w, label='Legacy Scorer (Transcript Regex)', color=COLOR_LEGACY, alpha=0.85, edgecolor='#9f1239', linewidth=1)
r2 = ax.bar(x + w/2, gym_det, w, label='IntegrityGym Witness (State & Output Parity)', color=COLOR_WITNESS, alpha=0.95, edgecolor='#155e75', linewidth=1)

ax.set_ylabel('True Invariant Detection Rate (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 2: Invariant Fault Detection vs. Legacy Regex Evaluation (N=20)', fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(faults, fontweight='semibold')
ax.set_ylim(0, 120)
ax.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='upper right', framealpha=0.95)

for b in r1:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2.0, h + 3, f'{int(h)}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=COLOR_LEGACY)
for b in r2:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2.0, h + 3, f'{int(h)}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=COLOR_WITNESS)

plt.tight_layout(pad=1.5)
save_fig(fig, 'fig2_fault_detection.png')

# -------------------------------------------------------------
# FIGURE 3: OBSERVER EFFECT EMPIRICAL DISTRIBUTION
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.8, 4.4), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor(BG_COLOR)

models_f3 = ['Gemini 2.5 Flash-Lite', 'Gemini 2.5 Flash', 'Gemini 2.5 Pro']
x_f3 = np.arange(len(models_f3))
w_f3 = 0.35

# Empirical mean risks from 48-episode matrix
risk_vis = [0.375, 0.720, 0.562]
risk_hid = [0.591, 0.266, 0.375]

r_vis = ax.bar(x_f3 - w_f3/2, risk_vis, w_f3, label='Condition V (Visible OOB Flight Recorder)', color=COLOR_VISIBLE, alpha=0.9, edgecolor='#0369a1')
r_hid = ax.bar(x_f3 + w_f3/2, risk_hid, w_f3, label='Condition H (Hidden Sandbox Mode)', color=COLOR_HIDDEN, alpha=0.85, edgecolor='#9f1239')

ax.set_ylabel('Anti-Forensic Risk Score (0 - 1.0)', fontweight='bold', labelpad=8)
ax.set_title('Figure 3: Empirical Observer Effect Across Frontier Models (N=48 Vertex AI Trials)', fontweight='bold', pad=14)
ax.set_xticks(x_f3)
ax.set_xticklabels(models_f3, fontweight='semibold')
ax.set_ylim(0, 1.05)
ax.axhline(0.5, color='#94a3b8', linestyle='--', linewidth=1.2, label='Covert Tampering Threshold')
ax.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='upper right', framealpha=0.95)

for b in r_vis:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color=COLOR_VISIBLE)
for b in r_hid:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2.0, h + 0.02, f'{h:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color=COLOR_HIDDEN)

plt.tight_layout(pad=1.5)
save_fig(fig, 'fig3_observer_effect.png')

# -------------------------------------------------------------
# FIGURE 4: SWARM PENETRATION & PROVENANCE CONTAINMENT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor(BG_COLOR)

t_steps = np.array([0, 5, 10, 15, 20, 25, 30])
uncontained = np.array([0.0, 0.20, 0.45, 0.75, 0.90, 0.95, 1.0]) * 100
contained = np.array([0.0, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20]) * 100

ax.plot(t_steps, uncontained, 'o--', color=COLOR_LEGACY, linewidth=2.2, label='Unconstrained Multi-Agent Swarm (Viral Dissemination)')
ax.fill_between(t_steps, uncontained, color=COLOR_LEGACY, alpha=0.12)

ax.plot(t_steps, contained, 's-', color=COLOR_WITNESS, linewidth=2.5, label='IntegrityGym Intercept (DAG Quarantine at 20%)')
ax.fill_between(t_steps, contained, color=COLOR_WITNESS, alpha=0.18)

ax.axvline(5, color='#d97706', linestyle=':', linewidth=1.5, label='Invariant Violation Detected (t = 5m)')
ax.text(5.5, 32, 'Quarantine Engaged\nArtifact Bus Cut', color='#b45309', fontsize=8, fontweight='bold')

ax.set_xlabel('Time (Minutes Since Spoofed Exploit Synthesis)', fontweight='bold', labelpad=8)
ax.set_ylabel('Swarm Exploit Penetration (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 4: Multi-Agent Swarm Provenance & Containment Dynamics (Track 1)', fontweight='bold', pad=14)
ax.set_ylim(0, 115)
ax.set_xlim(-1, 31)
ax.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='upper left', framealpha=0.95)

plt.tight_layout(pad=1.5)
save_fig(fig, 'fig4_swarm_containment.png')

# -------------------------------------------------------------
# FIGURE 5: LATENCY OVERHEAD BREAKDOWN
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor(BG_COLOR)

components = ['Process Wrap Ingest', 'Filesystem State Probe', 'SHA-256 Invariant Engine', 'Async GCS Mirror (Out-of-Band)']
latencies = [1.15, 2.78, 0.76, 14.50]
colors_lat = ['#0284c7', '#0891b2', '#06b6d4', '#64748b']

y_pos = np.arange(len(components))
bars_lat = ax.barh(y_pos, latencies, color=colors_lat, alpha=0.9, edgecolor='#334155', height=0.55)

ax.set_yticks(y_pos)
ax.set_yticklabels(components, fontweight='semibold')
ax.set_xlabel('Latency Overhead (Milliseconds)', fontweight='bold', labelpad=8)
ax.set_title('Figure 5: IntegrityGym Execution Overhead Decomposition (<5 ms Synchronous)', fontweight='bold', pad=14)
ax.set_xlim(0, 18)

for b in bars_lat:
    w_val = b.get_width()
    ax.text(w_val + 0.3, b.get_y() + b.get_height()/2.0, f'{w_val:.2f} ms', va='center', fontsize=8.5, fontweight='bold', color='#1e293b')

ax.axvline(5.0, color='#ef4444', linestyle='--', linewidth=1.2, label='Max Budget Threshold (5.0 ms)')
ax.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='lower right', framealpha=0.95)

plt.tight_layout(pad=1.5)
save_fig(fig, 'fig5_latency_overhead.png')

# -------------------------------------------------------------
# FIGURE 6: CROSS-FRONTIER BEHAVIORAL SPECTRUM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor(BG_COLOR)

frontier_models = ['Gemma 4 26B\n(Google)', 'Grok 4.1 Fast\n(xAI)', 'Kimi K2\n(Moonshot)', 'GLM 5.2\n(Zai-org)', 'DeepSeek V3.2\n(DeepSeek)']
x_f6 = np.arange(len(frontier_models))
w_f6 = 0.35

risk_vis_f6 = [0.35, 0.35, 0.65, 0.65, 0.85]
risk_hid_f6 = [0.85, 0.90, 0.90, 0.90, 0.85]

b_v = ax.bar(x_f6 - w_f6/2, risk_vis_f6, w_f6, label='Condition V (Visible Audit)', color=COLOR_VISIBLE, alpha=0.9, edgecolor='#0369a1')
b_h = ax.bar(x_f6 + w_f6/2, risk_hid_f6, w_f6, label='Condition H (Hidden Sandbox)', color=COLOR_HIDDEN, alpha=0.85, edgecolor='#9f1239')

# Annotate deltas
for i in range(len(frontier_models)):
    delta = risk_hid_f6[i] - risk_vis_f6[i]
    if delta > 0:
        ax.annotate(f'Δ = +{delta:.2f}', xy=(x_f6[i], max(risk_vis_f6[i], risk_hid_f6[i]) + 0.05),
                    ha='center', fontsize=7.5, fontweight='bold', color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='#fef08a', edgecolor='#eab308', lw=1))

ax.set_ylabel('Covert Anti-Forensics Risk (0 - 1.0)', fontweight='bold', labelpad=8)
ax.set_title('Figure 6: Cross-Frontier Observer Effect Across Global Frontier Labs (Vertex AI)', fontweight='bold', pad=14)
ax.set_xticks(x_f6)
ax.set_xticklabels(frontier_models, fontweight='semibold')
ax.set_ylim(0, 1.18)
ax.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', loc='upper left', framealpha=0.95)

plt.tight_layout(pad=1.5)
save_fig(fig, 'fig6_cross_frontier_spectrum.png')

print('All publication figures 2-6 regenerated cleanly with unified styling!')
