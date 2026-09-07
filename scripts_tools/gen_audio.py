#!/usr/bin/env python3
"""Generate simple sound effects as WAV files for the game.
Reproducible; run from repo root:  python3 scripts_tools/gen_audio.py
"""
import numpy as np, wave, os

SR = 44100
OUT = "assets/audio"

def save(name, data16):
    os.makedirs(OUT, exist_ok=True)
    with wave.open(os.path.join(OUT, name), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data16.tobytes())
    print("wrote", name, round(len(data16) / SR, 2), "s")

def env(n, a=0.01, r=0.2):
    t = np.linspace(0, 1, n, endpoint=False)
    e = np.ones(n)
    ai = max(1, int(a * SR)); ri = max(1, int(r * SR))
    if ai < n: e[:ai] = np.linspace(0, 1, ai)
    if ri < n: e[-ri:] = np.linspace(1, 0, ri)
    return e

def main():
    # --- pickup: bright rising blip ---
    dur = 0.45; n = int(SR * dur); t = np.linspace(0, dur, n, endpoint=False)
    f = 520 + 900 * t / dur
    sig = np.sin(2 * np.pi * f * t) * env(n, 0.01, 0.2)
    save("pickup.wav", (sig * 0.5 * 32767).astype(np.int16))

    # --- caught: harsh descending buzz ---
    dur = 0.5; n = int(SR * dur); t = np.linspace(0, dur, n, endpoint=False)
    f = 260 - 160 * t / dur
    sig = np.sin(2 * np.pi * f * t) * env(n, 0.005, 0.35)
    sig += 0.5 * np.sign(np.sin(2 * np.pi * f * 1.5 * t))
    save("caught.wav", (np.clip(sig, -1, 1) * 0.6 * 32767).astype(np.int16))

    # --- lever click: short two-tone ---
    dur = 0.12; n = int(SR * dur); t = np.linspace(0, dur, n, endpoint=False)
    sig = np.sin(2 * np.pi * 700 * t) * env(n, 0.002, 0.08)
    save("lever.wav", (sig * 0.4 * 32767).astype(np.int16))

    # --- goal: gentle ascending arpeggio ---
    dur = 0.7; n = int(SR * dur); t = np.linspace(0, dur, n, endpoint=False)
    sig = np.zeros(n)
    for i, s in enumerate([0, 4, 7, 12]):
        f0 = 330 * (2 ** (s / 12)); start = int(i * 0.13 * SR)
        if start >= n: continue
        seg = np.zeros(n)
        seg[start:] = np.sin(2 * np.pi * f0 * (t[start:] - start / SR)) * env(n - start, 0.01, 0.18)
        sig += seg
    save("goal.wav", (np.clip(sig, -1, 1) * 0.45 * 32767).astype(np.int16))

    # --- toggle OFF: soft descending ---
    dur = 0.3; n = int(SR * dur); t = np.linspace(0, dur, n, endpoint=False)
    f = 440 - 180 * t / dur
    sig = np.sin(2 * np.pi * f * t) * env(n, 0.01, 0.2)
    save("toggle_off.wav", (sig * 0.4 * 32767).astype(np.int16))

    # --- toggle ON: soft rising ---
    f = 380 + 180 * t / dur
    sig = np.sin(2 * np.pi * f * t) * env(n, 0.01, 0.25)
    save("toggle_on.wav", (sig * 0.4 * 32767).astype(np.int16))

if __name__ == "__main__":
    main()
