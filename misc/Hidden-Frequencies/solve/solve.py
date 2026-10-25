#!/usr/bin/env python3
"""Decode Hidden Frequencies by peak-picking 150 ms windows."""
from pathlib import Path
import wave

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
wav_path = ROOT / "attachments" / "recording.wav"

with wave.open(str(wav_path), "rb") as wav:
    sample_rate = wav.getframerate()
    channels = wav.getnchannels()
    width = wav.getsampwidth()
    raw = wav.readframes(wav.getnframes())

if channels != 1 or width != 2:
    raise SystemExit("expected mono 16-bit PCM")
samples = np.frombuffer(raw, dtype="<i2").astype(np.float64)
window = int(sample_rate * 0.15)
digits = []
for start in range(0, len(samples) - window + 1, window):
    segment = samples[start:start + window] * np.hanning(window)
    spectrum = np.abs(np.fft.rfft(segment))
    freqs = np.fft.rfftfreq(window, 1 / sample_rate)
    band = (freqs >= 1900) & (freqs <= 5100)
    peak = freqs[band][np.argmax(spectrum[band])]
    digit = round((peak - 2000) / 200)
    if 0 <= digit <= 15:
        digits.append(format(digit, "x"))

hex_string = "".join(digits)
flag = bytes.fromhex(hex_string).decode()
print("[*] windows:", len(digits), "hex:", hex_string)
print("[+] FLAG:", flag)
