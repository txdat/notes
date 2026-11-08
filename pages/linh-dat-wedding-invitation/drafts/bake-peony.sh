#!/bin/bash
# bake-peony.sh SPRAY.png BUD.png BLOOM.png, run from the page dir: cuts the Gemini peony shots
# (prompts/09, 10, 11) out of their cobalt backdrop, tones them toward the card's muted palette and
# bakes a soft shadow (light from the upper left), so nothing is filtered on the page.
set -e
T=/tmp/pw/bake; mkdir -p $T drafts/src/unbaked
python3 -I drafts/key-peony.py "$1" drafts/src/unbaked/peony-spray.webp 800
python3 -I drafts/key-peony.py "$2" drafts/src/unbaked/peony-bud.webp 600
python3 -I drafts/key-peony.py "$3" drafts/src/unbaked/peony-bloom.webp 800
TONE="-modulate 103,86,100"   # a little lighter and less saturated, like the prints' faded tone
shadowed() { # SRC OUT PAD ROTATE SHADOWS... (rotated before the shadow, so it still falls down-right)
  local SRC=$1 OUT=$2 P=$3 R=$4; shift 4
  magick $SRC $TONE -background none -rotate $R +repage -bordercolor none -border $P $T/padded.png
  local args=()
  for s in "$@"; do args+=( \( $T/padded.png -background 'rgb(30,20,12)' -shadow $s \) ); done
  magick -size $(magick identify -format %wx%h $T/padded.png) xc:none "${args[@]}" $T/padded.png \
    -background none -flatten -quality 88 $OUT
  magick identify -format "%f %wx%h %b\n" $OUT
}
# ~3.4 image px per CSS px: a close contact shadow and a wider soft one, both down and right
shadowed drafts/src/unbaked/peony-spray.webp assets/peony-spray.webp 60 0 "38x4+3+6" "24x16+10+22"
# the bud lies tilted across the envelope corner
shadowed drafts/src/unbaked/peony-bud.webp assets/peony-bud.webp 60 10 "38x4+3+6" "24x16+10+22"
# the same bud mirrored and its stem cut shorter, for the corner of the time and venue card (page 4)
magick drafts/src/unbaked/peony-bud.webp -gravity north -crop 100%x80%+0+0 +repage -flop $T/bud-flop.png
shadowed $T/bud-flop.png assets/peony-bud-2.webp 60 0 "38x4+3+6" "24x16+10+22"
# one open bloom by the thanks card (last page)
shadowed drafts/src/unbaked/peony-bloom.webp assets/peony-bloom.webp 60 0 "38x4+3+6" "24x16+10+22"
