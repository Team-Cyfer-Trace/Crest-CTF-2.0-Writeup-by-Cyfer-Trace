# Latchkey

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Reverse_Engineering-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Medium-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-250-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-220-1F5F73?style=flat-square)

> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:03 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

A small access-control binary. Give it a string; it tells you "Access granted." or "Access denied." — nothing else. No usable strings, no helpful errors. Work out HOW it decides, not WHAT. Submit the accepted CREST{...} string. Attachment: latchkey (x86-64 ELF, statically linked, stripped)

**Flag format:** `CREST{...}`

**Attachments:** [`latchkey`](attachments/latchkey)

## Flag

```text
CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Two XOR-shared transition tables encode a DFA; a breadth-first search recovers the accepting string.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `source-writeup.docx` | Original author-formatted Word writeup, preserved unchanged. |
| `attachments/latchkey` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested BFS over the XOR-reconstructed DFA. |

## Notes

- The author's original Word writeup is preserved as `source-writeup.docx`.
- The binary is a stripped x86-64 PIE with a large `.data` section; the two tables are at file offsets `0x3020` and `0x8c20`.

## Run the solver

Then run it:

```bash
cd solve
python solve.py
```

Expected final line:

```text
[+] FLAG: CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}
```

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
