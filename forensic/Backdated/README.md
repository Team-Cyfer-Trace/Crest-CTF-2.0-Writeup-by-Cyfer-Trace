# Backdated

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Forensics-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-550-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-87-1F5F73?style=flat-square)

> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:17 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

We suspect an attacker tampered with file timestamps on a compromised host to make their tooling look like ancient, irrelevant cruft. We pulled a filesystem snapshot (snapshot.bin) — but per-file modification times in a snapshot are just metadata, and metadata can be forged. Luckily our logging agent keeps a separate, append-only audit journal (journal.jsonl) that records the true creation order of every file via a monotonically increasing sequence number. An attacker can rewrite a file's claimed timestamp, but they can't rewrite the journal after the fact. Cross-reference the two. Something doesn't add up.

**Flag format:** `ctf7{...}`

**Attachments:** No local attachment: the challenge served `snapshot.bin` and `journal.jsonl` from the target, which is offline.

**Targets (offline after the event):** `http://2.31.70.16:8100/`

## Flag

```text
ctf7{t1m3st4mps_l13_but_j0urn4ls_d0nt}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A forged snapshot timestamp is exposed by the append-only audit journal's true creation order.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The author's original title was “Timestamp Forgery (journal vs snapshot)”; the official challenge name is `Backdated`.
- The writeup recovers the flag from the file whose journal creation order contradicts its claimed timestamp.

## Run the solver

No standalone solver is archived because the two evidence files were served by the offline target. The writeup gives the full cross-reference method.

---

[← Back to Forensics](../README.md) · [All writeups](../../README.md)
