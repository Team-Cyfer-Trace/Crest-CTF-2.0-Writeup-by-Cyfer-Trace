# Noise Updated

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Cryptography-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-900-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-143-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:20 p.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

An incident response team recovered signed audit records, a public key,
fragments of a signing service, and an encrypted evidence capsule. The service
was retired before investigators could recover its configuration. Determine
whether the signatures expose the signing key and recover the evidence.
Objectives:

 Establish that the signatures are valid and determine what the evidence implies about nonce generation.
 Reconcile the conflicting configuration clues. The candidate exponent range is deliberately wider than the previous build; do not assume the stale constant is authoritative.
 Derive the relevant ECDSA relation and recover the private scalar using a justified cryptanalytic method.
 Verify the recovered scalar against pubkey.pem and the complete signature set.
 Recover and authenticate the flag from sealed_flag.bin.

Format notes: sealed_flag.bin begins with the five-byte magic WBSG1, followed
by a 12-byte AES-GCM nonce and then ciphertext plus authentication tag. The
AES-256-GCM associated data is CRY-03. The encryption key is derived as SHA-256
of the recovered private scalar encoded as 32 big-endian bytes.
The artifacts are offline; no network interaction is needed. Submit the flag
in CREST{...} format.
Attachments: signatures.json, pubkey.pem, sign_service.py,
evidence/incident_17.log, evidence/calibration.note, sealed_flag.bin

**Flag format:** `CREST{...}`

**Attachments:** [`files_8hMVcTH.zip`](attachments/files_8hMVcTH.zip)

## Flag

```text
CREST{FORENSIC_NONCE_ALIGNMENT_V3}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Quantised ECDSA nonces with an unknown power-of-two quantum; the quantum is inferred and the key recovered with a hidden-number lattice.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/files_8hMVcTH.zip` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |

## Notes

- The archive contains `signatures.json`, `pubkey.pem`, `sealed_flag.bin`, the recovered `sign_service.py`, and a 73 MB incident log.
- The log and key file contain many `CREST{decoy_...}` strings; the writeup explains why they are not the flag.

## Run the solver

No standalone solver is archived. The official archive is included (`files_8hMVcTH.zip`); the writeup gives the HNP construction, the quantum search, and the decryption step.

---

[← Back to Cryptography](../README.md) · [All writeups](../../README.md)
