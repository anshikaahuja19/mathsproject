"""
Generate an original, royalty-free background track with NumPy/SciPy.

    .venv/bin/python Code/make_music.py 400                 # length in seconds
    MUSIC_STYLE=piano .venv/bin/python Code/make_music.py 400

Styles (all steady, no drums, low-passed to stay out of the voice range):
  pad    – warm sustained synth pad, C – Am – F – G
  piano  – soft, sparse piano chords, Cmaj7 – Am7 – Fmaj7 – G6
  rhodes – mellow electric piano with gentle tremolo (lo-fi feel), D – Bm – G – A
  airy   – high, breathy shimmer pad, E – C#m – A – B

Writes Code/music/background.wav (44.1 kHz stereo). Mixed at a constant low
level under the narration by Code/build.sh.
"""
import os
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import lfilter

SR = 44100
OUT = Path(__file__).resolve().parent / "music" / "background.wav"
STYLE = os.environ.get("MUSIC_STYLE", "piano")
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, cutoff, passes=2):
    a = np.exp(-2 * np.pi * cutoff / SR)
    for _ in range(passes):
        x = lfilter([1 - a], [1, -a], x)
    return x


def tvec(dur):
    return np.arange(int(dur * SR)) / SR


# ---------------------------------------------------------------- instruments
def pad_note(f, dur, fade=3.0):
    t = tvec(dur)
    sig = sum(np.sin(2 * np.pi * f * d * t + p) for d, p in ((1, 0), (1.003, 1.1), (0.997, 2.3)))
    sig += 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return sig * np.minimum(1, t / fade) * np.minimum(1, (dur - t) / fade) / 4


def piano_note(f, dur=5.0):
    t = tvec(dur)
    sig = np.zeros_like(t)
    for k in range(1, 8):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)          # slight string inharmonicity
        sig += np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.6 + 0.9 * k)) / k ** 1.3
    return sig * np.minimum(1, t / 0.006)


def rhodes_note(f, dur=4.0):
    t = tvec(dur)
    index = 1.6 * np.exp(-t * 3)                          # bell-like attack that fades
    sig = np.sin(2 * np.pi * f * t + index * np.sin(2 * np.pi * f * t))
    return sig * np.minimum(1, t / 0.01) * np.exp(-t * 0.9)


# ---------------------------------------------------------------- arrangements
def render(length):
    n = int(length * SR) + SR * 20
    L = np.zeros(n)
    R = np.zeros(n)

    def put(sig, at, pan=0.5, gain=1.0):
        s = int(at * SR)
        e = min(s + len(sig), n)
        L[s:e] += sig[:e - s] * gain * (1 - pan) * 2
        R[s:e] += sig[:e - s] * gain * pan * 2

    if STYLE == "pad":
        chords = [[48, 55, 60, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]]
        step = 2 * 4 * 60 / 70
        for i, at in enumerate(np.arange(0, length, step)):
            for m in chords[i % 4]:
                put(pad_note(hz(m), step + 3), at, 0.5 + (0.08 if m % 2 else -0.08))
        cutoff = 900

    elif STYLE == "piano":
        chords = [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 52, 59]]
        beat = 60 / 66
        for i, at in enumerate(np.arange(0, length, 4 * beat)):
            notes = chords[i % 4]
            for j, m in enumerate(notes):                # soft rolled chord on beat 1
                put(piano_note(hz(m), 6), at + j * 0.035, 0.3 + 0.13 * j, 0.5)
            put(piano_note(hz(notes[-1] + 12), 4), at + 2 * beat, 0.6, 0.18)   # gentle echo note
        cutoff = 1800

    elif STYLE == "rhodes":
        chords = [[50, 57, 61, 66], [47, 54, 57, 62], [43, 50, 54, 59], [45, 52, 55, 61]]
        beat = 60 / 72
        for i, at in enumerate(np.arange(0, length, 4 * beat)):
            for j, m in enumerate(chords[i % 4]):
                put(rhodes_note(hz(m), 5), at, 0.35 + 0.1 * j, 0.45)
                put(rhodes_note(hz(m), 3), at + 2.5 * beat, 0.65 - 0.1 * j, 0.2)
        t = np.arange(n) / SR
        trem = 1 - 0.25 * (0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t))
        L *= trem
        R *= np.roll(trem, int(SR * 0.06))
        cutoff = 1500

    elif STYLE == "airy":
        chords = [[64, 71, 76, 80], [61, 68, 73, 76], [57, 64, 69, 73], [59, 66, 71, 75]]
        step = 8.0
        for i, at in enumerate(np.arange(0, length, step)):
            for m in chords[i % 4]:
                put(pad_note(hz(m), step + 4, fade=4), at, 0.5 + (0.15 if m % 2 else -0.15), 0.6)
        breath = lowpass(rng.standard_normal(n), 2500) * 0.08   # soft airy noise bed
        swell = 0.6 + 0.4 * np.sin(2 * np.pi * np.arange(n) / SR / 16)
        L += breath * swell
        R += np.roll(breath, SR // 3) * swell
        cutoff = 3000

    else:
        sys.exit(f"Unknown MUSIC_STYLE {STYLE!r}")

    L, R = lowpass(L, cutoff), lowpass(R, cutoff)
    return np.stack([L, R], axis=1)


def main(length):
    n = int(length * SR)
    mix = render(length)[:n]
    fade_in = np.minimum(1, np.arange(n) / (3 * SR))
    fade_out = np.minimum(1, (n - np.arange(n)) / (5 * SR))
    mix *= (fade_in * fade_out)[:, None]
    # Normalise by loudness (RMS) so every style sits at the same level
    mix *= 0.12 / np.sqrt(np.mean(mix ** 2))
    mix = np.clip(mix, -0.98, 0.98)
    OUT.parent.mkdir(exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    print(f"Wrote {OUT} ({length:.0f}s, style={STYLE})")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 400)
