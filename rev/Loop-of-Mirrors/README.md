# Loop of Mirrors

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Reverse_Engineering-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-1000-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-189-1F5F73?style=flat-square)

> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:05 a.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

The mirror accepts one reflection. Its validation logic is folded through evolving state transitions, and material recovered along the way matters to what follows.
Recover the one flag the mirror accepts. Run the stripped Linux x86-64 executable (chmod +x mirror && ./mirror) and enter one flag line in the normal CREST{...} format. The challenge is fully offline and requires no network access. Debuggers, disassemblers, emulators, scripts, and AI assistance are allowed.
Attachment: mirror

**Flag format:** `CREST{...}`

**Attachments:** [`mirror`](attachments/mirror)

## Flag

```text
CREST{pr1sms_tw1st_paths_bef0re_th3_last_echo_7c91d2ab}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Three hash-chained VM programs validate three shuffled 16-byte blocks; the author inverted the VMs with a Unicorn emulator.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `source-writeup.docx` | Original author-formatted Word writeup, preserved unchanged. |
| `attachments/mirror` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |

## Notes

- The author's original Word writeup is preserved as `source-writeup.docx`.
- The binary is a stripped x86-64 PIE; the flag is 55 characters and the validator is fully offline.
- The challenge is listed officially as `Loop of Mirrors`; the author's working title was `mirror`.

## Run the solver

No standalone solver is archived. The author's original writeup uses a Unicorn-based emulator and is preserved as `source-writeup.docx`; the binary is included for reproduction.

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
