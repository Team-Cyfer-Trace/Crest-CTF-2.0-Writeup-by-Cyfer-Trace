# Query Shadow

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Web-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-400-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-232-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:40 a.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

Shadow Directory is a lightweight internal staff directory. Register an account, set a display name on your profile, then open the Colleagues page to see everyone who picked the same display name as you.
The directory knows more than it lets on. Recover the flag. Flag format: crest{...}

**Flag format:** `crest{...}`

**Attachments:** No attachments: this was a live web service, offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:5200/`

## Flag

```text
crest{sec0nd_0rder_1nj3ct10n_sh4d0w}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A stored display name is spliced into an XPath query; inject a UNION-style payload to reach the flag node.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The exact flag is reproduced from the author's writeup.
- The writeup's original heading is “Shadow Directory”, the application name; the official challenge name is `Query Shadow`.

## Run the solver

No offline solver is archived; the target is offline. The writeup contains the registration flow and the XPath payload.

---

[← Back to Web](../README.md) · [All writeups](../../README.md)
