> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:14 p.m.
>
> **Official challenge:** Afterimage Protocol · **Category:** Steganography · **Difficulty:** Expert · **Points:** 1000 · **Solves:** 144
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Afterimage Protocol (STEG-01) — Writeup

**Flag:** `CREST{f1lt3rs_b3f0r3_p1x3ls_9f42d8e1}`

## Challenge

Case NSR-0217: a lossless 1024x800 RGB PNG (`afterimage.png`). Re-saving or converting destroys evidence, so all work was read-only on the original file.

## Overview

The flag sits behind three nested layers. Two fake flags are planted as decoys.

| Where | Content | Verdict |
|---|---|---|
| PNG `tEXt` chunk `Archive-Preview` | `CREST{metadata_is_not_evidence_31d9}` | Decoy |
| Green LSB, row 0 (4-byte length prefix + text) | `CREST{bitplanes_are_only_the_lobby_a61e}` | Decoy |
| PNG row filter bytes | Layer 1 | Real |

## Dead ends

- Bit-plane viewing, LSB extraction across channel and order permutations, and header/keyword searches found only the green-channel decoy.
- Triple-frequency analysis showed that the only pixel-value modifications in the image are in row 0 (the decoy). The real data is therefore not in pixel LSBs at the first level.
- The row filter types are uniformly distributed over 1-4 and never 0. That is unusual for a PNG encoder, so I decoded them as data.

## Layer 1: PNG filter types (2 bits per scanline)

1. Concatenate the IDAT chunks, zlib-decompress, and take the first byte of each of the 800 scanlines.
2. Subtract 1 to get a value 0-3, i.e. 2 bits per row, MSB first, packed into bytes (1600 bits, 200 bytes).
3. Result: `AP1!` | `u16be(len)=187` | zlib data.
4. The zlib data decompresses to a spec for stage 2, including `a=7a1c39e24fd865b0` and the normalization `R&FE, G&FD, B&FE`.

## Layer 2: selected pixels, Morton order, R0^B0

From the layer 1 spec:

- Selector: `((((R>>2)*3) ^ ((G>>2)*5) ^ ((B>>2)*7) ^ (x*11) ^ (y*13)) & 7) < 3`
- Order: Morton code, x bits on even positions and y bits on odd, ascending, 10 bits each.
- Carrier bit: `R0 ^ B0` (XOR of the two LSBs).
- Format: `AP2!` | `u16be(len)=446` | zlib(text) | `crc32be(text)`. The CRC matched.

The text is the layer 3 spec. It gives `b=e9136cb2a04f7d58` and `nonce=051160a96d7b299f`, plus:

- Pool selector: `((((R>>2)*11)+((G>>2)*17)+((B>>2)*23)+(x*5)+(y*7)) & 15) in (2,5,9)`, taken in row-major order.
- Shuffle: a PCG32 (XSH-RR 64/32) seeded from a BLAKE2s hash, followed by a Fisher-Yates shuffle (`i = n-1..1`, `j = next % (i+1)`).
- Carrier bit: green bit 1 (`G1`), MSB first, 109 bytes.
- Key derivation, encryption and authentication all use BLAKE2s.

## Layer 3: shuffled pixel pool, G1, authenticated encryption

- `d = SHA256` of the normalized pixels (`R&FE, G&FD, B&FE`), RGB row-major, raw bytes.
- `case = "NSR-0217"`; `a`, `b` and `nonce` are the hex strings decoded to bytes.
- `P = BLAKE2s-32("AP3/PCG\0" | d | case | a | b | nonce)`; `initstate = le64(P[0:8])`, `initseq = le64(P[8:16])`.
- The 109 carrier bits give the wire format `AP3F | 01 | 01 | u32be(ctlen) | ct | tag16`.
- `Kenc` and `Ktag` come from `AP3/ENC\0` and `AP3/TAG\0` with the same inputs as `P`.
- The tag is `BLAKE2s-16` keyed with `Ktag` over `"AP3/AUTH\0" | header | ct`. It verified, which confirmed every encoding choice above.
- The keystream is `ks[i] = BLAKE2s-32(key=Kenc, "AP3/KS\0" | nonce | u32be(i))`. Plaintext is `ct XOR ks`, which is zlib data.

Decompressed:

```
AFTERIMAGE/FINAL
case=NSR-0217
proof=CREST{f1lt3rs_b3f0r3_p1x3ls_9f42d8e1}
```

## Takeaways

- Stego can hide in container structure (PNG filter bytes), not only in pixel values.
- Each layer's output is the next layer's instructions, so decoding is sequential.
- The authentication tag gives an exact check that all key-derivation choices were right.

## Scripts

- `jj.py`: layer 1 (filter types)
- `kk.py`: layer 2 (Morton order, R0^B0)
- `ll.py`: layer 3 (PCG shuffle, G1, decrypt)
