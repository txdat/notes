"""key-peony.py (run with python3 -I) SRC OUT WIDTH: cut a Gemini flower shot out of its flat cobalt-blue background.

Alpha comes from "blueness" (B - max(R, G)) measured against a smooth per-pixel estimate of the
background, so the backdrop's gradient and its cast shadows key out; the colour is then unmixed
from that background so petal edges carry no blue fringe. The Gemini sparkle in the bottom-right
corner is dropped, the result is cropped to the flowers and scaled to WIDTH px."""
import sys
import numpy as np
from PIL import Image

src, out, width = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
h, w, _ = im.shape
def blueness(c):  # share of B above the warmer channels: a shadowed backdrop (k x bg) scores like the backdrop
    return (c[..., 2] - np.maximum(c[..., 0], c[..., 1])) / np.maximum(c[..., 2], 1)
blue = blueness(im)

# background: average clearly-blue pixels, spread smoothly under the flowers
bgmask = (blue > 0.3).astype(np.float32)
def box(a, r):  # box blur along both axes, edge-padded
    for ax in (0, 1):
        p = np.pad(a, [(r, r) if i == ax else (0, 0) for i in (0, 1)], mode="edge")
        c = np.cumsum(p, axis=ax, dtype=np.float64)
        c = np.insert(c, 0, 0, axis=ax)
        n = a.shape[ax]
        a = (np.take(c, range(2 * r + 1, n + 2 * r + 1), axis=ax) - np.take(c, range(n), axis=ax)) / (2 * r + 1)
    return a.astype(np.float32)
def smooth(a, f=16, r=8):  # wide, smooth blur: downsample, three box passes, upsample
    small = np.asarray(Image.fromarray(a).resize((w // f, h // f), Image.BOX))
    for _ in range(3):
        small = box(small, r)
    return np.asarray(Image.fromarray(small).resize((w, h), Image.BILINEAR))
den = smooth(bgmask) + 1e-4
bg = np.stack([smooth(im[..., c] * bgmask) / den for c in range(3)], -1)
bgblue = blueness(bg)

FG = 0.06  # blueness at or below this is fully opaque (silver eucalyptus sits near 0)
a = np.clip((bgblue - blue) / (bgblue - FG), 0, 1)
a = np.clip((a - 0.06) / 0.94, 0, 1) ** 1.3  # tighten the soft rim so no backdrop glow is left
a[int(h * 0.86):, int(w * 0.86):] = 0  # Gemini sparkle

# unmix: C = a F + (1 - a) Bg
aa = np.maximum(a, 1e-3)[..., None]
fg = np.clip((im - (1 - a[..., None]) * bg) / aa, 0, 255)
# any blue left on soft edges: pull B back toward the warmer channels
fg[..., 2] = np.minimum(fg[..., 2], np.maximum(fg[..., 0], fg[..., 1]) + 10)

rgba = np.dstack([fg, a * 255]).round().astype(np.uint8)
img = Image.fromarray(rgba, "RGBA")
# drop isolated specks: keep the bbox of reasonably opaque pixels, padded
ys, xs = np.nonzero(a > 0.5)
pad = 12
img = img.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, w), min(ys.max() + pad, h)))
img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
img.save(out, quality=90, method=6)
print(out, img.size)
