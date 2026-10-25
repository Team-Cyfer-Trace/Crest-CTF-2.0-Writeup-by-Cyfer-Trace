# White Pixel

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Web-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Medium-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-200-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-74-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:09 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

A near-blank white page. It looks completely empty — or does it? Flag format: crest{...}

**Flag format:** `crest{...}`

**Attachments:** No local attachment: the page served `/q.png`, which is offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:5500/`

## Flag

```text
crest{p}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A near-blank page serves a 60×84 PNG whose two almost-identical whites spell the flag.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The image uses `(255,255,255)` and `(255,255,254)`; treating blue=254 as set reveals the block letter.
- The flag is the very short `crest{p}`; the challenge is a visual reveal, not a long phrase.

## Run the solver

No offline solver is archived because `/q.png` was not preserved. The writeup gives the pixel threshold and the rendered letter.

---

[← Back to Web](../README.md) · [All writeups](../../README.md)
