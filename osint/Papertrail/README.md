# Papertrail

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-OSINT-8A4B08?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-7A5A12?style=flat-square)
![Points](https://img.shields.io/badge/Points-250-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-253-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

9 Word documents were recovered from a backup share, along with `cover_memo.txt` explaining why. Only some of these documents actually matter.

**Flag format:** `CREST{...}`

**Attachments:** [`files_xpYwEQI.zip`](attachments/files_xpYwEQI.zip) (extracted into `attachments/docs/files/`) · [`cover_memo.txt`](attachments/docs/files/cover_memo.txt)

## Flag

```text
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** filter the nine `.docx` files by `dc:creator`; only the four authored by R. Chen contain Base64 fragments, ordered by the `Internal Memo #N` number in the body text.

- A `.docx` is a ZIP. The author and description live in `docProps/core.xml`.
- Four documents are authored by R. Chen and carry `frag=` values.
- Filenames are not the order; the memo numbers are.
- Concatenating the fragments in memo order gives the Base64 flag.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/files_xpYwEQI.zip`](attachments/files_xpYwEQI.zip) | Original challenge bundle |
| [`attachments/docs/files/cover_memo.txt`](attachments/docs/files/cover_memo.txt) | Explains that only R. Chen's documents matter |
| [`attachments/docs/files/doc_01.docx`](attachments/docs/files/doc_01.docx) … [`doc_09.docx`](attachments/docs/files/doc_09.docx) | Nine Word documents |
| [`solve/solve.py`](solve/solve.py) | Author filter, memo ordering, Base64 decode |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output ends with:

```text
[+] FLAG: CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

## Notes

- The `frag=` values are split across four files; no single document is the answer.
- `dc:description` holds the fragment, while `dc:creator` is the trust filter. The visible body text only supplies the memo number.
- Extracted documents are included for convenience. The original zip is kept alongside them so the bundle can be verified.

---

[← Back to OSINT](../README.md) · [All writeups](../../README.md)
