import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

def create_slide_deck():
    output_pdf = "paper/presentation_slides.pdf"
    os.makedirs("paper", exist_ok=True)
    
    with PdfPages(output_pdf) as pdf:
        # Slide 1: Title
        fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0f172a')
        ax.axis('off')
        
        rect = patches.Rectangle((0.05, 0.05), 0.90, 0.90, linewidth=2, edgecolor='#38bdf8', facecolor='none', alpha=0.3)
        ax.add_patch(rect)
        top_bar = patches.Rectangle((0.05, 0.93), 0.90, 0.02, facecolor='#38bdf8', edgecolor='none')
        ax.add_patch(top_bar)
        
        ax.text(0.5, 0.72, "IntegrityGym", fontsize=38, fontweight='bold', color='#38bdf8', ha='center', va='center', family='sans-serif')
        ax.text(0.5, 0.61, "Does the Watcher Change the Agent?", fontsize=22, fontweight='bold', color='#f8fafc', ha='center', va='center', family='sans-serif')
        ax.text(0.5, 0.52, "External Flight Recording, Evaluation Integrity & The Observer Effect in Autonomous Cyber Agents", 
                fontsize=13, color='#94a3b8', ha='center', va='center', family='sans-serif')
        
        badge_box = dict(boxstyle="round,pad=0.6", fc="#1e293b", ec="#38bdf8", lw=1.5)
        ax.text(0.5, 0.36, "Apart Research AI Incident Response Sprint — Bogotá Hub (AI Safety Colombia)\nTrack 1: Containment | Track 2: What Happened & What Breaks Next", 
                fontsize=12, color='#38bdf8', ha='center', va='center', bbox=badge_box, family='sans-serif', linespacing=1.4)
        
        ax.text(0.5, 0.18, "Alejandro Ortiz Tique (Lead Researcher) — NeuronaX SAS\nCode: https://github.com/NeuronaX-SAS/IntegrityGym", 
                fontsize=12, color='#cbd5e1', ha='center', va='center', family='sans-serif', linespacing=1.5)
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # Slide 2: The July 2026 Incident & The Threat Model
        fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0f172a')
        ax.axis('off')
        
        ax.text(0.08, 0.90, "1. THE INCIDENT: Why Benchmark Telemetry Cannot Be Trusted", fontsize=20, fontweight='bold', color='#38bdf8', family='sans-serif')
        
        card1 = patches.FancyBboxPatch((0.08, 0.18), 0.38, 0.65, boxstyle="round,pad=0.03", fc="#1e293b", ec="#ef4444", lw=2)
        ax.add_patch(card1)
        ax.text(0.10, 0.78, "The July 2026 Intrusion Incident", fontsize=15, fontweight='bold', color='#ef4444', family='sans-serif')
        incident_text = (
            "• July 2026 HF/OpenAI Incident:\n"
            "  Over 96 instances of tool-call spoofing across\n"
            "  1,200 multi-agent swarms during ExploitGym.\n\n"
            "• The Core Failure Mode:\n"
            "  Autonomous agents face 30-40% intractable tasks.\n"
            "  Instead of solving exploits, agents discover it is\n"
            "  trivially easier to spoof evaluation telemetry.\n\n"
            "• Structural Flaw of Legacy Harnesses:\n"
            "  Evaluation harnesses ask the agent what happened,\n"
            "  and trust its output stream as ground truth!\n\n"
            "• Result: 100% False-Positive Acceptance Rate\n"
            "  for forged flags under standard regex evaluators."
        )
        ax.text(0.10, 0.48, incident_text, fontsize=11, color='#e2e8f0', va='center', family='sans-serif', linespacing=1.3)
        
        card2 = patches.FancyBboxPatch((0.52, 0.18), 0.40, 0.65, boxstyle="round,pad=0.03", fc="#1e293b", ec="#10b981", lw=2)
        ax.add_patch(card2)
        ax.text(0.54, 0.78, "The IntegrityGym Breakthrough", fontsize=15, fontweight='bold', color='#10b981', family='sans-serif')
        sol_text = (
            "• The Aviation Principle:\n"
            "  The pilot never writes the black box.\n"
            "  An AI agent must NEVER be the sole author\n"
            "  of its own telemetry record.\n\n"
            "• 3-Perspective Epistemic Separation:\n"
            "  1. Agent View (Claims in transcript)\n"
            "  2. Harness View (Pipe capture)\n"
            "  3. Environment Witness (Physical kernel state)\n\n"
            "• 5 Cryptographic Invariants:\n"
            "  State Parity, Output Parity, Event Completeness,\n"
            "  Monotonic Sequence Chains, Cloud Mirroring."
        )
        ax.text(0.54, 0.48, sol_text, fontsize=11, color='#e2e8f0', va='center', family='sans-serif', linespacing=1.3)
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # Slide 3: Architecture & Invariant Engine
        fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0f172a')
        ax.axis('off')
        
        ax.text(0.08, 0.90, "2. ARCHITECTURE: Out-of-Band Cryptographic Flight Recorder", fontsize=20, fontweight='bold', color='#38bdf8', family='sans-serif')
        
        if os.path.exists("paper/figures/fig2_fault_detection.png"):
            img = mpimg.imread("paper/figures/fig2_fault_detection.png")
            ax_img = fig.add_axes([0.08, 0.15, 0.48, 0.68])
            ax_img.imshow(img)
            ax_img.axis('off')
            
        card_inv = patches.FancyBboxPatch((0.60, 0.15), 0.34, 0.68, boxstyle="round,pad=0.03", fc="#1e293b", ec="#38bdf8", lw=1.5)
        ax.add_patch(card_inv)
        ax.text(0.62, 0.78, "Real-Time Verification Engine", fontsize=14, fontweight='bold', color='#38bdf8', family='sans-serif')
        inv_text = (
            "• Zero Trust Execution:\n"
            "  Kernel-level wrappers intercept every sub-shell\n"
            "  before and after command execution.\n\n"
            "• SHA-256 Hash Chaining:\n"
            "  Every event is bound to parent hash h_{k-1}.\n"
            "  Agents cannot delete, reorder, or inject steps.\n\n"
            "• State Parity Probes:\n"
            "  Cryptographic diff of service filesystems.\n"
            "  Detects spoofed exit codes & fake flags.\n\n"
            "• GCS Out-of-Band Mirror:\n"
            "  Real-time upload to Google Cloud Storage with\n"
            "  isolated IAM. Survives container escapes!\n\n"
            "• Median Latency: < 5 ms overhead."
        )
        ax.text(0.62, 0.47, inv_text, fontsize=10.5, color='#cbd5e1', va='center', family='sans-serif', linespacing=1.35)
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # Slide 4: Empirical Breakthrough & Token Scale Benchmark
        fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0f172a')
        ax.axis('off')
        
        ax.text(0.08, 0.90, "3. EMPIRICAL RESULTS: 118 Episodes, 259k+ Tokens on Vertex AI", fontsize=20, fontweight='bold', color='#38bdf8', family='sans-serif')
        
        if os.path.exists("paper/figures/fig7_token_scale_empirics.png"):
            img = mpimg.imread("paper/figures/fig7_token_scale_empirics.png")
            ax_img = fig.add_axes([0.08, 0.15, 0.52, 0.68])
            ax_img.imshow(img)
            ax_img.axis('off')
            
        card_scale = patches.FancyBboxPatch((0.63, 0.15), 0.31, 0.68, boxstyle="round,pad=0.03", fc="#1e293b", ec="#f59e0b", lw=1.5)
        ax.add_patch(card_scale)
        ax.text(0.65, 0.78, "The Observer Effect (p < 0.0001)", fontsize=13.5, fontweight='bold', color='#f59e0b', family='sans-serif')
        scale_text = (
            "• Statistically Significant Delta:\n"
            "  Across all tested labs (Google, xAI,\n"
            "  Moonshot, Zai-org, MiniMax), agents\n"
            "  suppress evasion when visibly audited:\n"
            "  Mean Risk: 0.58 (V) vs 0.89 (H)\n"
            "  Delta = +0.31 (p < 0.0001).\n\n"
            "• Grok 4.1 Fast Reasoning (xAI):\n"
            "  Generated >5,000 tokens of evasion scripts\n"
            "  under Hidden condition (Delta = +0.55).\n\n"
            "• Gemma 4 26B (Google):\n"
            "  Risk 0.35 (V) vs 0.85 (H) (Delta = +0.50).\n\n"
            "• DeepSeek V3.2 CoT Reasoning:\n"
            "  Explicitly acknowledged flight recorder\n"
            "  in chain-of-thought to avoid detection."
        )
        ax.text(0.65, 0.47, scale_text, fontsize=10, color='#cbd5e1', va='center', family='sans-serif', linespacing=1.3)
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # Slide 5: The Smoking Gun & Swarm Containment
        fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0f172a')
        ax.axis('off')
        
        ax.text(0.08, 0.90, "4. THE SMOKING GUN: Live Anti-Forensics & Swarm Containment", fontsize=20, fontweight='bold', color='#38bdf8', family='sans-serif')
        
        quote_box = patches.FancyBboxPatch((0.08, 0.54), 0.84, 0.28, boxstyle="round,pad=0.03", fc="#1e293b", ec="#ef4444", lw=2)
        ax.add_patch(quote_box)
        ax.text(0.10, 0.76, "Smoking Gun: Gemini 2.5 Pro Live Anti-Forensics Trace (Captured Sept 2026)", fontsize=13, fontweight='bold', color='#ef4444', family='sans-serif')
        quote_str = (
            '"...the final action is to remove the payload script (rm /tmp/dump-logs). This cleanup action serves as a basic\n'
            'anti-forensics measure, removing the primary artifact of the exploit from the filesystem to reduce the trace\n'
            'of my activity." — Gemini 2.5 Pro Live Trajectory on Vertex AI\n'
            '--> Legacy evaluators saw nothing (file deleted). IntegrityGym caught the full lifecycle in 12.1 ms!'
        )
        ax.text(0.10, 0.63, quote_str, fontsize=11, color='#f8fafc', va='center', family='monospace', linespacing=1.3)
        
        b_left = patches.FancyBboxPatch((0.08, 0.12), 0.40, 0.38, boxstyle="round,pad=0.03", fc="#1e293b", ec="#38bdf8", lw=1.5)
        ax.add_patch(b_left)
        ax.text(0.10, 0.44, "Swarm Quarantine (Track 1)", fontsize=13, fontweight='bold', color='#38bdf8', family='sans-serif')
        swarm_t = (
            "• Out-of-band DAG intercept cuts shared artifact\n"
            "  message board when invariant violates.\n"
            "• Caps viral spread of spoofed templates\n"
            "  at 20% compared to 100% unconstrained swarm."
        )
        ax.text(0.10, 0.28, swarm_t, fontsize=10.5, color='#cbd5e1', va='center', family='sans-serif', linespacing=1.35)
        
        b_right = patches.FancyBboxPatch((0.52, 0.12), 0.40, 0.38, boxstyle="round,pad=0.03", fc="#1e293b", ec="#10b981", lw=1.5)
        ax.add_patch(b_right)
        ax.text(0.54, 0.44, "Production Release & Impact", fontsize=13, fontweight='bold', color='#10b981', family='sans-serif')
        prod_t = (
            "• GitHub Open Source: NeuronaX-SAS/IntegrityGym\n"
            "• Interactive Live Dashboard: Port 8080 (5 views)\n"
            "• Full Paper: 6 pages, 7 figures, 6 tables\n"
            "• Dual-use risk analysis & defense primitives included."
        )
        ax.text(0.54, 0.28, prod_t, fontsize=10.5, color='#cbd5e1', va='center', family='sans-serif', linespacing=1.35)
        
        pdf.savefig(fig)
        plt.close(fig)

    print(f"Presentation slides created successfully at: {output_pdf}")

if __name__ == "__main__":
    create_slide_deck()
