# NP In Disguise

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Miscellaneous-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-600-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-96-1F5F73?style=flat-square)

> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:18 p.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

We invented our own tiny esoteric programming language, NP-lang. Programs make a series of guesses and check some constraints on them. Here's a program, its spec, and a reference interpreter that can check whether a given set of guesses makes the program succeed. Find the guesses that make it succeed, and it'll hand you something worth having.

**Flag format:** `ctf7{...}`

**Attachments:** No local attachment: the target served `program(1).esolang`, `SPEC.md`, and `interpreter.py`, which are offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:8111/`

## Flag

```text
ctf7{s4t_1s_h4rd_but_n0t_f0r_us}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Reverse a tiny esolang into Boolean constraints, solve the assignment, and use its SHA-256 digest as the payload key.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The program has 70 variables and 750 clauses; the author solved it as SAT and verified zero unsatisfied clauses.
- The flag prefix is lowercase `ctf7{...}`.

## Run the solver

No standalone solver is archived because the `.esolang` program, `SPEC.md`, and reference interpreter were served by the offline target. The writeup gives the constraint construction and final assignment.

---

[← Back to Miscellaneous](../README.md) · [All writeups](../../README.md)
