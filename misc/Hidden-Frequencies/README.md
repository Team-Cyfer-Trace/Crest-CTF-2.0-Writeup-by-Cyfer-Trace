# Hidden Frequencies

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Miscellaneous-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-550-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-93-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:14 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

We intercepted this audio recording during a routine sweep. It sounds like nothing much — some ambient tone in the background — but something about its frequency content seems off. Amplitude waveforms and a default spectrogram render won't get you far here; you'll need to look closer, and more precisely, than that.

**Flag format:** `ctf7{...}`

**Attachments:** [`recording.wav`](attachments/recording.wav)

**Targets (offline after the event):** `http://2.31.70.16:8120/`

## Flag

```text
ctf7{fr3qu3ncy_d0m41n_s3cr3ts}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A 9-second WAV hides hex digits as 200 Hz-spaced tones in 150 ms windows.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/recording.wav` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested peak-picking decoder; prints the recovered hex and flag. |
| `solve/requirements.txt` | Python dependencies for the archived solver. |

## Notes

- The original target was a directory listing containing `recording.wav`; the file is archived here.
- The solver uses 150 ms windows and maps `(frequency - 2000) / 200` to a hex digit.

## Run the solver

Install the solver dependencies first:

```bash
cd solve
python -m pip install -r requirements.txt
```

Then run it:

```bash
cd solve
python solve.py
```

Expected final line:

```text
[+] FLAG: ctf7{fr3qu3ncy_d0m41n_s3cr3ts}
```

---

[← Back to Miscellaneous](../README.md) · [All writeups](../../README.md)
