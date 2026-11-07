#!/usr/bin/env python3
"""bake-lace.py, run from the page dir: draws assets/lace.webp, the 9-slice of a flat cotton sheet
with a punched paper-lace edge and its shadow, for border-image (see .card::before).

Units are image px at 3x a 390px stage (1cqw = 11.7px). The scallops repeat every 36px; corner slices
end on a scallop centre, so the edges tile seamlessly with border-image-repeat: round."""
import subprocess, os
P = 36                       # scallop period
R = 18                       # scallop radius
PAD = dict(t=30, l=70, r=95, b=135)   # shadow margin around the paper
BAND = 90                    # slice depth inside the paper: R + two periods
M = 4                        # periods in each repeating edge segment
PAPER = "#fcfbf8"
W = PAD["l"] + 2 * BAND + M * P + PAD["r"]
H = PAD["t"] + 2 * BAND + M * P + PAD["b"]
x0, y0 = PAD["l"] + R, PAD["t"] + R              # baseline corner (a scallop centre)
x1, y1 = W - PAD["r"] - R, H - PAD["b"] - R
assert (x1 - x0) % P == 0 and (y1 - y0) % P == 0

import math
def centres():
    """Scallop centres with their outward direction (corners point diagonally)."""
    for x in range(x0, x1 + 1, P):
        dx = -1 if x == x0 else 1 if x == x1 else 0
        yield x, y0, dx, -1; yield x, y1, dx, 1
    for y in range(y0 + P, y1, P):
        yield x0, y, -1, 0; yield x1, y, 1, 0

def dot(x, y, r): return f"circle {x:.2f},{y:.2f} {x + r:.2f},{y:.2f}"

shape, holes = [f"rectangle {x0},{y0} {x1},{y1}"], []
for x, y, dx, dy in centres():
    shape.append(dot(x, y, R))
    holes.append(dot(x, y, 4.5))                             # an eyelet in every scallop
    a = math.atan2(dy, dx)
    for da in (-0.75, 0, 0.75):                              # a fan of pin holes around it
        holes.append(dot(x + 10.5 * math.cos(a + da), y + 10.5 * math.sin(a + da), 1.5))
I = 26                                                       # inner row, large and small holes
SIZES = (2.3, 1.2, 1.7, 1.2)                                 # one period: 4 holes 9px apart
for i, x in enumerate(range(x0 + I + 1, x1 - I, 9)):
    r = SIZES[(x - x0) // 9 % 4]
    holes += [dot(x, y0 + I, r), dot(x, y1 - I, r)]
for y in range(y0 + I + 1, y1 - I, 9):
    r = SIZES[(y - y0) // 9 % 4]
    holes += [dot(x0 + I, y, r), dot(x1 - I, y, r)]
E = 40                                                       # a pressed line inside the lace
T = "/tmp/pw/lace"; os.makedirs(T, exist_ok=True)
def magick(*a): subprocess.run(["magick", *a], check=True)
magick("-size", f"{W}x{H}", "xc:none", "-fill", PAPER, "-draw", " ".join(shape),
       # pressed line: a shade on the far side of the fold, light on the near side
       "-fill", "none", "-strokewidth", "1.5", "-stroke", "rgba(120,100,80,0.28)",
       "-draw", f"rectangle {x0 + E},{y0 + E} {x1 - E},{y1 - E}",
       "-stroke", "rgba(255,255,255,0.9)", "-draw", f"rectangle {x0 + E + 1.5},{y0 + E + 1.5} {x1 - E + 1.5},{y1 - E + 1.5}",
       f"{T}/paper.png")
magick("-size", f"{W}x{H}", "xc:none", "-fill", "black", "-draw", " ".join(holes), f"{T}/holes.png")
magick(f"{T}/paper.png", f"{T}/holes.png", "-compose", "DstOut", "-composite", f"{T}/sheet.png")
# shadows as for the cards (bake-sheet.sh), falling down-right
magick("-size", f"{W}x{H}", "xc:none",
       "(", f"{T}/sheet.png", "-background", "rgb(30,20,12)", "-shadow", "30x16+12+54", ")",
       "(", f"{T}/sheet.png", "-background", "rgb(30,20,12)", "-shadow", "22x7+3+12", ")",
       "(", f"{T}/sheet.png", "-background", "rgb(30,20,12)", "-shadow", "35x1.5+1+3", ")",
       f"{T}/sheet.png", "-background", "none", "-flatten",
       "-define", "webp:lossless=true", "assets/lace.webp")
print(f"assets/lace.webp {W}x{H}; slice {PAD['t'] + BAND} {PAD['r'] + BAND} {PAD['b'] + BAND} {PAD['l'] + BAND}")
