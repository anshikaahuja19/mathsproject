"""
Split one continuous voice recording (Code/my_voice/full.m4a) into one clip
per narration line (Code/my_voice/<key>.wav), so the scenes can use it.

How the recording was made: every line of NARRATION_SCRIPT.md read in order,
with a ~3 second pause between lines.

    .venv/bin/python Code/split_recording.py            # split + report
    TEMPO=1.0 .venv/bin/python Code/split_recording.py  # keep natural speed

Steps
  1. find pauses >= 1.2 s  -> speech chunks
  2. join chunks listed in MERGE (a mid-line pause that looked like a gap)
  3. check the chunk count equals the number of narration lines
  4. per clip: shorten long pauses inside the line, speed up by TEMPO
     (pitch is preserved), save as WAV
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from narration import N  # noqa: E402

SRC = HERE / "my_voice" / "full.m4a"
OUT = HERE / "my_voice"
GAP = 1.2          # a pause at least this long separates two lines
NOISE = "-35dB"    # level below which audio counts as silence
TEMPO = float(__import__("os").environ.get("TEMPO", "1.2"))
# Chunk 26 ("Bottom right:") + chunk 27 (rest of the line) form line m8c
MERGE = [(26, 27)]


def silences(path):
    log = subprocess.run(["ffmpeg", "-i", str(path), "-af",
                          f"silencedetect=noise={NOISE}:d={GAP}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(starts, ends))


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout)


def main():
    total = duration(SRC)
    chunks, prev = [], 0.0
    for s, e in silences(SRC):
        if s - prev > 0.2:
            chunks.append([prev, s])
        prev = e
    if total - prev > 0.2:
        chunks.append([prev, total])

    for a, b in sorted(MERGE, reverse=True):
        chunks[a][1] = chunks[b][1]
        del chunks[b]

    keys = list(N)
    if len(chunks) != len(keys):
        sys.exit(f"Found {len(chunks)} chunks but the script has {len(keys)} lines. "
                 "Check the pauses between lines / the MERGE list.")

    tighten = ("silenceremove=stop_periods=-1:stop_duration=0.45:"
               f"stop_threshold=-40dB:stop_silence=0.35,atempo={TEMPO}")
    print(f"{'line':6s} {'from':>7s} {'to':>7s} {'raw':>6s} {'final':>6s}")
    raw_sum = fin_sum = 0
    for key, (a, b) in zip(keys, chunks):
        out = OUT / f"{key}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(a - 0.15, 0):.2f}",
                        "-to", f"{b + 0.25:.2f}", "-i", str(SRC), "-af", tighten,
                        "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(out)], check=True)
        d = duration(out)
        raw_sum += b - a
        fin_sum += d
        print(f"{key:6s} {a:7.1f} {b:7.1f} {b - a:6.1f} {d:6.1f}")
    print(f"\nspeech: {raw_sum:.0f}s raw -> {fin_sum:.0f}s after tightening (tempo {TEMPO})")


if __name__ == "__main__":
    main()
