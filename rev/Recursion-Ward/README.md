# Recursion Ward

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Reverse_Engineering-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Medium-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-300-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-165-1F5F73?style=flat-square)

> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:06 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

A third access-control binary. Symbols are intact this time (you'll find a check function), but reading it top-to-bottom won't get you far — the control flow has been flattened into a single switch on a "state" variable, with a handful of decoy branches mixed in that never actually lead anywhere useful. Submit the accepted input. Flag format: CREST{...} Attachment: recursion_ward (x86-64 ELF, dynamically linked, symbols present)

**Flag format:** `CREST{...}`

**Attachments:** [`recursion_ward`](attachments/recursion_ward)

## Flag

```text
CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

The checker is control-flow flattened into a state machine; follow the real state graph from start to accept.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `source-writeup.docx` | Original author-formatted Word writeup, preserved unchanged. |
| `attachments/recursion_ward` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested capstone/pyelftools state-graph walker. |
| `solve/requirements.txt` | Python dependencies for the archived solver. |

## Notes

- The author's original Word writeup is preserved as `source-writeup.docx`.
- The binary is not stripped, so the solver locates `check` directly rather than hard-coding its address.

## Run the solver

Install the solver dependencies first:

```bash
cd solve
python -m pip install -r requirements.txt
```

Then run it:

```bash
cd solve
python solve.py
```

Expected final line:

```text
[+] FLAG: CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}
```

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
