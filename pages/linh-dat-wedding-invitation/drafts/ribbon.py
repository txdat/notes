# Renders assets/ribbon.webp: a narrow champagne satin ribbon lying flat across the card, pulled
# tight under the wax seal at its middle, with a tight contact shadow. Run: python3 drafts/ribbon.py
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

rng = np.random.default_rng(11)
W, M, H = 96, 16, 1600  # ribbon width, shadow margin each side, length (px)
TW = W + 2 * M
y = np.arange(H)[:, None].astype(float)
x = (np.arange(W)[None, :] + 0.5) / W
t = y / H  # 0 at the top edge of the card, 1 at the bottom, the seal at 0.5

# Lying flat, satin barely shades across its width; its sheen changes along the length as the
# ribbon rises and falls a little over the paper.
along = 0.06 * np.sin(y / 150 + 0.8) + 0.04 * np.sin(y / 57 + 2.0) + 0.015 * np.sin(y / 21)
sheen_pos = 0.5 + 0.18 * np.sin(y / 300 + 1.1)
gloss = np.clip(np.sin(y / 150 + 0.8) * 0.6 + np.sin(y / 57 + 2.0) * 0.4, 0, None) ** 2
sheen = (0.12 + 0.45 * gloss) * np.exp(-((x - sheen_pos) / 0.3) ** 2)
across = 1 - 0.035 * (2 * x - 1) ** 2

# Pulled tight under the seal: fine creases fan out above and below it and fade with distance.
d = (t - 0.5) * H / W  # distance from the seal in ribbon widths
fan = np.exp(-np.abs(d) / 3.2) * np.clip((np.abs(d) - 0.2) * 2, 0, 1)
crease = np.zeros((H, W))
for k, (slope, ph, amp) in enumerate([(0.9, 0.0, 1.0), (-0.7, 1.3, 0.8), (1.6, 2.2, 0.6), (-1.3, 0.6, 0.5)]):
    u = (x - 0.5) * slope * np.sign(d) + d * 0.35 + ph
    crease += amp * np.sin(u * 2 * np.pi)
crease = 0.075 * fan * crease

# Woven fibres run along the ribbon.
def streaks(rows, amp):
    n = rng.normal(0, 1, (rows, W))
    img = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return amp * (np.asarray(img, float) / 255 - 0.5)

tex = streaks(H // 90, 0.03) + streaks(H // 8, 0.018) + rng.normal(0, 0.006, (H, W))

base = np.array([229, 214, 188], float) / 255
hi = np.array([250, 244, 232], float) / 255
lum = (1 + along + crease + tex) * across
col = base * lum[..., None]
col = col * (1 - sheen[..., None]) + hi * sheen[..., None] * 1.0

# Selvedge: a fine darker thread at each edge.
px = np.arange(W)[None, :]
edge = np.minimum(px, W - 1 - px)
col *= np.where(edge < 1, 0.86, np.where(edge < 3, 0.95, 1.0))[..., None]

# Where it turns over the card's top and bottom edges.
end = np.clip(np.minimum(y, H - 1 - y) / 18, 0, 1)
col *= (0.8 + 0.2 * end)[..., None]

rgb = np.clip(col, 0, 1)
a = np.zeros((H, TW)); a[:, M:M + W] = 1
body = np.zeros((H, TW, 3)); body[:, M:M + W] = rgb

# A tight contact shadow: the ribbon lies on the paper, it does not float.
mask = Image.fromarray((a * 255).astype(np.uint8))
near = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.6)), float) / 255
soft = np.asarray(mask.transform(mask.size, Image.AFFINE, (1, 0, -2, 0, 1, 0)).filter(ImageFilter.GaussianBlur(4)), float) / 255
sha = np.maximum(near * 0.22, soft * 0.14)
alpha = a + sha * (1 - a)
dark = np.array([70, 50, 28], float) / 255
out_rgb = (body * a[..., None] + dark * (sha * (1 - a))[..., None]) / np.maximum(alpha, 1e-6)[..., None]
img = np.dstack([np.clip(out_rgb, 0, 1), alpha])
dest = Path(__file__).resolve().parents[1] / "assets/ribbon.webp"
Image.fromarray((img * 255).round().astype(np.uint8), "RGBA").save(dest, quality=90, method=6)
