#!/bin/bash
# bake-cotton.sh, run from the page dir: a seamless tile of cream cotton paper for the page backdrop.
# Blurs wrap around the edges (virtual-pixel tile), so the tile repeats without seams.
set -e
T=/tmp/pw/cotton; mkdir -p $T; S=1024
# soft mottling of the pulp
magick -size ${S}x${S} xc:gray50 -seed 7 +noise Random -colorspace gray -virtual-pixel tile -blur 0x40 -auto-level -level 30%,70% $T/mottle.png
# short fibres: noise streaked in two directions
magick -size ${S}x${S} xc:gray50 -seed 11 +noise Random -colorspace gray -virtual-pixel tile -motion-blur 0x7+20 -auto-level -level 35%,65% $T/f1.png
magick -size ${S}x${S} xc:gray50 -seed 13 +noise Random -colorspace gray -virtual-pixel tile -motion-blur 0x7+115 -auto-level -level 35%,65% $T/f2.png
# fine tooth
magick -size ${S}x${S} xc:gray50 -seed 17 +noise Random -colorspace gray -virtual-pixel tile -blur 0x0.7 -auto-level $T/tooth.png
# mix, then darken the cream by up to 7% where the mix is dark
magick $T/mottle.png $T/f1.png $T/f2.png $T/tooth.png -evaluate-sequence mean -auto-level $T/mix.png
magick -size ${S}x${S} xc:'#ede6d9' \( $T/mix.png +level 93%,100% \) -compose multiply -composite -quality 86 assets/cotton.webp
magick identify -format "%f %wx%h %b\n" assets/cotton.webp
