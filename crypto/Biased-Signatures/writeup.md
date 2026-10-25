> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:38 p.m.
>
> **Official challenge:** Biased Signatures · **Category:** Cryptography · **Difficulty:** Hard · **Points:** 600 · **Solves:** 90
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Biased Signatures (Crypto)

**Flag:** `ctf7{3cds4_n0nc3_b14s_l34ks_k3y}`

## Challenge

> A signing service rolled out a "faster" nonce generator for its ECDSA
> (secp256k1) signatures. Performance went up. Something else went down.
>
> We captured the service's public key and a handful of signatures it
> produced, along with a flag encrypted under its private key. Can you
> recover the key?
>
> Flag format: `ctf7{...}`

### Provided: `readme.txt`

```
Biased Signatures - public parameters
======================================

Curve: secp256k1
n (order): 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Public key Q: (0x439838c44975b105bc12751a905d4ebc7144f212c68b03362ae476d28c8cb7d7, 0x27fb37edf771220f510e8dbdc1a6a8a5d67a57d346e53b7a55ca1926b6fb0c68)

VULNERABILITY (public knowledge, this is what you must exploit):
Every signature below was produced with a broken RNG: the nonce k used
for each ECDSA signature has its top 56 bits forced to zero, i.e.
0 < k < 0x100000000000000000000000000000000000000000000000000.

signatures[i] = { message, h = SHA256(message) mod n, r, s }
  where s = k^-1 * (h + r*d) mod n  (standard ECDSA, d = private key)

Flag encryption (public scheme, only d is secret):
  key = SHA256(d.to_bytes(32, "big"))
  flag_ciphertext = flag_bytes XOR key  (repeating-key XOR, key length 32)
  (see flag_ciphertext_hex in data.json)

Recover d from the biased signatures, then decrypt the flag.
```

### Provided: `data.json`

```json
{
  "curve": "secp256k1",
  "n": "0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141",
  "Qx": "0x439838c44975b105bc12751a905d4ebc7144f212c68b03362ae476d28c8cb7d7",
  "Qy": "0x27fb37edf771220f510e8dbdc1a6a8a5d67a57d346e53b7a55ca1926b6fb0c68",
  "bias_bits": 56,
  "nonce_bound_hex": "0x100000000000000000000000000000000000000000000000000",
  "signatures": [
    {
      "message": "biased-signatures-challenge:message-0",
      "h": "0x6435c3f15a014af2159e62d5b3af02356092f4bd2811a781c6069784f16891d1",
      "r": "0x72ea8afff95e3306f2f39af9aaf2b9e07ecc18c33014c461c31a8bdcfa53af46",
      "s": "0x9a97b618c5c43219bfeb83843e92325378b33450c69a99403f0a97582ecdcdc5"
    },
    {
      "message": "biased-signatures-challenge:message-1",
      "h": "0xc55c79a04deebcfbaa3e4a76915161f536d1aeb39558b7dee2fb455815b980d7",
      "r": "0x755ed7b5d307a4aab1e84374247f4a8467c4c9caa32f419b130cecd37e06174b",
      "s": "0x7d351b6ec99b762b05e3174ac95a3f14de056b8cc4481fcb706d8d862edfb044"
    },
    {
      "message": "biased-signatures-challenge:message-2",
      "h": "0xfc22554ecb7d87bf993ae137800db3cc01536ec87d9aaed4130dbaccccd1d786",
      "r": "0xa674a5625787a6c5e809cf6294a2763cb4e0649aa1db17318d1c624ef9419ecb",
      "s": "0xe8b7790690dd8bfc9e30c8089a965d87af8c3b6b168927347054c29a6a87dbb3"
    },
    {
      "message": "biased-signatures-challenge:message-3",
      "h": "0xcb792d5b42c75cc1c50230e908a7fe14801e0217a3de3b9cd86f188c593955ec",
      "r": "0x901892073cd7db61298896c3992a27e35381fb5b43bf343ab00ebc73a1a4da2f",
      "s": "0x2cb55e91d2ac1ffaf40ab8638c18a5601bf679bae5f9128b6f9a95e47007f8c5"
    },
    {
      "message": "biased-signatures-challenge:message-4",
      "h": "0x2f31e161f775a28144627856046449fa166e9538a3e7fe5f9476bc41255deff5",
      "r": "0x6cbb6f0bd07fac10ad8c5bfafd3be7ddb0f8e7da941e1dc4817fc17563f2ef0b",
      "s": "0xfdb6303db2493db0a8a9974b737cec718b7be53ce50449a66f879b324eec8140"
    },
    {
      "message": "biased-signatures-challenge:message-5",
      "h": "0xf12359507b49dc3746361b112998e67e63442000c9ea50eff7563d5447dd538d",
      "r": "0xc30ed26aa5f04d68755b107e03e9be47976a310e3a34a1ffa4e53fc95aa31fb",
      "s": "0xe7660176de5c2f7a9d4d772f8a84264f622f11b235321319be24bb0ea2424e1f"
    },
    {
      "message": "biased-signatures-challenge:message-6",
      "h": "0xa96205adb09946342e9be235244663188c473c4b4af3918fce1ba875dd4a6dfb",
      "r": "0x7db491bf41431ea00ca6492dfe7b7e6143746c419497fa7de375943423db514",
      "s": "0xaedf8c934094c6fbab23863a19c024d49d7e31b2127744be6e1fafefba3975e9"
    }
  ],
  "flag_ciphertext_hex": "19bcf9fefa365049f77a1e341be2050956e618cf33c2898e4149e6ddee4449d8"
}
```

