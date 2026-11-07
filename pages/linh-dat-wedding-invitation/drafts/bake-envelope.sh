#!/bin/bash
# bake-envelope.sh, run from the page dir: bakes the CSS paper-lift and shadows into the envelope,
# seal and monogram images (sources in drafts/src), so nothing is filtered while the page scrolls.
set -e
U=drafts/src/unbaked; T=/tmp/pw/bake; mkdir -p $T
LIFT="-channel RGB -function polynomial 1.0608,-0.01 +channel"   # brightness(1.04) contrast(1.02)
shadowed() { # SRC OUT PAD SHADOWS...
  local SRC=$1 OUT=$2 P=$3; shift 3
  magick $SRC $LIFT -bordercolor none -border $P $T/padded.png
  local args=()
  for s in "$@"; do args+=( \( $T/padded.png -background 'rgb(30,20,12)' -shadow $s \) ); done
  # flatten onto a canvas the size of the padded image, so the picture keeps its place
  magick -size $(magick identify -format %wx%h $T/padded.png) xc:none "${args[@]}" $T/padded.png \
    -background none -flatten -quality 85 $OUT
  magick identify -format "%f %wx%h %b\n" $OUT
}
# envelope: 900px image shown ~335px wide, so the CSS shadows are scaled ~2.7x (as bake-sheet.sh)
ENV=("30x14+11+48" "22x6+3+11" "35x1.4+1+3")
shadowed $U/envelope-closed.webp assets/envelope-closed.webp 110 "${ENV[@]}"
shadowed $U/envelope-open.webp assets/envelope-open.webp 110 "${ENV[@]}"
magick $U/envelope-pocket.webp $LIFT -quality 85 assets/envelope-pocket.webp
# seal: 320px shown ~70px wide; CSS drop-shadow(0 2px 2px / .3)
shadowed $U/seal.webp assets/seal.webp 24 "30x4.5+0+10"
# monogram: wine ink over a 70% white hairline 1px (13px here) below it
magick -size 600x614 xc:none \
  \( drafts/src/monogram.webp -alpha extract -background white -alpha shape -channel A -evaluate multiply 0.7 +channel \) -geometry +0+13 -composite \
  \( drafts/src/monogram.webp -alpha extract -background '#6e1a26' -alpha shape \) -geometry +0+0 -composite -quality 90 assets/monogram-wine.webp
# photo thumbnails: the prints' matt, faded tone, CSS contrast(0.94) saturate(0.9) brightness(1.02)
for f in drafts/src/unbaked/photos/*-s.webp; do
  magick "$f" -channel RGB -function polynomial 0.94,0.03 +channel \
    -color-matrix "0.9213 0.0715 0.0072  0.0213 0.9715 0.0072  0.0213 0.0715 0.9285" \
    -channel RGB -evaluate multiply 1.02 +channel -quality 82 assets/photos/$(basename "$f")
done
