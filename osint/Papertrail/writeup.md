# Papertrail — full writeup

[← Back to OSINT](../README.md) · [Challenge overview](README.md)

**Category:** OSINT · **Difficulty:** Medium · **Points:** 250 · **Solves:** 253 · **Flag:** `CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}`

## TL;DR

1. `cover_memo.txt` says only documents authored by the compromised account, R. Chen, are relevant.
2. A `.docx` is a ZIP. Read `docProps/core.xml` for `dc:creator` and `dc:description`.
3. Four files are authored by R. Chen; each `dc:description` contains a Base64 `frag=`.
4. The filenames are not the order. The body text says `Internal Memo #1` … `#4`; sort by that number.
5. Concatenate the fragments and Base64-decode.

## The cover memo

```text
SECURITY ADVISORY - internal distribution
-------------------------------------------
We believe R. Chen's workstation was compromised sometime this
month. IT recovered 9 documents from the affected backup share,
but only documents actually AUTHORED by the compromised account
are relevant -- the rest are unrelated noise from the same backup job.
```

This is the first filter. The challenge is not "read all nine documents"; it is "attribute the documents, then read the ones that belong to the compromised account."

## Step 1 — Treat the docx as a ZIP

A `.docx` file is an OOXML package. The metadata is in `docProps/core.xml`:

```bash
for f in *.docx; do
  echo "== $f"
  unzip -p "$f" docProps/core.xml
  echo
done
```

The two fields that matter:

```xml
<dc:creator>R. Chen</dc:creator>
<dc:description>frag=Q1JFU1R7ZDBjeF9</dc:description>
```

## Step 2 — Filter by author

| File | Creator | `dc:description` |
| --- | --- | --- |
| `doc_01.docx` | T. Nakamura | no fragment |
| `doc_02.docx` | **R. Chen** | `frag=QxZXNfYXIzX20zd` |
| `doc_03.docx` | **R. Chen** | `frag=Q1JFU1R7ZDBjeF9` |
| `doc_04.docx` | **R. Chen** | `frag=DRkNHQ0X3QwMH0=` |
| `doc_05.docx` | **R. Chen** | `frag=jMHJlX3ByMHAzcn` |
| `doc_06.docx` | M. Okonkwo | no fragment |
| `doc_07.docx` | D. Kowalski | no fragment |
| `doc_08.docx` | M. Okonkwo | no fragment |
| `doc_09.docx` | M. Okonkwo | no fragment |

Exactly four documents pass the author filter, and each one carries a fragment.

## Step 3 — Order by memo number, not filename

The visible body text is otherwise filler:

```text
Routine status update, nothing sensitive here.
Internal Memo #3
```

The memo number is the ordering key:

| Memo | File | Fragment |
| --- | --- | --- |
| #1 | `doc_03.docx` | `Q1JFU1R7ZDBjeF9` |
| #2 | `doc_05.docx` | `jMHJlX3ByMHAzcn` |
| #3 | `doc_02.docx` | `QxZXNfYXIzX20zd` |
| #4 | `doc_04.docx` | `DRkNHQ0X3QwMH0=` |

Filename order (`02, 03, 04, 05`) is wrong, and revision counts do not help. The memo number is the only order that produces a valid Base64 string.

## Step 4 — Concatenate and decode

```text
Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=
```

```bash
echo -n 'Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=' | base64 -d
```

## The solver

The Python version avoids `unzip` and `pandoc`:

```python
import zipfile, re, base64

with zipfile.ZipFile(path) as archive:
    core = archive.read("docProps/core.xml").decode()
    document = archive.read("word/document.xml").decode()

creator = re.search(r"<dc:creator>(.*?)</dc:creator>", core).group(1)
description = re.search(r"<dc:description>(.*?)</dc:description>", core).group(1)
text = " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", document))
memo = int(re.search(r"Internal Memo #(\d+)", text).group(1))
```

It collects `(memo, fragment)` pairs, sorts them, joins the fragments, and decodes. Full script: [`solve/solve.py`](solve/solve.py).

## Flag

```text
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

## What I learned

- **Office documents are ZIP archives.** Metadata, document text, and embedded objects are separate XML parts, and they can tell different stories.
- **Attribution is a filter.** The cover memo turns nine files into four before any decoding starts.
- **Do not trust filename order.** When a challenge splits data across files, look for an explicit sequence in the content.
- **Check `dc:description`.** It is easy to ignore because it is not a field a normal reader sees in Word.

## Reproduce

```bash
cd solve
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to OSINT](../README.md) · [Challenge overview](README.md)
