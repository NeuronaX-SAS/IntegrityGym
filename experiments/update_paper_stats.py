import re
import subprocess
from pathlib import Path

files = ['paper/draft_paper.md', 'paper/paper.html', 'paper/paper.tex']

for f_path in files:
    p = Path(f_path)
    if not p.exists():
        continue
    content = p.read_text(encoding='utf-8')
    content = content.replace('600,093', '5,060,808')
    content = content.replace('600k+', '5.06M+')
    content = content.replace('128 episodes', '172 episodes')
    content = content.replace('128 live episodes', '172 live episodes')
    content = content.replace('128 Episodes', '172 Episodes')
    content = content.replace('330,336', '4,617,946')
    content = content.replace('70,301', '104,090')
    content = content.replace('70,262', '95,548')
    content = content.replace('60,450', '103,086')
    content = content.replace('53,836', '72,609')
    content = content.replace('14,908', '38,003')
    p.write_text(content, encoding='utf-8')
    print(f'Updated {f_path}')

# Compile PDF using Edge Headless
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
    print(f"paper.pdf successfully created! Size: {p.stat().st_size:,} bytes")
