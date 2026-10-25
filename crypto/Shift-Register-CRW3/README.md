# Shift Register CRW3

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Cryptography-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-700-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-77-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:16 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

The Shift Register appliance is a legacy telemetry gateway whose three subsystems were each "modernised" on their own schedule, and each modernisation left one real bug behind. The front door is a telemetry link that still protects its frames with a home-grown stream cipher keyed by a Linear Feedback Shift Register -- a keystream that gives itself up to anyone holding a scrap of known plaintext. Behind it sits an internal host-diagnostics console that shells out to ping without sanitising its input. And the artifact that console guards is a maintenance binary with a stack overflow that needs the universal gadget to drive it.This is a three-stage chain -- Crypto then Misc then Pwn -- where each stage's output is the next stage's key. Recover the flag from the maintenance console. Access:Stage 1: nc 2.31.70.16 16230Stage 2: http://2.31.70.16:16231/Stage 3: nc 2.31.70.16 16232

**Flag format:** `ctf7{...}`

**Attachments:** [`shift_console`](attachments/shift_console)

**Targets (offline after the event):** `nc 2.31.70.16 16230` · `http://2.31.70.16:16231/` · `nc 2.31.70.16 16232`

## Flag

```text
ctf7{lfsr_berlekamp_massey_cmdi_ret2csu}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

An LFSR stream cipher with known plaintext, a command-injection diagnostics console, and a ret2csu stack overflow.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/shift_console` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |

## Notes

- The archived `shift_console` is the stage-3 maintenance binary used for the pwn stage.
- The flag uses lowercase `ctf7{...}`.

## Run the solver

No offline solver is archived; two of the three stages are remote services that are offline after the event. The writeup contains the LFSR recovery, the command injection, and the ret2csu chain.

---

[← Back to Cryptography](../README.md) · [All writeups](../../README.md)
