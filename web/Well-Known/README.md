# Well Known

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Web-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Easy-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-200-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-196-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:02 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

Crest Security has launched its new marketing site and promises security you can verify. Take a look around and find the flag. Flag format: crest{...}

**Flag format:** `crest{...}`

**Attachments:** No attachments: this was a live web service, offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:5400/`

## Flag

```text
crest{w3ll_kn0wn_s3cur1ty_txt}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

The marketing site points to `/.well-known/security.txt`, where an internal canary contains the flag.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The flag uses lowercase `crest{...}`.

## Run the solver

No offline solver is archived; the target is offline. The writeup gives the exact `.well-known` path and the canary.

---

[← Back to Web](../README.md) · [All writeups](../../README.md)
