# Close Enough — full writeup

[← Back to Cryptography](../README.md) · [Challenge overview](README.md)

**Category:** Cryptography · **Difficulty:** Expert · **Points:** 1200 · **Solves:** 122 · **Flag:** `CREST{close_enough_was_only_the_first_lock}`

## TL;DR

1. The 100 RSA moduli in `keyset.json` are supposed to be independent. Six of them have prime factors that are close together.
2. Fermat's factorization method finds those six factors immediately.
3. Six records in `messages.json` are marked `kind: "route"`. Decrypting them with the factored private keys walks a linked chain.
4. The final route record contains a 32-byte AES key. The payload is AES-256-GCM; decrypt it with the nonce, AAD, ciphertext, and tag.

## The data

`keyset.json` contains 100 public keys:

```json
{
  "public": [
    { "id": "k001", "n": "…", "e": 65537 },
    …
  ]
}
```

`messages.json` contains 500 records and one payload. Most records are operational noise. The useful ones advertise themselves:

```json
{
  "rid": "rec-7f2a",
  "kind": "route",
  "c": "…"
}
```

Only the route records matter. The others are there to make grep-based guessing expensive.

## Step 1 — Find the weak moduli

RSA is built on `n = p * q`. If `p` and `q` are close, then `n` is close to a perfect square. Fermat's method starts at `a = ceil(sqrt(n))` and checks whether `a² - n` is a square:

```text
a = ceil(sqrt(n))
b² = a² - n
if b² is a perfect square:
    p = a - b
    q = a + b
```

For a correctly generated 2048-bit key, this loop is impractical. For these six keys, the first value of `a` already worked. Zero iterations means the primes were *adjacent* enough that `ceil(sqrt(n))` was the midpoint.

| Key | Fermat iterations |
| --- | ---: |
| `k003` | 0 |
| `k008` | 0 |
| `k014` | 0 |
| `k017` | 0 |
| `k021` | 0 |
| `k023` | 0 |

The solver checks every key with a bounded loop rather than trusting the ids:

```python
def fermat_factor(n, max_iter=1000):
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            if p > 1 and p * q == n:
                return p, q
        a += 1
    return None
```

## Step 2 — Recover the private exponents

Once `p` and `q` are known, the rest is textbook RSA:

```text
φ(n) = (p - 1)(q - 1)
d = e⁻¹ mod φ(n)
m = c^d mod n
```

The decrypted route records begin with `CR5\0`. Each one contains an `N=` field pointing at the next record:

| Route record | Decrypted with | Next |
| --- | --- | --- |
| `rec-7f2a` | `k003` | `rec-19bd` |
| `rec-19bd` | `k008` | `rec-4a61` |
| `rec-4a61` | `k014` | `rec-b035` |
| `rec-b035` | `k017` | `rec-82ce` |
| `rec-82ce` | `k021` | `rec-d914` |
| `rec-d914` | `k023` | final record |

The final plaintext is:

```text
CR5\0FINAL\2|R=7b851e6a|C=a4544b34|T=887e44393ce495c6|K=da34e1270307df06e78dc0326c75b47943137f28d57b8d3a03411713ce05e8be
```

The `K=` field is the 32-byte AES key.

## Step 3 — Decrypt the payload

The payload object uses short field names:

| Field | Meaning |
| --- | --- |
| `n` | AES-GCM nonce |
| `a` | additional authenticated data (hex) |
| `c` | ciphertext (hex) |
| `t` | authentication tag (hex) |

AES-GCM expects the tag appended to the ciphertext:

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

plaintext = AESGCM(aes_key).decrypt(
    bytes.fromhex(payload["n"]),
    bytes.fromhex(payload["c"]) + bytes.fromhex(payload["t"]),
    bytes.fromhex(payload["a"]),
)
print(plaintext.decode())
```

If the key, nonce, AAD, ciphertext, or tag is wrong, decryption raises `InvalidTag` instead of returning garbage. That makes the final step self-checking.

## Flag

```text
CREST{close_enough_was_only_the_first_lock}
```

## What I learned

- **Key generation is part of the attack surface.** A correct algorithm with bad randomness is still broken.
- **Fermat is cheap to test.** A bounded loop over every exported modulus is a useful triage step; you do not need to know which key is weak in advance.
- **Follow the data, not the noise.** The `kind` field and the decrypted `N=` links turn 500 records into a six-step path.
- **AES-GCM is authenticated.** A successful decrypt is also an integrity check, which is a nice way to confirm the recovered key.

## Reproduce

```bash
cd solve
python -m pip install -r requirements.txt
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to Cryptography](../README.md) · [Challenge overview](README.md)
