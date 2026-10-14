from pathlib import Path
import os
from xml.sax.saxutils import escape

def main():
    rows = [
        ("NOW", "Building cloud and full-stack projects", "#58a6ff"),
        ("PREV", "M.Tech Cloud Computing | B.E. ECE", "#3fb950"),
        ("STACK", "AWS · Python · Linux · Docker · React", "#d2a8ff"),
        ("HIGHLIGHTS", "Cloud automation · AI · Web applications", "#f2cc60"),
    ]
    pieces = []
    static = os.getenv("STATIC") == "1"
    for i, (key, value, color) in enumerate(rows):
        style = "" if static else f' style="opacity:0;animation:fade .5s ease-out {i*180}ms forwards"'
        pieces.append(f'<text x="22" y="{85+i*58}" fill="{color}" font-size="12" font-family="monospace"{style}>{escape(key)}</text>')
        pieces.append(f'<text x="22" y="{108+i*58}" fill="#c9d1d9" font-size="14" font-family="monospace"{style}>{escape(value)}</text>')
    animation = "" if static else "@keyframes fade{to{opacity:1}}"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="300" viewBox="0 0 490 300">
<rect width="490" height="300" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M10 0H480Q490 0 490 10V32H0V10Q0 0 10 0" fill="#161b22"/>
<circle cx="16" cy="16" r="4" fill="#ff5f56"/><circle cx="30" cy="16" r="4" fill="#ffbd2e"/><circle cx="44" cy="16" r="4" fill="#27c93f"/>
<text x="62" y="20" fill="#8b949e" font-family="monospace" font-size="11">vigneshvp1501@github ~ $ whoami</text>
<style>{animation}</style>
{''.join(pieces)}
</svg>'''
    Path("info-card.svg").write_text(svg, encoding="utf-8")
    print("Created info-card.svg")

if __name__ == "__main__":
    main()
