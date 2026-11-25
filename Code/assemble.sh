#!/usr/bin/env bash
# Join the rendered scenes and mix in the background music -> Matrices_Video.mp4
# (called by build.sh; run it on its own to change the music without re-rendering)
#
#   ./Code/assemble.sh                       # piano at the default level
#   MUSIC_VOL=0.03 ./Code/assemble.sh        # quieter music (0 = no music)
#   MUSIC_STYLE=rhodes ./Code/assemble.sh    # piano | rhodes | airy | pad
set -euo pipefail
cd "$(dirname "$0")/.."

PY=${PY:-python3}
[ -x .venv/bin/python ] && PY=.venv/bin/python

SCENES=(Title WhatIsMatrix MatrixAsTransform Addition ScalarMultiplication
        MatrixVector MatrixMatrix Summary)
OUT_DIR=media/videos/scenes/1080p30
VOICE_ONLY=media/voice_only.mp4
FINAL=Matrices_Video.mp4
export MUSIC_STYLE=${MUSIC_STYLE:-piano}
MUSIC_VOL=${MUSIC_VOL:-0.05}

# 1. Concatenate the scenes in order (narration-only audio, loudness-normalised)
inputs=(); filter=""
for i in "${!SCENES[@]}"; do
  inputs+=(-i "$OUT_DIR/${SCENES[$i]}.mp4")
  filter+="[$i:v][$i:a]"
done
filter+="concat=n=${#SCENES[@]}:v=1:a=1[v][a];[a]loudnorm=I=-16:TP=-1.5[an]"
ffmpeg -y -v error "${inputs[@]}" -filter_complex "$filter" \
       -map "[v]" -map "[an]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
       -c:a aac -b:a 192k -ar 48000 "$VOICE_ONLY"

# 2. Background music: original track generated in code, at one constant,
#    low level well beneath the narration (no ducking/pumping)
LEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE_ONLY")
"$PY" Code/make_music.py "$LEN"
ffmpeg -y -v error -i "$VOICE_ONLY" -i Code/music/background.wav -filter_complex \
  "[1:a]volume=${MUSIC_VOL}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$FINAL"

echo "Built $FINAL ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL") s)"
