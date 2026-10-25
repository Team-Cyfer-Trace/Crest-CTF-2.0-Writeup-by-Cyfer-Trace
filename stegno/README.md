# Steganography

Data hidden in the places nobody looks: invisible code points, pixel planes, audio spectra, and file metadata.

**Team result:** 2 of 2 cleared · **Published writeups:** 2 (1 personal, 1 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Transmission](Transmission/) | Ishant Choudhary (`griffin-dox`) | Hard | 600 | 80 | [read](Transmission/writeup.md) |
| [Afterimage Protocol](Afterimage-Protocol/) | Hrishikesh (`hrishikesh`) | Expert | 1000 | 144 | [read](Afterimage-Protocol/writeup.md) |

All challenges in this category were cleared by the team.

## Notes

- `Transmission` uses four invisible Unicode code points, Morse, Base32, Base64, and a repeating-key XOR.
- `Afterimage Protocol` hides the real payload in PNG row-filter bytes and steganographic pixel selection; metadata and visible flag-shaped strings are decoys.

---

[← All categories](../README.md) · [All writeups](../README.md)
