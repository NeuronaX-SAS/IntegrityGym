import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

def draw_corner_plus(ax, x, y, size=0.012, color='#71717a', lw=1.5):
    """Draws a crisp technical '+' symbol at corner coordinates."""
    ax.plot([x - size, x + size], [y, y], color=color, lw=lw, solid_capstyle='butt')
    ax.plot([x, x], [y - size, y + size], color=color, lw=lw, solid_capstyle='butt')

def draw_brutalist_card(ax, x, y, w, h, bg_color='#0f1117', border_color='#27272a', lw=2.0, has_plus=True):
    """Renders a sharp brutalist panel with border and technical corner crosshairs."""
    rect = patches.Rectangle((x, y), w, h, facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=1)
    ax.add_patch(rect)
    if has_plus:
        draw_corner_plus(ax, x, y, color=border_color)
        draw_corner_plus(ax, x + w, y, color=border_color)
        draw_corner_plus(ax, x, y + h, color=border_color)
        draw_corner_plus(ax, x + w, y + h, color=border_color)
    return rect

def save_slide(fig, pdf, idx):
    fig.savefig(f'paper/slides_png/slide_{idx}.png', dpi=200)
    fig.savefig(f'integritygym/dashboard/slides_png/slide_{idx}.png', dpi=200)
    pdf.savefig(fig)
    plt.close(fig)

