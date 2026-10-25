# Nightfall

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Multi-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-200-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-188-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:19 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

A Linux host running an internal Depot Portal has been placed in your investigation scope. Your objective is to assess the exposed services, gain a foothold, and work your way through the machine to recover both flags. The system may reveal more than it first appears to. Investigate carefully and document your findings as you progress. Retrieve and submit both flags: user.txt (user-level flag) and root.txt (root-level flag). Flag format: crest{...} The target exposes a web service and SSH; your instance details are provided when the challenge starts. Rules: attack only your assigned NIGHTFALL instance. Do not attack hosting infrastructure, other teams' instances, or unrelated systems. Do not share flags or solutions with other teams. If the instance appears unavailable or broken, contact the organizers. Good luck, and follow the trail.

**Flag format:** `crest{...}`

**Attachments:** No attachments: this was a live Linux boot2root target, offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:8080/`

## Flag

```text
user.txt: crest{r3us3d_cr3ds_0p3n_th3_d00r}
root.txt: crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A Linux boot2root: exposed backup source, a diagnostic token, an uploaded web shell, and a root-owned timer script via PATH hijack.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- Nightfall carries two flags: `user.txt` and `root.txt`. Both exact values are reproduced from the writeup.
- The flag prefix is lowercase `crest{...}`.

## Run the solver

No solver is archived; the engagement required the live host and SSH access. The writeup contains the full enumeration and privilege-escalation chain.

---

[← Back to Multi](../README.md) · [All writeups](../../README.md)
