"""
Helper module for the M3 animation video "Matrices & Matrix Operations".

Contents
--------
* Colour palette (used consistently across every scene)
* `Mat`      – a LaTeX-free matrix mobject built from Text + drawn brackets,
               with easy access to rows, columns and single entries.
* `tts`      – generates narration audio with the macOS `say` voice (cached).
* `NarratedScene` – a Scene subclass with a `voice(...)` context manager that
               plays a narration clip and keeps the animation in sync with it.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import wave
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

# --------------------------------------------------------------------------
# Student details (shown on the opening frame). Set via environment
# variables or edit here.
# --------------------------------------------------------------------------
STUDENT_NAME = os.environ.get("STUDENT_NAME", "Anshika Ahuja")
STUDENT_ID = os.environ.get("STUDENT_ID", "E25B070780")

# --------------------------------------------------------------------------
# Visual style
# --------------------------------------------------------------------------
BG = "#101418"
PROSE_FONT = "Avenir Next"     # headings / sentences
MATH_FONT = "Times New Roman"  # numbers, symbols, formulas

COL_A = "#58C4DD"        # matrix A (January sales)  – blue
COL_B = "#83C167"        # matrix B (February sales) – green
COL_SUM = "#FFFFFF"      # results
COL_SCALAR = "#FFD54F"   # scalars                   – yellow
COL_PRICE = "#FF8A65"    # price vector p             – orange
COL_ROW = "#FFD54F"      # row highlight             – yellow
COL_COL = "#F06292"      # column highlight          – pink
COL_DIM = "#B39DDB"      # dimensions m×n            – purple
COL_I = "#83C167"        # i-hat                     – green
COL_J = "#F06292"        # j-hat                     – pink
COL_V = "#FFD54F"        # general vector v           – yellow
COL_P = "#58C4DD"        # matrix P
COL_Q = "#FF8A65"        # matrix Q
GREY = "#8A939C"

config.background_color = BG

MINUS = "−"  # proper minus sign


def fmt(x) -> str:
    """Format a number for display, using a true minus sign."""
    if isinstance(x, str):
        return x
    if float(x).is_integer():
        x = int(x)
    s = str(x)
    return s.replace("-", MINUS)


def prose(text, size=34, color=WHITE, **kw):
    return Text(text, font=PROSE_FONT, font_size=size, color=color, **kw)


def math(markup, size=40, color=WHITE, **kw):
    """Pango-markup maths, e.g. math('a<sub>ij</sub>')."""
    return MarkupText(markup, font=MATH_FONT, font_size=size, color=color, **kw)


def title_bar(text, color=WHITE):
    t = prose(text, size=40, color=color, weight=BOLD)
    t.to_edge(UP, buff=0.45)
    line = Line(LEFT, RIGHT, color=GREY, stroke_width=2)
    line.set_width(config.frame_width - 1.2).next_to(t, DOWN, buff=0.2)
    return VGroup(t, line)


# --------------------------------------------------------------------------
# Matrix mobject (no LaTeX needed)
# --------------------------------------------------------------------------
class Mat(VGroup):
    """A matrix drawn with Text entries and square brackets.

    >>> A = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A)
    >>> A.entry(1, 2)   # 0-indexed: row 2, column 3 in maths notation
    """

    def __init__(self, rows, color=WHITE, font_size=44, col_gap=0.55,
                 row_gap=0.32, bracket_color=None, bracket_pad=0.18, **kw):
        super().__init__(**kw)
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])
        cells = [[Text(fmt(v), font=MATH_FONT, font_size=font_size, color=color)
                  for v in row] for row in rows]
        cw = max(c.width for row in cells for c in row)
        ch = max(c.height for row in cells for c in row)
        for i, row in enumerate(cells):
            for j, c in enumerate(row):
                c.move_to(np.array([j * (cw + col_gap), -i * (ch + row_gap), 0]))
        self.cells = cells
        self.entries = VGroup(*[c for row in cells for c in row])
        self.entries.move_to(ORIGIN)

        h = self.entries.height + 2 * bracket_pad + 0.1
        tick = 0.14
        bc = bracket_color or GREY
        top = self.entries.get_top()[1] + bracket_pad + 0.05
        bot = top - h
        xl = self.entries.get_left()[0] - bracket_pad - 0.05
        xr = self.entries.get_right()[0] + bracket_pad + 0.05
        lb = VMobject(stroke_color=bc, stroke_width=3).set_points_as_corners(
            [[xl + tick, top, 0], [xl, top, 0], [xl, bot, 0], [xl + tick, bot, 0]])
        rb = VMobject(stroke_color=bc, stroke_width=3).set_points_as_corners(
            [[xr - tick, top, 0], [xr, top, 0], [xr, bot, 0], [xr - tick, bot, 0]])
        self.brackets = VGroup(lb, rb)
        self.add(self.brackets, self.entries)

    def entry(self, i, j):
        return self.cells[i][j]

    def row(self, i):
        return VGroup(*self.cells[i])

    def col(self, j):
        return VGroup(*[r[j] for r in self.cells])

    def row_box(self, i, color=COL_ROW, buff=0.12):
        return SurroundingRectangle(self.row(i), color=color, buff=buff,
                                    corner_radius=0.08, stroke_width=3)

    def col_box(self, j, color=COL_COL, buff=0.12):
        return SurroundingRectangle(self.col(j), color=color, buff=buff,
                                    corner_radius=0.08, stroke_width=3)

    def entry_box(self, i, j, color=COL_ROW, buff=0.1):
        return SurroundingRectangle(self.entry(i, j), color=color, buff=buff,
                                    corner_radius=0.06, stroke_width=3)


def labelled(mat: Mat, name: str, color, size=44):
    """Return VGroup(name_label, '=', mat) laid out left-to-right."""
    lab = math(f"<i>{name}</i>", size=size, color=color)
    eq = math("=", size=size)
    return VGroup(lab, eq, mat).arrange(RIGHT, buff=0.25)


# --------------------------------------------------------------------------
# Narration (macOS text-to-speech, cached to Code/voice/)
# --------------------------------------------------------------------------
VOICE_DIR = Path(__file__).resolve().parent / "voice"
VOICE = os.environ.get("TTS_VOICE", "Samantha")
RATE = int(os.environ.get("TTS_RATE", "185"))


def tts(text: str) -> tuple[str, float]:
    VOICE_DIR.mkdir(exist_ok=True)
    key = hashlib.md5(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:12]
    path = VOICE_DIR / f"{key}.wav"
    if not path.exists():
        subprocess.run(["say", "-v", VOICE, "-r", str(RATE), "-o", str(path),
                        "--file-format=WAVE", "--data-format=LEI16@44100", text],
                       check=True)
    with wave.open(str(path)) as w:
        dur = w.getnframes() / w.getframerate()
    return str(path), dur


class _Voice:
    def __init__(self, scene, text, pause):
        self.scene, self.text, self.pause = scene, text, pause

    def __enter__(self):
        path, self.duration = tts(self.text)
        self.scene.add_sound(path)
        self.start = self.scene.renderer.time
        return self

    def __exit__(self, *exc):
        elapsed = self.scene.renderer.time - self.start
        remaining = self.duration - elapsed
        if remaining < -0.5:
            print(f"[sync] animations overran narration by {-remaining:.1f}s: "
                  f"{self.text[:50]!r}")
        self.scene.wait(max(remaining, 0) + self.pause)
        return False


class NarratedScene(Scene):
    """Scene whose `voice()` blocks keep visuals in step with narration."""

    def voice(self, text: str, pause: float = 0.25):
        return _Voice(self, text, pause)
