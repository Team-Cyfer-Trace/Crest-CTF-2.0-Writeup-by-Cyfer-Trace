# Origami

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Reverse_Engineering-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-400-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-193-1F5F73?style=flat-square)

> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:06 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

Another access-control binary — but this one's data section is clearly obfuscated garbage until the program starts running. Something unpacks before the real check happens. Flag format: CREST{...} Attachment: origami (x86-64 ELF, statically linked, stripped)

**Flag format:** `CREST{...}`

**Attachments:** [`origami`](attachments/origami)

## Flag

```text
CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

An XOR-unpacked bytecode VM checks one byte per block with XOR and rotate constraints; invert each block directly.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `source-writeup.docx` | Original author-formatted Word writeup, preserved unchanged. |
| `attachments/origami` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested inversion of the per-byte XOR/ROL VM. |

## Notes

- The author's original Word writeup is preserved as `source-writeup.docx`.
- The packed blob is at file offset `0x3020`; the four-byte XOR key is at `0x31cb`.

## Run the solver

Then run it:

```bash
cd solve
python solve.py
```

Expected final line:

```text
[+] FLAG: CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}
```

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
