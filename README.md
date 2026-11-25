# M3 Animation Video — Matrices & Matrix Operations

**Concept:** What does a matrix represent? Dimensions, entry meanings, addition, scalar multiplication and matrix multiplication.
**Student:** Anshika Ahuja · **Student ID:** E25B070780

| Deliverable | File |
|---|---|
| Final video (1080p, 16:9, 6:32) | [`Matrices_Video.mp4`](Matrices_Video.mp4) |
| Animation source code | [`Code/`](Code/) |
| Narration script | [`Code/NARRATION_SCRIPT.md`](Code/NARRATION_SCRIPT.md) |
| Storyboard | see below |

## Storyboard

| # | Scene (`Code/scenes.py`) | What it teaches |
|---|---|---|
| 1 | `Title` | Opening frame: title, concept, name and ID |
| 2 | `WhatIsMatrix` | A table of sales data becomes matrix *A*; rows = shops, columns = items; *A* is 2 × 3 (rows × columns); notation *a<sub>ij</sub>*, with *a*<sub>23</sub> = 6 and *a*<sub>12</sub> = 5 interpreted |
| 3 | `MatrixAsTransform` | A 2 × 2 matrix *T* transforms the plane: its columns are where î and ĵ land; *T*(1, 2) = 1·(2, 0) + 2·(1, 1) = (4, 2) |
| 4 | `Addition` | January + February sales, added entry by entry; (*A*+*B*)<sub>ij</sub> = *a*<sub>ij</sub> + *b*<sub>ij</sub>; 2 × 3 + 2 × 2 is undefined |
| 5 | `ScalarMultiplication` | 2*A* doubles every entry; (*cA*)<sub>ij</sub> = *c*·*a*<sub>ij</sub>; geometrically, 2**v** stretches a vector and −**v** flips it |
| 6 | `MatrixVector` | Quantities × prices = revenue: *A***p** = (140, 90); row · column (dot product); (*m*×*n*)(*n*×*k*) → *m*×*k* |
| 7 | `MatrixMatrix` | *PQ* worked entry by entry; *QP* ≠ *PQ*; (*PQ*)**x** = *P*(*Q***x**), so the order of transformations matters |
| 8 | `Summary` | Recap, followed by the closing frame with credits and AI disclosure |

**Colour coding (consistent throughout):** blue = *A* / *P*; green = *B* / î; orange = prices **p** / *Q*; yellow = scalars, rows and **v**; pink = columns / ĵ; purple = dimensions.

## Worked examples (verified)

```
A = [3 5 2; 4 1 6]   B = [2 3 1; 5 2 0]   p = [10; 20; 5]
A + B = [5 8 3; 9 3 6]     2A = [6 10 4; 8 2 12]     Ap = [140; 90]
P = [2 0; 1 3]   Q = [1 4; 2 −1]   PQ = [2 8; 7 1]   QP = [6 12; 3 −3]
T = [2 1; 0 1]   T(1,2) = (4,2)
```
`python Code/verify_math.py` checks every number above with NumPy. All of them were also recalculated by hand.

## How to rebuild the video

Requirements: macOS, Python 3.13, `brew install pango pkg-config ffmpeg`.

```bash
python3.13 -m venv .venv && .venv/bin/pip install -r Code/requirements.txt
.venv/bin/python Code/split_recording.py   # cut my recording into one clip per line
./Code/build.sh      # renders all scenes at 1080p, outputs Matrices_Video.mp4
MUSIC_VOL=0.03 ./Code/assemble.sh   # change only the music (style/volume), no re-render
.venv/bin/manim -pql Code/scenes.py Addition   # quick preview of one scene
```

`Code/helpers.py` contains the LaTeX-free matrix object (`Mat`) and the `NarratedScene.voice()` helper. Each narration clip is generated first, and the scene waits for its exact length, so the audio and visuals stay in sync.

## Credits & AI disclosure

- **Animation:** [Manim Community](https://www.manim.community/) v0.22.1 (Python)
- **Narration:** voiced by Anshika Ahuja (recorded in one take, `Code/my_voice/full.m4a`; split into lines with `Code/split_recording.py`, long pauses shortened and played at 1.2× speed with pitch unchanged)
- **Music:** original soft piano track generated with `Code/make_music.py` (NumPy/SciPy), mixed at a constant low level under the narration
- **AI tools used:** Claude (Anthropic) helped draft the script, the storyboard and the Manim/Python code. Every equation and calculation was checked independently by hand and with `Code/verify_math.py`.
