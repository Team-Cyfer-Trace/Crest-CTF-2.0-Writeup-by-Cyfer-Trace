# Transmission

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-Steganography-7A3B52?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-600-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-80-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

An archived conversation appears ordinary, but its formatting may carry another message. Investigate the original transmission and recover the hidden flag.

**Flag format:** `CREST{...}`

Preserve the exact downloaded file; copying only its visible text may remove evidence.

**Attachment:** [`transmission.txt`](attachments/transmission.txt)

## Flag

```text
CREST{bl4nk_5p4ces_4re_d3lusi0ns}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** 485 invisible Unicode characters form 71 Morse groups, which spell a Base32 string; decoding it yields Base64, which XORs with `KEY42` to reveal the flag.

- Four invisible code points are used: two carry data, one separates groups, one is filler.
- The data maps to Morse, then Base32, then Base64, then a repeating-key XOR.
- The known flag prefix `CREST{` reveals the 5-byte XOR key `KEY42`.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/transmission.txt`](attachments/transmission.txt) | Original chat log with invisible characters |
| [`solve/solve.py`](solve/solve.py) | Full decoding chain |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output:

```text
[+] invisible characters: 485
[+] Morse groups: 71
[+] Base32: INBGGY22GJMXOST2KVAVQQ2BMFREKUKHJNBUC4LBO5MTKSKBLJIUCU3DO5FWYMCDJJKFS2Y
[+] FLAG: CREST{bl4nk_5p4ces_4re_d3lusi0ns}
```

## Notes

- Do not copy/paste the visible text. The payload lives in characters that most editors hide.
- The mapping that produces valid Morse is **U+200B = dash** and **U+034F = dot**; the opposite assignment produces invalid groups such as `---.`.
- The Morse output is Base32 (`A–Z`, `2–7`). It then decodes to Base64, not directly to the flag.

---

[← Back to Steganography](../README.md) · [All writeups](../../README.md)
