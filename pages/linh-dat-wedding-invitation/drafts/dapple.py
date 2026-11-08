# Renders assets/dapple.webp: the soft shadow of a leafy branch falling across the table from the
# upper right, as through a window, for a sunlit flat-lay. Dark, transparent, very soft; the page
# shows it at low opacity. Run: python3 drafts/dapple.py
from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

rng = np.random.default_rng(5)
W, H = 900, 1400
S = 2  # supersampling
img = Image.new("L", (W * S, H * S), 0)
d = ImageDraw.Draw(img)

def leaf(cx, cy, length, angle, width=0.42):
    pts = []
    for i in range(41):
        t = i / 40
        r = length * (t - 0.5)
        w = length * width * math.sin(math.pi * t) ** 0.9 / 2
        pts.append((r, w))
    pts += [(r, -w) for r, w in reversed(pts)]
    ca, sa = math.cos(angle), math.sin(angle)
    d.polygon([((cx + x * ca - y * sa) * S, (cy + x * sa + y * ca) * S) for x, y in pts], fill=255)

def branch(x0, y0, ang, length, leaves):
    pts = []
    x, y = x0, y0
    for i in range(60):
        ang += rng.normal(0, 0.03)
        x += math.cos(ang) * length / 60
        y += math.sin(ang) * length / 60
        pts.append((x, y))
    d.line([(px * S, py * S) for px, py in pts], fill=255, width=int(5 * S))
    for k in range(leaves):
        px, py = pts[int((k + 0.5) / leaves * 59)]
        side = 1 if k % 2 else -1
        la = ang + side * rng.uniform(0.7, 1.2)
        L = rng.uniform(70, 120)
        leaf(px + math.cos(la) * L * 0.55, py + math.sin(la) * L * 0.55, L, la)

# branches reach in from beyond the top right corner
branch(980, -60, math.radians(140), 700, 11)
branch(1000, 260, math.radians(165), 520, 8)
branch(860, -90, math.radians(115), 420, 6)

a = np.asarray(img.resize((W, H), Image.LANCZOS), float) / 255
# the further from the window, the softer the shadow: blur grows to the lower left
soft = [np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), float) / 255 for r in (7, 15, 26)]
yy, xx = np.mgrid[0:H, 0:W]
dist = np.clip(((W - xx) / W * 0.6 + yy / H * 0.6), 0, 1)
w1 = np.clip(1 - dist * 2, 0, 1)
w3 = np.clip(dist * 2 - 1, 0, 1)
w2 = 1 - w1 - w3
shade = soft[0] * w1 + soft[1] * w2 + soft[2] * w3
# and it fades out across the table
shade *= np.clip(1.25 - dist * 1.1, 0, 1)
out = np.zeros((H, W, 4))
out[..., :3] = np.array([58, 44, 30]) / 255
out[..., 3] = shade
dest = Path(__file__).resolve().parents[1] / "assets/dapple.webp"
Image.fromarray((out * 255).round().astype(np.uint8), "RGBA").save(dest, quality=80, method=6)
