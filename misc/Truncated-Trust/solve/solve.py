#!/usr/bin/env python3
"""Truncated Trust — recover a truncated LCG with LLL + Babai, then decrypt.

Pure standard library. Usage:
    python solve/solve.py
    python solve/solve.py path/to/data.json

The default reads ../attachments/data.json.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "attachments" / "data.json"
path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATA
data = json.loads(path.read_text())

M, A, C = data["modulus"], data["multiplier_a"], data["increment_c"]
H, S = data["leaked_outputs"], data["hidden_bits"]
CT = bytes.fromhex(data["flag_ciphertext_hex"])
n = len(H)

# state_i = a^i * s0 + c_i (mod M)
ai = [pow(A, i, M) for i in range(n)]
ci = [0]
for i in range(1, n):
    ci.append((A * ci[-1] + C) % M)
# low_i = a^i * l0 + K_i (mod M)
K = [(ai[i] * (H[0] << S) + ci[i] - (H[i] << S)) % M for i in range(n)]

# Lattice basis: row 0 = (1, a, ..., a^7); rows 1..7 = M * e_i.
B = [[ai[j] for j in range(n)]] + [
    [M if j == i else 0 for j in range(n)] for i in range(1, n)
]
B[0][0] = 1


def dot(x, y):
    return sum(p * q for p, q in zip(x, y))


def gram_schmidt(B):
    Bs, mu = [], [[F(0)] * len(B) for _ in B]
    for i, row in enumerate(B):
        v = [F(x) for x in row]
        for j in range(i):
            mu[i][j] = dot(row, Bs[j]) / dot(Bs[j], Bs[j])
            v = [x - mu[i][j] * y for x, y in zip(v, Bs[j])]
        Bs.append(v)
    return Bs, mu


def lll(B, delta=F(3, 4)):
    B = [r[:] for r in B]
    Bs, mu = gram_schmidt(B)
    k = 1
    while k < len(B):
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [x - q * y for x, y in zip(B[k], B[j])]
                Bs, mu = gram_schmidt(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gram_schmidt(B)
            k = max(k - 1, 1)
    return B


def babai(R, target):
    Bs, _ = gram_schmidt(R)
    b = [F(x) for x in target]
    for i in range(len(R) - 1, -1, -1):
        c = round(dot(b, Bs[i]) / dot(Bs[i], Bs[i]))
        b = [x - c * y for x, y in zip(b, R[i])]
    return b  # residual: target - closest lattice vector


R = lll(B)
mid = 1 << (S - 1)
target = [mid] + [mid - K[i] for i in range(1, n)]
residual = babai(R, target)
l0 = int(target[0] - residual[0])

s0 = (H[0] << S) + l0
states = [s0]
for _ in range(n):
    states.append((A * states[-1] + C) % M)
assert all(states[i] >> S == H[i] for i in range(n)), "recovered seed inconsistent"
print(f"[+] state[0] = {states[0]:#018x}")
print(f"[+] state[8] = {states[8]:#018x}")

key = states[8].to_bytes(8, "big")
for width, endian, start in itertools.product((1, 2, 4, 8), ("big", "little"), (0, 1)):
    stream, counter = b"", start
    while len(stream) < len(CT):
        stream += hashlib.sha256(key + counter.to_bytes(width, endian)).digest()
        counter += 1
    plaintext = bytes(x ^ y for x, y in zip(CT, stream))
    if plaintext.isascii() and plaintext.startswith(b"ctf7{") and plaintext.endswith(b"}"):
        print(f"[+] FLAG: {plaintext.decode()}  (counter: {width}-byte {endian}, start {start})")
