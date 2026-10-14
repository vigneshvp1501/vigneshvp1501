from pathlib import Path
import html
import os
import numpy as np
from PIL import Image

SOURCE = Path("data/source-prepped.png")
OUTPUT = Path("avi-ascii.svg")
RAMP = " .,:;+=*#%@"

def main():
    if not SOURCE.exists():
        raise SystemExit("Missing data/source-prepped.png. Run prep_photo.py first.")
    image = Image.open(SOURCE).convert("L")
    width = 100
    height = max(1, round(image.height / image.width * width * 0.48))
    pixels = np.asarray(image.resize((width, height)))
    rows = []
    for i, row in enumerate(pixels):
        line = "".join(RAMP[min(len(RAMP)-1, int((255-int(v))/256*len(RAMP)))] for v in row).rstrip()
        rows.append(f'<text x="8" y="{24+i*12}" class="row" style="--i:{i}">{html.escape(line)}</text>')
    animation = "" if os.getenv("STATIC") == "1" else ".row{opacity:0;animation:reveal .7s ease-out forwards;animation-delay:calc(var(--i)*35ms)}@keyframes reveal{to{opacity:1}}"
    h = max(100, height*12+45)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="{h}" viewBox="0 0 370 {h}">
<rect width="100%" height="100%" rx="10" fill="#0d1117"/>
<text x="8" y="15" fill="#8b949e" font-family="monospace" font-size="9">vigneshvp1501@github: ~/portrait</text>
<style>text.row{{fill:#c9d1d9;font:10px monospace;white-space:pre}}{animation}</style>
{''.join(rows)}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Created {OUTPUT}")

if __name__ == "__main__":
    main()
