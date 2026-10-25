# Same Key Twice

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Cryptography-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-550-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-69-1F5F73?style=flat-square)

> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:44 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

Two supposedly independent secure-chat sessions were recovered from a noisy telemetry archive. The exports contain 500,000 routine operational events each, with a small number of protocol records mixed into the stream. Record order is not trustworthy. A handful of strings resembling flags appear in unrelated operational events; do not assume a flag-shaped string is valid merely because it matches the format. Flag format: CREST{...} Attachments: chall.py, evidence/alpha.cblog, evidence/bravo.cblog

**Flag format:** `CREST{...}`

**Attachments:** See [attachments/README.md](attachments/README.md) for the official download links.

## Flag

```text
CREST{nonce_reuse_breaks_confidentiality_and_integrity}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

A repeated ECDSA nonce leaks the private key; two very large chatter logs supply the signatures.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/README.md` | Attachment note and official download links. |

## Notes

- The two official `.cblog` files are 92.96 MB each (186 MB total). They are linked from `attachments/README.md` instead of committed.
- The writeup notes that `chall.py` was not provided as an attachment.
- The flag prefix is uppercase `CREST{...}`.

## Run the solver

No standalone solver is archived. The author's `work/solve.py` was not included, and the two 93 MB evidence files are linked rather than committed; the writeup gives the full nonce-reuse recovery.

---

[← Back to Cryptography](../README.md) · [All writeups](../../README.md)
