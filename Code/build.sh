#!/usr/bin/env bash
# Build the final 1080p video:  ./Code/build.sh
# Requires: manim (pip install -r Code/requirements.txt), ffmpeg, macOS `say`.
# To change only the music (no re-render), run ./Code/assemble.sh instead.
set -euo pipefail
cd "$(dirname "$0")/.."

MANIM=${MANIM:-manim}
PY=${PY:-python3}
[ -x .venv/bin/manim ] && MANIM=.venv/bin/manim && PY=.venv/bin/python

SCENES=(Title WhatIsMatrix MatrixAsTransform Addition ScalarMultiplication
        MatrixVector MatrixMatrix Summary)

"$PY" Code/verify_math.py

"$MANIM" render --resolution 1920,1080 --frame_rate 30 --disable_caching \
         Code/scenes.py "${SCENES[@]}"

# Join scenes + add background music (see Code/assemble.sh)
./Code/assemble.sh
