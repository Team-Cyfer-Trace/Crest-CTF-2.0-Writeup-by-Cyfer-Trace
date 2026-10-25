# Close Enough

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-Cryptography-B4441F?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-1200-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-122-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

A key-generation service exported public RSA parameters and a large queue of encrypted application records. The service was expected to create independent keys and preserve a verifiable chain of records. Something in the exported data was not as expected. Recover the protected message and submit the exact value.

**Flag format:** `CREST{...}`

**Attachments:** [`keyset.json`](attachments/keyset.json) · [`messages.json`](attachments/messages.json)

## Flag

```text
CREST{close_enough_was_only_the_first_lock}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** six RSA moduli were generated from primes that were too close together, so Fermat's method factored them instantly; decrypting the six linked route records revealed the AES-GCM payload key.

- 100 public keys, 500 records, 6 route records.
- Fermat factorization found six weak moduli with **zero** iterations.
- The route chain ended in a `CR5\0FINAL\2` record containing a 32-byte AES key.
- The payload decrypted under AES-256-GCM with authenticated AAD.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/keyset.json`](attachments/keyset.json) | 100 exported RSA public keys |
| [`attachments/messages.json`](attachments/messages.json) | 500 application records plus the encrypted payload |
| [`solve/solve.py`](solve/solve.py) | End-to-end solver: factoring → route → AES-GCM |
| [`solve/requirements.txt`](solve/requirements.txt) | Python dependency (`cryptography`) |

## Run the solver

```bash
cd solve
python -m pip install -r requirements.txt
python solve.py
```

Expected output ends with:

```text
[+] FLAG: CREST{close_enough_was_only_the_first_lock}
```

## Notes

- The weakness is **not** RSA itself. It is the key generation: `p` and `q` are close enough that `ceil(sqrt(n))` lands on a square difference almost immediately.
- The 494 non-route records are noise. The `kind: "route"` field and the decrypted `N=` links identify the intended path.
- AES-GCM authenticates both the ciphertext and the AAD; the solver passes `ciphertext + tag` to `AESGCM.decrypt()`.

---

[← Back to Cryptography](../README.md) · [All writeups](../../README.md)
