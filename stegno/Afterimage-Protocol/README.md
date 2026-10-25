# Afterimage Protocol

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Steganography-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-1000-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-144-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:14 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

At 02:17, Northstar's relay station vanished from the survey network. Case NSR-0217 contains one surviving artifact: a lossless night-survey raster pulled from a retired archive node. Analysts cannot agree whether the raster contains evidence, contamination, or a deliberate dead drop. Download the original artifact from the challenge attachment and recover the proof token. Submit only the final CREST{...} value. Archive metadata and visible flag-shaped strings are not automatically valid evidence. Custody warning: work on a copy of the exact downloaded PNG. Re-saving, optimizing, or converting it can permanently destroy evidence. Attachment: STEG-01-Afterimage-Protocol.zip (contains afterimage.png)

**Flag format:** `CREST{...}`

**Attachments:** [`afterimage.png`](attachments/afterimage.png)

## Flag

```text
CREST{f1lt3rs_b3f0r3_p1x3ls_9f42d8e1}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

PNG row-filter bytes and a PCG-selected pixel pool hide the final layer; metadata and visible flags are decoys.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/afterimage.png` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested final-layer decoder for the original PNG. |
| `solve/requirements.txt` | Python dependencies for the archived solver. |

## Notes

- The PNG must be the exact downloaded artifact; re-saving or converting it can destroy the row-filter layer.
- The solver reproduces the final layer from the image and the constants recovered in the writeup; intermediate exploration scripts are not needed.

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
[+] FLAG: CREST{f1lt3rs_b3f0r3_p1x3ls_9f42d8e1}
```

---

[← Back to Steganography](../README.md) · [All writeups](../../README.md)
