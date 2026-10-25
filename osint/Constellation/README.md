# Constellation

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-OSINT-8A4B08?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-350-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-168-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

A leaked export from a small social platform — 26 users, their bios, and a friend/connection graph. `brief.txt` names three accounts of interest. Recover the flag.

**Flag format:** `CREST{...}`

**Attachments:** [`nodebook_export.json`](attachments/nodebook_export.json) · [`brief.txt`](attachments/brief.txt)

## Flag

```text
CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** intersect the neighbour sets of `kestrel`, `fennec`, and `quartz`; the only account connected to all three is `nova_7`, whose bio is Base64.

- 26 users, 26-ish edges, and a lot of filler posts.
- `nova_7` is the only common neighbour.
- The bio decodes to the flag.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/brief.txt`](attachments/brief.txt) | The three accounts of interest |
| [`attachments/nodebook_export.json`](attachments/nodebook_export.json) | Users, bios, connections, and posts |
| [`solve/solve.py`](solve/solve.py) | Graph intersection + Base64 decode |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output:

```text
[+] accounts connected to all three targets: ['nova_7']
[+] nova_7 bio: CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}
```

## Notes

- The `posts` array is noise. The challenge is a single graph query plus one anomalous bio.
- "Connected to all three" means the intersection of the three adjacency sets, not a path through the graph.
- Base64 is easy to spot here because the bio is the only field that does not read like a sentence.

---

[← Back to OSINT](../README.md) · [All writeups](../../README.md)
