# Biased Signatures

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Cryptography-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-600-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-90-1F5F73?style=flat-square)

> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:38 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

A signing service rolled out a "faster" nonce generator for its ECDSA (secp256k1) signatures. Performance went up. Something else went down. We captured the service's public key and a handful of signatures it produced, along with a flag encrypted under its private key. Can you recover the key?

**Flag format:** `ctf7{...}`

**Attachments:** No downloadable attachment: the `readme.txt` parameters and the signature set are quoted in the writeup, and the service endpoint is offline.

**Targets (offline after the event):** `http://2.31.70.16:8050/`

## Flag

```text
ctf7{3cds4_n0nc3_b14s_l34ks_k3y}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

ECDSA with the top 56 nonce bits forced to zero; the hidden-number problem recovers the private key.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The challenge's public parameter block is reproduced in the writeup (`readme.txt` in the original service).
- The flag prefix is lowercase `ctf7{...}` even though the challenge is in the CREST event.
- The service endpoint was taken down after the event; no live solver is possible.

## Run the solver

No standalone solver is archived. The author's referenced `work/solve.py` was not included in the submitted files; the writeup contains the parameter block, the signature records, and the lattice recipe.

---

[← Back to Cryptography](../README.md) · [All writeups](../../README.md)
