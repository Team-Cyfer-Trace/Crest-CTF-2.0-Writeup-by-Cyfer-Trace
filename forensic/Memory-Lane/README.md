# Memory Lane

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Forensics-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-550-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-42-1F5F73?style=flat-square)

> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:47 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

We pulled a raw memory dump off a compromised host running a proprietary credential-manager service. Incident response left us some notes from a prior engagement against the same software: The process is compiled without ASLR and always loads at a fixed base address of 0x555555554000. Its in-memory record table starts with a 4-byte magic signature CRDM. Good luck reconstructing what it was hiding.

**Flag format:** `ctf7{...}`

**Attachments:** No local attachment: the target served `memdump.bin`, which is offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:8060/`

## Flag

```text
ctf7{m3m0ry_w4lk1ng_cr3d_c4rv3}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Reconstruct a credential-manager record table from a raw memory dump at a fixed, non-ASLR base address.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The challenge notes a fixed base address of `0x555555554000` and a record table starting with the `CRDM` magic.
- The writeup recovers the flag from the record table and preserves the exact string.

## Run the solver

No standalone solver is archived because the memory dump was served by the offline target. The writeup gives the record-table walk and flag extraction.

---

[← Back to Forensics](../README.md) · [All writeups](../../README.md)
