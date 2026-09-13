import subprocess
from pathlib import Path

html_file = Path('paper/paper.html')
tex_file = Path('paper/paper.tex')

# Read markdown content
md_content = Path('paper/draft_paper.md').read_text(encoding='utf-8')

# Re-generate paper.html with the new citations
with open('experiments/compile_official_apart_paper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Execute update_paper_stats.py to ensure numbers and citations are aligned
subprocess.run(['uv', 'run', 'python', 'experiments/update_paper_stats.py'], check=True)

# Now compile to PDF
edge_cmd = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--print-to-pdf=c:\\dev\\IntegrityGym\\paper\\paper.pdf",
    "file:///c:/dev/IntegrityGym/paper/paper.html"
]

print("Compiling paper.pdf via Microsoft Edge headless...")
res = subprocess.run(edge_cmd, capture_output=True, text=True)
print("Edge exit code:", res.returncode)

p = Path("paper/paper.pdf")
if p.exists():
    print(f"paper.pdf successfully updated! Size: {p.stat().st_size:,} bytes")
