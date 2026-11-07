#!/bin/bash
# bake-sheet.sh SRC OUT, run from assets/: bake-sheet.sh ../drafts/src/card.webp card-sheet.webp
set -e
SRC=$1; OUT=$2; T=/tmp/pw/bake; mkdir -p $T
W=$(magick identify -format %w $SRC); H=$(magick identify -format %h $SRC)
P=120
# paper colour: most of the warmth out, a touch brighter
magick $SRC -modulate 100,15 -level 0%,91% $T/base.png
# grain tiled at the same scale as on screen (240px tile on a ~330px card ≈ 730px on this image)
magick -size ${W}x${H} tile:../drafts/src/grain.webp -resize 300% -crop ${W}x${H}+0+0 +repage +level 80%,100% $T/grain.png 2>/dev/null || magick ../drafts/src/grain.webp -resize 730x730 -write mpr:g +delete -size ${W}x${H} tile:mpr:g +level 80%,100% $T/grain.png
magick -size ${W}x${H} -define gradient:center=$((W*18/100)),$((H*8/100)) -define gradient:radii=$((W*14/10)),$((H*11/10)) radial-gradient:white-'rgb(247,247,246)' -level 0%,100% $T/light.png
magick $T/base.png \( $T/grain.png $T/light.png -compose multiply -composite \) -compose multiply -composite \( $SRC -alpha extract \) -compose copy-opacity -composite $T/sheet.png
# shadows scaled from the CSS ones by the image/screen ratio (~3x); flatten onto a canvas the size of the padded sheet
magick $T/sheet.png -bordercolor none -border $P $T/padded.png
magick -size $((W+2*P))x$((H+2*P)) xc:none \
  \( $T/padded.png -background 'rgb(30,20,12)' -shadow 30x16+12+54 \) \
  \( $T/padded.png -background 'rgb(30,20,12)' -shadow 22x7+3+12 \) \
  \( $T/padded.png -background 'rgb(30,20,12)' -shadow 35x1.5+1+3 \) \
  $T/padded.png -background none -flatten -quality 82 $OUT
magick identify -format "%f %wx%h %b\n" $OUT
