#!/bin/sh
# Builds assets/og-2411.jpg, the 1200×630 link preview of 2411.html: the sealed card on cotton
# paper between two peonies, with the leaf shadow in the corner.
# drafts/og-2411-card.png is the closed card screenshotted from 2411.html at 4× with a transparent
# background and its CSS shadow off (Playwright: omitBackground, clip to #fold).
set -e
cd "$(dirname "$0")/../assets"
magick ../drafts/og-2411-card.png -resize x560 -background none -rotate -3 \
  \( +clone -background '#3c2c1c' -shadow 35x14+6+12 \) +swap -background none -layers merge +repage /tmp/og-card-s.png
magick -size 1200x630 xc:'#e7dfd1' \( cotton.webp -resize 512x512 -write mpr:t +delete \) -size 1200x630 tile:mpr:t -compose over -composite \
  /tmp/og-card-s.png -gravity center -geometry +0+0 -compose over -composite \
  \( peony-spray.webp -resize 340x -background none -rotate -100 -flop \) -gravity northwest -geometry +40+60 -compose over -composite \
  \( peony-bloom.webp -resize 330x -background none -rotate -15 \) -gravity southeast -geometry +95+20 -compose over -composite \
  \( dapple.webp -resize 700x -channel A -evaluate multiply 0.35 +channel \) -gravity northeast -geometry +0-160 -compose over -composite \
  -quality 86 -strip og-2411.jpg
