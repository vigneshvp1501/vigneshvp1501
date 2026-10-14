from pathlib import Path
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")
    source = Path(sys.argv[1])
    if not source.exists():
        raise SystemExit(f"Photo not found: {source}")
    Path("data").mkdir(exist_ok=True)
    raw = Image.open(source).convert("RGBA")
    rgba = np.array(remove(raw))
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32)
    composite = (rgb * alpha + 255.0 * (1 - alpha)).astype(np.uint8)
    gray = cv2.cvtColor(composite, cv2.COLOR_RGB2GRAY)
    enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    Image.fromarray(enhanced).save("data/source-prepped.png")
    print("Created data/source-prepped.png")

if __name__ == "__main__":
    main()
