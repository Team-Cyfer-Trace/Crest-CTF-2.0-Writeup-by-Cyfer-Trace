# Truncated Trust — full writeup

[← Back to Miscellaneous](../README.md) · [Challenge overview](README.md)

**Category:** Miscellaneous · **Difficulty:** Hard · **Points:** 600 · **Solves:** 91 · **Flag:** `ctf7{trunc4t3d_lcg_l4tt1c3_r3c0v3ry}`

## TL;DR

- The LCG is `s[i+1] = (a * s[i] + c) mod 2^64`, with public `a`, `c`, and modulus.
- Eight outputs leak `s[i] >> 40` (the top 24 bits). The low 40 bits are unknown.
- The only free variable is the low 40 bits of the seed, `l0`. Each leaked state gives a linear congruence in `l0` plus a small unknown.
- That is a Hidden Number Problem-style closest-vector problem. LLL + Babai recovers `l0`.
- Rebuild the recurrence to `s[8]`, derive the SHA-256 keystream, and try counter encodings.

## The generator

```text
s[i+1] = (a * s[i] + c) mod m
m = 2^64
```

The parameters are public:

```text
m = 18446744073709551616
a = 11110795144557789151
c = 5152819025229729726
```

The leaked values are the top 24 bits of eight consecutive states:

```text
5360055, 10083526, 1362311, 721806, 2864540, 13840525, 12152733, 11334751
```

Since `s[i] >> 40` is known, write:

```text
s[i] = (H[i] << 40) + low[i]
0 <= low[i] < 2^40
```

Only `l0 = low[0]` is independent. Every later state is a function of it:

```text
s[i] = a^i * s[0] + c_i (mod 2^64)
low[i] = a^i * l0 + K[i] (mod 2^64)
```

where `K[i]` folds in the known high bits and the accumulated increment.

## The lattice

The unknowns are `l0` and the seven `low[1..7]` values, each constrained to a `2^40` box modulo `2^64`. Build the basis:

```text
row 0      = (1, a, a^2, ..., a^7)
row i (1..7) = 2^64 * e_i
```

The lattice contains the vector of low parts. Reduce it with LLL, then use Babai's nearest-plane algorithm to find the closest vector to the centre of the box:

```text
target = (2^39, 2^39 - K[1], ..., 2^39 - K[7])
```

The first coordinate of the recovered vector is `l0`.

```python
R = lll(B)
mid = 1 << (S - 1)
target = [mid] + [mid - K[i] for i in range(1, n)]
residual = babai(R, target)
l0 = int(target[0] - residual[0])
```

## Recover the states

```python
s0 = (H[0] << S) + l0
states = [s0]
for _ in range(n):
    states.append((A * states[-1] + C) % M)
assert all(states[i] >> S == H[i] for i in range(n))
```

The check is important: it proves the recovered low bits are consistent with every leaked high part, not just the first one.

Output:

```text
state[0] = 0x51c9b7eb4157371c
state[8] = 0x1a664328ca81141c
```

## Decrypt the flag

`README.txt` specifies:

```text
key_bytes = state[8].to_bytes(8, "big")
keystream = SHA256(key_bytes || counter) || SHA256(key_bytes || counter+1) || ...
ciphertext = flag_bytes XOR keystream[:len(flag_bytes)]
```

The counter serialization is not specified. The solver tries widths `{1, 2, 4, 8}`, both endiannesses, and start values `{0, 1}`:

```python
for width, endian, start in itertools.product((1, 2, 4, 8), ("big", "little"), (0, 1)):
    stream, counter = b"", start
    while len(stream) < len(CT):
        stream += hashlib.sha256(key + counter.to_bytes(width, endian)).digest()
        counter += 1
    plaintext = bytes(x ^ y for x, y in zip(CT, stream))
    if plaintext.startswith(b"ctf7{"):
        print(plaintext.decode())
```

Only **4-byte big-endian, starting at 0** produces a clean flag. The 4-byte little-endian variant matches the first block by coincidence, then turns to garbage, which is a useful reminder to validate the whole plaintext rather than just the prefix.

## Flag

```text
ctf7{trunc4t3d_lcg_l4tt1c3_r3c0v3ry}
```

## What I learned

- **Truncated output is not protection.** Known `a`, `c`, and `m` plus enough outputs turn the hidden bits into a lattice problem.
- **One unknown can be enough.** All eight low parts are determined by `l0`; the lattice encodes that dependency.
- **Verify with the leak.** The recovered seed must reproduce every known high part.
- **Keystream specs need exact serialization.** The counter width, endianness, and start value are part of the cryptographic contract, even when the hash is standard.

## Reproduce

```bash
cd solve
python solve.py
```

The solver is pure standard library. Full script: [`solve/solve.py`](solve/solve.py)

The provided Z3 model: [`attachments/script.py`](attachments/script.py) (requires `z3-solver`).

---

[← Back to Miscellaneous](../README.md) · [Challenge overview](README.md)
