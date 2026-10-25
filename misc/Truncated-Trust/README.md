# Truncated Trust

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-Miscellaneous-7A5A12?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-600-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-91-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

Our session-key generator is a simple, fully-documented linear congruential generator (LCG): `state[i+1] = (a * state[i] + c) mod m`, with publicly known `m`, `a`, and `c`. Nothing about the algorithm is secret — only the internal state is.

A debug log accidentally leaked 8 consecutive outputs from a live session — but only the top 24 bits of each 64-bit state. The flag was encrypted with the very next (unleaked) state as a key. Download the leaked data and see if 24 out of every 64 bits is really enough to keep the rest secret.

**Attachment:** [`data.json`](attachments/data.json) · [`README.txt`](attachments/README.txt) · [`script.py`](attachments/script.py)

## Flag

```text
ctf7{trunc4t3d_lcg_l4tt1c3_r3c0v3ry}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** the only unknown is the low 40 bits of the seed; eight truncated states become a closest-vector problem, LLL + Babai recovers the seed, and `state[8]` decrypts the flag.

- `m`, `a`, and `c` are public; `state[0]` is the only secret.
- Eight leaked values give the top 24 bits of `state[0..7]`.
- Lattice reduction recovers the low 40 bits, hence `state[8]`.
- The SHA-256 keystream uses `state[8]` as a big-endian key and a 4-byte big-endian counter starting at 0.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/data.json`](attachments/data.json) | LCG parameters, 8 truncated outputs, ciphertext |
| [`attachments/README.txt`](attachments/README.txt) | Original challenge notes |
| [`attachments/script.py`](attachments/script.py) | Z3 reference model (slow, requires `z3`) |
| [`solve/solve.py`](solve/solve.py) | Pure-stdlib LLL + Babai solver |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output:

```text
[+] state[0] = 0x51c9b7eb4157371c
[+] state[8] = 0x1a664328ca81141c
[+] FLAG: ctf7{trunc4t3d_lcg_l4tt1c3_r3c0v3ry}  (counter: 4-byte big, start 0)
```

## Notes

- The recovered flag uses the lowercase `ctf7{...}` format, not the event-wide `CREST{...}` format.
- The provided `script.py` models the same constraints with Z3 bit-vectors. It is a useful cross-check but much slower than the lattice solver.
- The counter encoding is not specified in `README.txt`; the solver tries common widths, endiannesses, and start values. Only 4-byte big-endian starting at 0 decrypts cleanly.

---

[← Back to Miscellaneous](../README.md) · [All writeups](../../README.md)
