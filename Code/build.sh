#!/usr/bin/env bash
# Build the final 1080p video:  ./Code/build.sh
# Requires: manim (pip install -r Code/requirements.txt), ffmpeg, macOS `say`.
set -euo pipefail
cd "$(dirname "$0")/.."

MANIM=${MANIM:-manim}
PY=${PY:-python3}
[ -x .venv/bin/manim ] && MANIM=.venv/bin/manim && PY=.venv/bin/python

SCENES=(Title WhatIsMatrix MatrixAsTransform Addition ScalarMultiplication
        MatrixVector MatrixMatrix Summary)
OUT_DIR=media/videos/scenes/1080p30
FINAL=Matrices_Video.mp4

"$PY" Code/verify_math.py

"$MANIM" render --resolution 1920,1080 --frame_rate 30 --disable_caching \
         Code/scenes.py "${SCENES[@]}"

# Concatenate in order, re-encoding to a single clean H.264/AAC file
inputs=(); filter=""
for i in "${!SCENES[@]}"; do
  inputs+=(-i "$OUT_DIR/${SCENES[$i]}.mp4")
  filter+="[$i:v][$i:a]"
done
filter+="concat=n=${#SCENES[@]}:v=1:a=1[v][a];[a]loudnorm=I=-16:TP=-1.5[an]"

ffmpeg -y -v error "${inputs[@]}" -filter_complex "$filter" \
       -map "[v]" -map "[an]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
       -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$FINAL"

echo "Built $FINAL ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL") s)"
