> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:14 p.m.
>
> **Official challenge:** Hidden Frequencies · **Category:** Miscellaneous · **Difficulty:** Hard · **Points:** 550 · **Solves:** 93
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Hidden Frequencies — Write-up

## Challenge

- **Category:** Miscellaneous
- **Target:** `http://2.31.70.16:8120/`
- **Flag format:** `ctf7{...}`

## Enumeration

Opening the target revealed a directory listing containing one file:

```text
recording.wav
```

The WAV file was downloaded for analysis.

## Audio Analysis

The recording is 9 seconds long, mono, and sampled at 44.1 kHz. A normal waveform view and a default spectrogram mainly show an ambient tone around 3200 Hz, but a closer time-frequency analysis reveals short tones at regular intervals.

The hidden tones use frequencies in 200 Hz increments:

```text
2000 Hz, 2200 Hz, 2400 Hz, ..., 5000 Hz
```

Each frequency maps to a hexadecimal digit using:

```text
hex_digit = (frequency - 2000) / 200
```

For example:

```text
2000 Hz -> 0
2200 Hz -> 1
2600 Hz -> 3
3200 Hz -> 6
3400 Hz -> 7
5000 Hz -> f
```

The tones were classified in 150 ms windows using a frequency correlation/FFT-style measurement. The resulting hexadecimal sequence was:

```text
637466377b6672337175336e63795f64306d34316e5f733363723374737d
```

## Decoding

Hex-decoding the sequence gives:

```text
ctf7{fr3qu3ncy_d0m41n_s3cr3ts}
```

## Flag

```text
ctf7{fr3qu3ncy_d0m41n_s3cr3ts}
```
