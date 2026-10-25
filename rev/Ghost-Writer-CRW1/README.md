# Ghost Writer CRW1

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Reverse_Engineering-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-700-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-138-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 11:05 a.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

The "Ghost Writer" note appliance ships as two halves. The field firmware -- a small MIPS (big-endian) client called gw-client -- talks to a backend "note daemon" over a private binary protocol that has no menu, no banner and no documentation. The backend itself is still running.This is a deliberately two-domain capstone. Stage 1 is pure reverse engineering on an architecture the rest of the collection never touches: you run and disassemble the MIPS firmware under qemu-mips (qemu-user) to recover the wire protocol -- the handshake magic, the numeric opcodes and the request-header layout -- without which the backend ignores you entirely. Stage 2 is heavyweight heap exploitation against the live x86-64 backend (pinned glibc 2.36). A use-after-free lets you corrupt the metadata of a chunk sitting in a large bin and mount the canonical large-bin attack: a single bk_nextsize write redirects a global function-table pointer into memory you control, turning a diagnostic command into a call of your choosing. Recover the flag from the note daemon. Access:Stage 1: http://2.31.70.16:16250/Stage 2: nc 2.31.70.16 16251

**Flag format:** `ctf7{...}`

**Attachments:** [`gw-client`](attachments/gw-client) · [`noted`](attachments/noted)

**Targets (offline after the event):** `http://2.31.70.16:16250/` · `nc 2.31.70.16 16251`

## Flag

```text
ctf7{mips_re_largebin_attack_chain}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Reverse a big-endian MIPS client protocol, then exploit a large-bin use-after-free in the x86-64 backend.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/gw-client` | Official challenge file. |
| `attachments/noted` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/exploit.py` | Author's live-service exploit; preserved but not runnable after the event. |

## Notes

- `gw-client` is the MIPS firmware; `noted` is the x86-64 backend.
- The exploit uses the `GWP1` protocol and a large-bin attack; see the writeup for the exact heap layout.

## Run the solver

Then run it:

```bash
cd solve
python exploit.py
```

This is the author's exploit against the original live daemon. It is preserved for reference, but it cannot be tested now because `2.31.70.16:16251` is offline.

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
