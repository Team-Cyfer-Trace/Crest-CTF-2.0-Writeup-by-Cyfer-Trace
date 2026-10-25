# Cryptography

Number theory, broken nonces, weak key generation, and the occasional lattice. The math is the exploit.

**Team result:** 5 of 9 cleared · **Published writeups:** 5 (1 personal, 4 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Close Enough](Close-Enough/) | Ishant Choudhary (`griffin-dox`) | Expert | 1200 | 122 | [read](Close-Enough/writeup.md) |
| [Same Key Twice](Same-Key-Twice/) | Bryan (`RadixCobra19`) | Hard | 550 | 69 | [read](Same-Key-Twice/writeup.md) |
| [Biased Signatures](Biased-Signatures/) | Bryan (`RadixCobra19`) | Hard | 600 | 90 | [read](Biased-Signatures/writeup.md) |
| [Shift Register CRW3](Shift-Register-CRW3/) | Hrishikesh (`hrishikesh`) | Expert | 700 | 77 | [read](Shift-Register-CRW3/writeup.md) |
| [Noise Updated](Noise-Updated/) | Hrishikesh (`hrishikesh`) | Expert | 900 | 143 | [read](Noise-Updated/writeup.md) |

## Still open

| Challenge | Difficulty | Solves |
| --- | --- | ---: |
| Cursed Pad | Hard | 0 |
| Marvin's Return | Hard | 12 |
| Modular Whisper | Hard | 1 |
| Salted Not Cured | Hard | 46 |

## Notes

- `Biased Signatures` leaks the top 56 bits of every ECDSA nonce; the writeup uses the hidden-number problem and a small lattice.
- `Noise Updated` infers the quantisation exponent from the signatures, then applies the same hidden-number approach.
- `Same Key Twice` is a nonce-reuse break, but its two official evidence files are 93 MB each and are linked rather than committed.
- `Shift Register CRW3` is a three-stage crypto → pwn chain; the archived binary is the stage-3 maintenance console.
- `Close Enough` recovers RSA primes from a shared-prime key-generation bug.

---

[← All categories](../README.md) · [All writeups](../README.md)
