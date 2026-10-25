# Session Drift

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Web-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Medium-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-300-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-174-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:35 a.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

Welcome to the Crest staff portal: single sign-on for Crest employees. Your session keeps you signed in across internal tools, and access to administrative reports is restricted to staff with the admin role.
Sign in with the demo account alice / password123 and find a way to read the admin report. Flag format: crest{...}

**Flag format:** `crest{...}`

**Attachments:** No attachments: this was a live web service, offline after the event.

**Targets (offline after the event):** `http://2.31.70.16:5100/`

## Flag

```text
crest{s3ss10n_dr1ft_s3cr3t_reuse}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A Flask-style client-side session cookie is signed with a weak secret; forge the admin role.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |

## Notes

- The demo account is `alice` / `password123`.
- The flag uses lowercase `crest{...}`.

## Run the solver

No offline solver is archived; the target is offline. The writeup shows the cookie decode, secret recovery, and forged session.

---

[← Back to Web](../README.md) · [All writeups](../../README.md)
