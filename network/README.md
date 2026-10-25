# Networking

Protocol archaeology, captures, identity brokers, and the places where networks leak credentials.

**Team result:** 1 of 1 cleared · **Published writeups:** 1 (0 personal, 1 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Keymaster CRW2](Keymaster-CRW2/) | Hrishikesh (`hrishikesh`) | Expert | 700 | 146 | [read](Keymaster-CRW2/writeup.md) |

All challenges in this category were cleared by the team.

## Notes

- `Keymaster CRW2` is a three-stage chain: NTLMv2 cracking → anomalous-curve ECDSA (Smart's attack) → OAuth `redirect_uri` bypass.
- The lesson is the composition: a network capture yields a credential, the credential unlocks a broken curve, and the curve's private key is the OAuth client secret.

---

[← All categories](../README.md) · [All writeups](../README.md)
