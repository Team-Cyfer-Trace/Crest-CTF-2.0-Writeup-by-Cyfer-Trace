> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:20 p.m.
>
> **Official challenge:** Noise Updated · **Category:** Cryptography · **Difficulty:** Expert · **Points:** 900 · **Solves:** 143
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Noise Updated (CTF7) — Writeup

**Flag:** `CREST{FORENSIC_NONCE_ALIGNMENT_V3}`

## Artifacts

`signatures.json` (16 ECDSA/secp256k1 signatures over SHA-256 digests), `pubkey.pem`, `sign_service.py`, `evidence/incident_17.log`, `evidence/calibration.note`, `sealed_flag.bin`.

The log (~73 MB), `signatures.json` and `pubkey.pem` are padded with many `CREST{decoy_...}` strings and `DECOY PUBLIC KEY` comments. These are noise; the real key is the only PEM block in `pubkey.pem`.

## Analysis

1. `sign_service.py` shows the nonce is `make_nonce(counter, quantum) = (counter // quantum) * quantum`, so every nonce is a multiple of `quantum`.
2. `calibration.note` says the quantum is a power of two, 2^q, with q in 18..31. The `24` in the margin and `LEGACY_QUANTUM = 0x01000000` (2^24) are untrusted, and the log warns not to trust the constant without signature-level validation.
3. So k_i = 2^q * m_i, where m_i < n / 2^q. The low q bits of every nonce are zero.

## Attack: Hidden Number Problem

ECDSA gives `s*k = h + r*d (mod n)`. Substituting k = 2^q * m:

```
m_i = a_i + b_i * d (mod n)
a_i = h_i / (s_i * 2^q),   b_i = r_i / (s_i * 2^q)
```

Each m_i is smaller than n / 2^q, so the pairs (a_i, b_i) form a hidden number problem instance. I built the usual embedding lattice (rows n·I, the b vector, the a vector with an embedding constant X = n >> q), scaled so the d coordinate and the m coordinates have comparable size, and ran LLL (sympy). Then I looked for a reduced row with last coordinate ±X and read off d.

Every q in 18..31 was tried, and a candidate d was accepted only if `d*G == pubkey`. Only **q = 18** produced a valid key. The stale 2^24 constant is wrong.

Recovered private scalar:

```
d = 0xf757acbadcb14f5fcf9ce5d80b54a633888ad75735dc594444517769e630d6a0
```

## Decrypting the flag

- `sealed_flag.bin` = `WBSG1` || 12-byte nonce || ciphertext+tag
- Key = SHA-256(d as 32 big-endian bytes)
- AES-256-GCM, associated data `CRY-03`

The GCM tag verified, and the plaintext was:

```
CREST{FORENSIC_NONCE_ALIGNMENT_V3}
```

## Notes

- Verification: d·G matches `pubkey.pem`, and the GCM tag authenticates. I did not re-check each of the 16 signatures against d separately.
- A first attempt without scaling the d coordinate failed for every q. The d coordinate (about n) dominated the short vector, so the scaling step was required.