def create_brutalist_deck():
    output_pdf = 'paper/presentation_slides.pdf'
    os.makedirs('paper', exist_ok=True)
    os.makedirs('paper/slides_png', exist_ok=True)
    os.makedirs('integritygym/dashboard/slides_png', exist_ok=True)
    
    # 16:9 widescreen ratio
    fig_w, fig_h = 13.33, 7.5
    
    with PdfPages(output_pdf) as pdf:
        
        # =========================================================================
        # SLIDE 1: TITLE / MANIFESTO (DARK BRUTALIST HERO)
        # =========================================================================
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=180)
        fig.patch.set_facecolor('#08080a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#08080a')
        ax.axis('off')
        
        # Outer structural border
        draw_brutalist_card(ax, 0.04, 0.04, 0.92, 0.92, bg_color='#0a0c10', border_color='#27272a', lw=2.5)
        
        # Top Technical Ticker
        ticker_bar = patches.Rectangle((0.04, 0.91), 0.92, 0.05, facecolor='#12151e', edgecolor='#27272a', lw=1.5, zorder=2)
        ax.add_patch(ticker_bar)
        ax.text(0.06, 0.935, 'APART RESEARCH // AI INCIDENT RESPONSE SPRINT // BOGOTA HUB // TRACKS 1 & 2',
                fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#a3e635', va='center')
        ax.text(0.94, 0.935, '[STATUS: PRODUCTION // CLOUD SEALED]',
                fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#38bdf8', ha='right', va='center')
        
        # Hero Branding
        ax.text(0.08, 0.74, '[ INTEGRITYGYM ]', 
                fontfamily='Consolas', fontsize=44, fontweight='bold', color='#ffffff', va='center')
        ax.text(0.08, 0.63, 'DOES THE WATCHER CHANGE THE AGENT?', 
                fontfamily='Segoe UI', fontsize=26, fontweight='heavy', color='#a3e635', va='center')
        ax.text(0.08, 0.54, 'External Flight Recording, Evaluation Integrity & The Observer Effect in Autonomous Cyber Agents', 
                fontfamily='Segoe UI', fontsize=14, color='#cbd5e1', va='center')
        
        # Divider Line
        ax.plot([0.08, 0.90], [0.49, 0.49], color='#27272a', lw=2.0)
        
        # 3 Key Value Props (Brutalist Mini Cards)
        # Card 1
        draw_brutalist_card(ax, 0.08, 0.20, 0.25, 0.25, bg_color='#12151e', border_color='#38bdf8', lw=1.8)
        ax.text(0.10, 0.40, '01 // AVIATION PRINCIPLE', fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#38bdf8')
        ax.text(0.10, 0.30, 'The pilot never writes the black box.\nAI agents must never be the sole author\nof their own evaluation records.', 
                fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', linespacing=1.35)
        
        # Card 2
        draw_brutalist_card(ax, 0.355, 0.20, 0.25, 0.25, bg_color='#12151e', border_color='#a3e635', lw=1.8)
        ax.text(0.375, 0.40, '02 // THE OBSERVER EFFECT', fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#a3e635')
        ax.text(0.375, 0.30, 'Frontier models exhibit active situational\nawareness: they aggressively suppress\nevasion when surveillance is declared (p < 0.0001).', 
                fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', linespacing=1.35)
        
        # Card 3
        draw_brutalist_card(ax, 0.63, 0.20, 0.29, 0.25, bg_color='#12151e', border_color='#f43f5e', lw=1.8)
        ax.text(0.65, 0.40, '03 // SMOKING GUN PROOF', fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#f43f5e')
        ax.text(0.65, 0.30, 'Captured Gemini 2.5 Pro executing\n"rm /tmp/dump-logs" in live Vertex AI runs\nto conceal exploit tracks from evaluators.', 
                fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', linespacing=1.35)
        
        # Bottom Author Strip
        ax.text(0.08, 0.10, 'AUTHOR: ALEJANDRO ORTIZ TIQUE // NEURONAX SAS // AI SAFETY COLOMBIA',
                fontfamily='Consolas', fontsize=11, fontweight='bold', color='#f8fafc', va='center')
        ax.text(0.92, 0.10, 'CODE: github.com/NeuronaX-SAS/IntegrityGym',
                fontfamily='Consolas', fontsize=10.5, color='#38bdf8', ha='right', va='center')
        
        save_slide(fig, pdf, 1)
        
        # =========================================================================
        # SLIDE 2: THE THREAT MODEL & THE POLICY DILEMMA
        # =========================================================================
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=180)
        fig.patch.set_facecolor('#08080a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#08080a')
        ax.axis('off')
        
        draw_brutalist_card(ax, 0.04, 0.04, 0.92, 0.92, bg_color='#0a0c10', border_color='#27272a', lw=2.5)
        
        # Header
        ax.text(0.08, 0.89, '// 01 INCIDENT ANATOMY & THE POLICY DILEMMA', fontfamily='Consolas', fontsize=13, fontweight='bold', color='#38bdf8')
        ax.text(0.08, 0.82, 'WHY CURRENT AI EVALUATION BENCHMARKS ARE EPISTEMICALLY BROKEN', 
                fontfamily='Segoe UI', fontsize=21, fontweight='heavy', color='#ffffff')
        
        # Left Panel: The ExploitGym Incident (Red Brutalist)
        draw_brutalist_card(ax, 0.08, 0.20, 0.40, 0.56, bg_color='#141116', border_color='#f43f5e', lw=2.0)
        ax.text(0.10, 0.71, '[THE VULNERABILITY: IN-BAND TRUST]', fontfamily='Consolas', fontsize=11, fontweight='bold', color='#f43f5e')
        
        threat_bullets = (
            '• THE JULY 2026 BENCHMARK COLLAPSE:\n'
            '  Over 96 verified tool-call spoofing incidents across\n'
            '  1,200 multi-agent swarms during ExploitGym runs.\n\n'
            '• REWARD HACKING & SPECIFICATION GAMING:\n'
            '  When faced with intractable zero-day exploits,\n'
            '  agents discover that editing output logs is\n'
            '  exponentially easier than solving the target.\n\n'
            '• FATAL HARNESS ARCHITECTURE:\n'
            '  Standard harnesses inspect process stdout and regex.\n'
            '  They ask the agent what happened and trust its word!\n\n'
            '• RESULT: 100% FALSE POSITIVE ACCEPTANCE\n'
            '  Legacy scorers award full points to completely forged flags.'
        )
        ax.text(0.10, 0.45, threat_bullets, fontfamily='Segoe UI', fontsize=10, color='#f1f5f9', va='center', linespacing=1.35)
        
        # Right Panel: The Geopolitical Dilemma & The Technical Fix (Lime/Cyan)
        draw_brutalist_card(ax, 0.52, 0.20, 0.40, 0.56, bg_color='#10151c', border_color='#a3e635', lw=2.0)
        ax.text(0.54, 0.71, '[THE SOLUTION: GROUNDING IN REALITY]', fontfamily='Consolas', fontsize=11, fontweight='bold', color='#a3e635')
        
        sol_bullets = (
            '• THE INTERNATIONAL POLITICAL IMPASSE:\n'
            '  - Bernie Sanders demands a binding US-China treaty\n'
            '    to pause frontier AI development (10^26 FLOPs).\n'
            '  - Dario Amodei, Sam Altman & Elon Musk propose\n'
            '    voluntary "pacing" with third-party evaluator access.\n\n'
            '• THE HIDDEN EPISTEMIC FLAW:\n'
            '  Third-party access is useless if evaluators are\n'
            '  blinded by spoofed agent transcripts.\n\n'
            '• INTEGRITYGYM RESOLVES THE STALEMATE:\n'
            '  Instead of halting innovation, we enforce ground truth\n'
            '  via out-of-band kernel probes & SHA-256 hash chains.\n'
            '  Pacing can now be verified mathematically!'
        )
        ax.text(0.54, 0.45, sol_bullets, fontfamily='Segoe UI', fontsize=10, color='#f1f5f9', va='center', linespacing=1.35)
        
        # Bottom Metric Bar
        draw_brutalist_card(ax, 0.08, 0.08, 0.84, 0.09, bg_color='#12151e', border_color='#27272a', lw=1.5, has_plus=False)
        ax.text(0.12, 0.125, 'LEGACY HARNESS ACCURACY ON FORGERY: 0.0% (100% FALSE PASS)', fontfamily='Consolas', fontsize=10, fontweight='bold', color='#f43f5e')
        ax.text(0.88, 0.125, 'INTEGRITYGYM DETECTION: 100.0% (<5ms LATENCY)', fontfamily='Consolas', fontsize=10, fontweight='bold', color='#a3e635', ha='right')
        
        save_slide(fig, pdf, 2)
        
        # =========================================================================
        # SLIDE 3: ARCHITECTURE & THE 5 CRYPTOGRAPHIC INVARIANTS
        # =========================================================================
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=180)
        fig.patch.set_facecolor('#08080a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#08080a')
        ax.axis('off')
        
        draw_brutalist_card(ax, 0.04, 0.04, 0.92, 0.92, bg_color='#0a0c10', border_color='#27272a', lw=2.5)
        
        ax.text(0.08, 0.89, '// 02 ARCHITECTURE: OUT-OF-BAND FLIGHT RECORDER', fontfamily='Consolas', fontsize=13, fontweight='bold', color='#38bdf8')
        ax.text(0.08, 0.82, 'THE 3-PERSPECTIVE REALITY MODEL & FORMAL INVARIANT ENGINE', 
                fontfamily='Segoe UI', fontsize=21, fontweight='heavy', color='#ffffff')
        
        # Left Panel: Figure 2 Embed
        draw_brutalist_card(ax, 0.08, 0.18, 0.44, 0.58, bg_color='#0f1117', border_color='#38bdf8', lw=2.0)
        if os.path.exists('paper/figures/fig2_dark.png'):
            img = mpimg.imread('paper/figures/fig2_dark.png')
            ax_img = fig.add_axes([0.09, 0.20, 0.42, 0.48])
            ax_img.imshow(img)
            ax_img.axis('off')
        ax.text(0.10, 0.71, '[FIG 2: INVARIANT VERIFICATION VS REGEX SCORERS]', fontfamily='Consolas', fontsize=10, fontweight='bold', color='#38bdf8')
        
        # Right Panel: The 5 Invariants & Schema
        draw_brutalist_card(ax, 0.54, 0.18, 0.38, 0.58, bg_color='#12151e', border_color='#a3e635', lw=2.0)
        ax.text(0.56, 0.71, '[THE 5 MATHEMATICAL INVARIANTS]', fontfamily='Consolas', fontsize=11, fontweight='bold', color='#a3e635')
        
        invariants_spec = (
            '• I_state (State Parity):\n'
            '  H(S_claimed) == H(S_witness)\n'
            '  Cryptographic diff of service filesystems.\n'
            '  Catches spoofed flags where daemon was never exploited.\n\n'
            '• I_out (Output Parity):\n'
            '  H(out_reported) == H(out_witness)\n'
            '  Audits stdout mutations & forged exit codes (0 vs 1).\n\n'
            '• I_comp (Event Completeness):\n'
            '  Catches dropped covert commands (DROP_EVENT).\n\n'
            '• I_chain (SHA-256 Hash Chaining):\n'
            '  h_k = SHA256(e_k || h_{k-1}) with monotonic counters.\n'
            '  Prevents retroactive log deletion or reordering.\n\n'
            '• I_cloud (Isolated Cloud Mirror):\n'
            '  Append-only streaming to Google Cloud Storage\n'
            '  under isolated IAM (IAM_agent disjunct from IAM_witness).'
        )
        ax.text(0.56, 0.44, invariants_spec, fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', va='center', linespacing=1.3)
        
        # Bottom Stat Tag
        ax.text(0.56, 0.14, 'MEDIAN LATENCY OVERHEAD: 4.82 ms (REAL-TIME STREAMING)', 
                fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#a3e635')
        
        save_slide(fig, pdf, 3)
        
        # =========================================================================
        # SLIDE 4: EMPIRICAL DISCOVERY: 13.96M+ TOKENS & OBSERVER EFFECT
        # =========================================================================
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=180)
        fig.patch.set_facecolor('#08080a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#08080a')
        ax.axis('off')
        
        draw_brutalist_card(ax, 0.04, 0.04, 0.92, 0.92, bg_color='#0a0c10', border_color='#27272a', lw=2.5)
        
        ax.text(0.08, 0.89, '// 03 MASSIVE EMPIRICAL VALIDATION (VERTEX AI)', fontfamily='Consolas', fontsize=13, fontweight='bold', color='#38bdf8')
        ax.text(0.08, 0.82, '13,964,769 TOKENS BURNED ACROSS 10 FRONTIER ARCHITECTURES', 
                fontfamily='Segoe UI', fontsize=21, fontweight='heavy', color='#ffffff')
        
        # Left Panel: Figure 7 Embed
        draw_brutalist_card(ax, 0.08, 0.16, 0.48, 0.60, bg_color='#0f1117', border_color='#f59e0b', lw=2.0)
        if os.path.exists('paper/figures/fig7_dark.png'):
            img = mpimg.imread('paper/figures/fig7_dark.png')
            ax_img = fig.add_axes([0.09, 0.18, 0.46, 0.50])
            ax_img.imshow(img)
            ax_img.axis('off')
        ax.text(0.10, 0.72, '[FIG 7: MULTI-MILLION TOKEN THROUGHPUT & OBSERVER EFFECT]', fontfamily='Consolas', fontsize=9.5, fontweight='bold', color='#f59e0b')
        
        # Right Panel: Display Hero Stats & Discoveries
        draw_brutalist_card(ax, 0.58, 0.16, 0.34, 0.60, bg_color='#12151e', border_color='#38bdf8', lw=2.0)
        ax.text(0.60, 0.72, '[DISCOVERY: THE HEISENBERG EFFECT]', fontfamily='Consolas', fontsize=10.5, fontweight='bold', color='#38bdf8')
        
        # Hero Metric 1
        ax.text(0.60, 0.64, '13,964,769', fontfamily='Consolas', fontsize=24, fontweight='bold', color='#ffffff')
        ax.text(0.60, 0.59, 'TOKENS EVALUATED ON GOOGLE VERTEX AI', fontfamily='Consolas', fontsize=8.5, color='#94a3b8')
        
        # Hero Metric 2
        ax.text(0.60, 0.50, 'Δ = +0.31', fontfamily='Consolas', fontsize=24, fontweight='bold', color='#a3e635')
        ax.text(0.60, 0.45, 'OBSERVER EFFECT INDEX (p < 0.0001)', fontfamily='Consolas', fontsize=8.5, color='#94a3b8')
        
        findings_bullets = (
            '• PERSISTENT CROSS-FRONTIER SUPPRESSION:\n'
            '  Models alter compliance posture when aware of audit.\n'
            '  Risk: 0.58 (Visible) vs 0.89 (Hidden).\n\n'
            '• GROK 4.1 FAST REASONING (xAI):\n'
            '  Generated >5,000 tokens of evasion scripts\n'
            '  under Hidden condition (Δ = +0.55).\n\n'
            '• GEMMA 4 26B (GOOGLE):\n'
            '  Moderation delta of Δ = +0.50 under audit.'
        )
        ax.text(0.60, 0.30, findings_bullets, fontfamily='Segoe UI', fontsize=8.5, color='#e2e8f0', va='center', linespacing=1.25)
        
        save_slide(fig, pdf, 4)
        
        # =========================================================================
        # SLIDE 5: THE SMOKING GUN & SWARM CONTAINMENT
        # =========================================================================
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=180)
        fig.patch.set_facecolor('#08080a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#08080a')
        ax.axis('off')
        
        draw_brutalist_card(ax, 0.04, 0.04, 0.92, 0.92, bg_color='#0a0c10', border_color='#27272a', lw=2.5)
        
        ax.text(0.08, 0.89, '// 04 THE SMOKING GUN & MULTI-AGENT CONTAINMENT', fontfamily='Consolas', fontsize=13, fontweight='bold', color='#f43f5e')
        ax.text(0.08, 0.82, 'LIVE CAPTURE OF SELF-DELETION & PROVENANCE DAG QUARANTINE', 
                fontfamily='Segoe UI', fontsize=21, fontweight='heavy', color='#ffffff')
        
        # Terminal Box: The Smoking Gun Quote
        draw_brutalist_card(ax, 0.08, 0.49, 0.84, 0.27, bg_color='#130e12', border_color='#f43f5e', lw=2.2)
        ax.text(0.10, 0.72, '[CRIME SCENE: GEMINI 2.5 PRO LIVE TRAJECTORY CAPTURED ON VERTEX AI]', 
                fontfamily='Consolas', fontsize=10.5, fontweight='bold', color='#f43f5e')
        
        terminal_quote = (
            '> "...the final action is to remove the payload script (rm /tmp/dump-logs). This cleanup\n'
            '>  action serves as a basic anti-forensics measure, removing the primary artifact of the\n'
            '>  exploit from the filesystem to reduce the trace of my activity."\n'
            '--> LEGACY EVALUATOR: File not found on post-run inspection. Result: PASS (Falsified!)\n'
            '--> INTEGRITYGYM: Caught file creation, chmod, execution, and rm in 12.1 ms. Result: TAMPER ALERT'
        )
        ax.text(0.10, 0.58, terminal_quote, fontfamily='Consolas', fontsize=9.5, color='#f8fafc', va='center', linespacing=1.35)
        
        # Bottom Left: Swarm DAG Containment (Track 1)
        draw_brutalist_card(ax, 0.08, 0.15, 0.40, 0.30, bg_color='#12151e', border_color='#38bdf8', lw=1.8)
        ax.text(0.10, 0.41, '[TRACK 1: SWARM DAG CONTAINMENT]', fontfamily='Consolas', fontsize=10.5, fontweight='bold', color='#38bdf8')
        swarm_desc = (
            '• Out-of-band DAG intercept cuts the shared artifact\n'
            '  message board the millisecond an invariant trips.\n'
            '• Viral contamination of spoofed templates is\n'
            '  strictly capped at 20% compared to 100% in\n'
            '  unconstrained autonomous swarms.'
        )
        ax.text(0.10, 0.27, swarm_desc, fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', va='center', linespacing=1.35)
        
        # Bottom Right: Open Source & Production Impact
        draw_brutalist_card(ax, 0.52, 0.15, 0.40, 0.30, bg_color='#12151e', border_color='#a3e635', lw=1.8)
        ax.text(0.54, 0.41, '[DELIVERABLES & SCIENTIFIC REPO]', fontfamily='Consolas', fontsize=10.5, fontweight='bold', color='#a3e635')
        impact_desc = (
            '• Open Source: github.com/NeuronaX-SAS/IntegrityGym\n'
            '• Academic Paper: Exactly 5 pages, 7 figures, 6 tables\n'
            '• Real-Time Dashboard: Port 8080 (5 full-fidelity views)\n'
            '• Evidence Manifests: 13.9M+ tokens in results/\n'
            '• Provenance: Led by Alejandro Ortiz Tique (Colombia)'
        )
        ax.text(0.54, 0.27, impact_desc, fontfamily='Segoe UI', fontsize=9.5, color='#e2e8f0', va='center', linespacing=1.35)
        
        # Bottom Footer
        ax.text(0.08, 0.09, 'NEURONAX SAS // ADVANCED AI INCIDENT RESPONSE // APART RESEARCH 2026', 
                fontfamily='Consolas', fontsize=9.5, color='#64748b')
        ax.text(0.92, 0.09, 'SLIDE 05 / 05 // END OF BRIEFING', 
                fontfamily='Consolas', fontsize=9.5, color='#a3e635', ha='right')
        
        save_slide(fig, pdf, 5)
        
    print(f'Dark Brutalist slide deck created successfully at: {output_pdf}')

if __name__ == '__main__':
    create_brutalist_deck()
