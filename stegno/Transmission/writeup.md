# Transmission — full writeup

[← Back to Steganography](../README.md) · [Challenge overview](README.md)

**Category:** Steganography · **Difficulty:** Hard · **Points:** 600 · **Solves:** 80 · **Flag:** `CREST{bl4nk_5p4ces_4re_d3lusi0ns}`

## TL;DR

- The visible chat log is a decoy. The last line, just before `--END--`, contains 485 invisible Unicode characters.
- Four code points are in play:
  - **U+200B** zero width space → dash
  - **U+034F** combining grapheme joiner → dot
  - **U+200C** zero width non-joiner → group separator
  - **U+2060** word joiner → filler, ignored
- Splitting on U+200C gives 71 Morse groups.
- Morse → Base32 → Base64 → repeating-key XOR (`KEY42`) → flag.

## Step 1 — Look at the raw bytes

The chat text looks ordinary. A hex dump of the last line shows a long run of non-ASCII bytes:

```bash
xxd transmission.txt | tail
```

The run uses only four code points, all invisible in a normal editor. That is the signal: the message is in the formatting, not the prose.

| Code point | Name | Role |
| --- | --- | --- |
| U+034F | Combining Grapheme Joiner | dot |
| U+200B | Zero Width Space | dash |
| U+2060 | Word Joiner | filler, ignored |
| U+200C | Zero Width Non-Joiner | separator between groups |

The mapping is easy to get backwards. The assignment above is the one that produces valid Morse groups; swapping dash and dot produces sequences such as `---.`, which is not a letter or digit.

## Step 2 — Morse

Drop U+2060 and split on U+200C:

```python
hidden = [c for c in text if c in "\u034f\u200b\u200c\u2060"]
symbols = "".join(
    "-" if c == "\u200b" else "." if c == "\u034f" else "|" if c == "\u200c" else ""
    for c in hidden
)
groups = [g for g in symbols.split("|") if g]
```

There are 71 groups, with lengths between one and five. That is exactly the shape of Morse letters and digits.

Decoding gives:

```text
INBGGY22GJMXOST2KVAVQQ2BMFREKUKHJNBUC4LBO5MTKSKBLJIUCU3DO5FWYMCDJJKFS2Y
```

## Step 3 — Base32

The Morse output uses only `A–Z` and `2–7` — the Base32 alphabet. Pad to a multiple of eight and decode:

```python
b32 = encoded + "=" * (-len(encoded) % 8)
raw = base64.b32decode(b32)
```

That yields:

```text
CBccZ2YwJzUAXCAabEQGKCAqawY5IAZQAScwKl0CJTYk
```

## Step 4 — Base64

The intermediate is itself Base64. Decode it (with padding) to 33 raw bytes:

```python
raw += b"=" * (-len(raw) % 4)
ciphertext = base64.b64decode(raw)
```

The bytes are non-printable, so there is one more layer.

## Step 5 — XOR with the known prefix

The flag format is `CREST{`. XOR the first six bytes of the ciphertext with `CREST{`:

```text
CT[0:6]  = 08 17 1c 67 66 30
CREST{   = 43 52 45 53 54 7b
key      = 4b 45 59 34 32 4b   -> "KEY42K"
```

The first five bytes repeat: **`KEY42`**. XOR the whole ciphertext with the repeating key:

```python
key = b"KEY42"
plaintext = bytes(c ^ key[i % len(key)] for i, c in enumerate(ciphertext))
```

## Decoding chain

```text
zero-width characters
        ↓
      Morse
        ↓
      Base32
        ↓
      Base64
        ↓
 XOR with "KEY42"
        ↓
       flag
```

## The solver

```python
hidden = [c for c in text if c in {DASH, DOT, SEPARATOR, FILLER}]
symbols = "".join(
    "-" if c == DASH else "." if c == DOT else "|" if c == SEPARATOR else ""
    for c in hidden
)
groups = [g for g in symbols.split("|") if g]
encoded = "".join(MORSE[g] for g in groups)
```

Full script, including the Morse table and padding: [`solve/solve.py`](solve/solve.py).

## Flag

```text
CREST{bl4nk_5p4ces_4re_d3lusi0ns}
```

## What I learned

- **Visible text is not the file.** Zero-width characters survive in the bytes but disappear from the rendered page.
- **Treat invisible code points as an alphabet.** Count the distinct characters; one is usually a separator, one is filler, and the rest carry symbols.
- **Validate the mapping.** Morse has a strict grammar, so an invalid group means the dash/dot assignment is wrong.
- **Known plaintext is powerful.** A six-byte known prefix was enough to recover the repeating XOR key.

## Reproduce

```bash
cd solve
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to Steganography](../README.md) · [Challenge overview](README.md)