## Solution

### The bug

The signing service generates ECDSA nonces on secp256k1 with their top 56
bits forced to zero:

```
0 < k < 2^200   (instead of the full 0 < k < n, n ≈ 2^256)
```

That's a classic nonce-bias vulnerability. Standard ECDSA:

```
s = k⁻¹ (h + r·d) mod n
```

Rearranged per signature:

```
k ≡ a·d + b (mod n)
where a = r·s⁻¹ mod n,  b = h·s⁻¹ mod n
```

Each signature gives one linear equation in the unknown private key `d`,
with a small, unknown "error" term `k` (< 2^200). With 7 such equations
this is exactly a **Hidden Number Problem (HNP)** — solvable with lattice
reduction.

### The lattice

Used the standard Boneh–Venkatesan HNP embedding, dimension `t+1 = 8`
(7 signatures + 1 for `d`):

- rows `i = 0..6`: `n² · eᵢ`
- row `7`: `(n·a₀, …, n·a₆, B)`  (`B = 2^200`)
- target vector: `(-n·b₀, …, -n·b₆, 0)`

The whole matrix is pre-scaled by `n` to clear a fractional `B/n` entry
that the textbook construction has, so everything stays in integers. Ran
LLL reduction (delta = 0.99) followed by Babai's nearest-plane algorithm
to find the lattice point closest to the target. The resulting error
vector's first 7 coordinates divide out by `n` to give the `kᵢ` nonces,
and the last coordinate divides out by `B` to give `d` directly.

No SageMath/fpylll were available locally or in WSL, so LLL + Babai's CVP
were implemented in pure Python using exact `Fraction` arithmetic —
dimension 8 kept it fast and reliable.

**Dead end:** first attempt divided *every* coordinate of the embedding
error vector by `n`. That's wrong — only the first 7 coordinates scale by
`n`; the last one (the `d` coordinate) scales by `B`, because only the
last lattice row carries that entry. Fixing that division fixed the whole
attack.

### Result

```
d = 0xa4775eafa69c278510f8e5eafd8212d22b01084b12f87763728ea3bb3f00cb62
```

Verified `d·G == Q` against the given public key — confirmed.

### Decrypting the flag

```
key = SHA256(d.to_bytes(32, "big"))
flag = ciphertext XOR key   (repeating 32-byte key)
```

```
ctf7{3cds4_n0nc3_b14s_l34ks_k3y}
```

## Solve script

The author's referenced `work/solve.py` was not included in the submitted files; the parameter block and recovery recipe above are sufficient to reproduce the key recovery.
