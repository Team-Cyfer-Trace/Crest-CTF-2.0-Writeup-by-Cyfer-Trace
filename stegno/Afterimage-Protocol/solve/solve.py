#!/usr/bin/env python3
"""Reproduce the final Afterimage Protocol layer from the original PNG."""
from pathlib import Path
import hashlib
import struct
import zlib

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
image_path = ROOT / "attachments" / "afterimage.png"
im = np.array(Image.open(image_path).convert("RGB")).astype(np.int64)
height, width, _ = im.shape
red, green, blue = im[..., 0], im[..., 1], im[..., 2]

normalized = im.copy()
normalized[..., 0] &= 0xFE
normalized[..., 1] &= 0xFD
normalized[..., 2] &= 0xFE
yy, xx = np.mgrid[0:height, 0:width]
rn, gn, bn = normalized[..., 0], normalized[..., 1], normalized[..., 2]
pool = ((((rn >> 2) * 11) + ((gn >> 2) * 17) + ((bn >> 2) * 23) + (xx * 5) + (yy * 7)) & 15)
mask = np.isin(pool, (2, 5, 9))
ys0, xs0 = np.nonzero(mask)
count = len(ys0)
print(f"[*] image {width}x{height}, pool {count} pixels")

MASK64 = (1 << 64) - 1


class PCG:
    def __init__(self, state: int, sequence: int):
        self.state = 0
        self.increment = ((sequence << 1) | 1) & MASK64
        self.next()
        self.state = (self.state + state) & MASK64
        self.next()

    def next(self) -> int:
        old = self.state
        self.state = (old * 6364136223846793005 + self.increment) & MASK64
        x = (((old >> 18) ^ old) >> 27) & 0xFFFFFFFF
        rot = old >> 59
        return ((x >> rot) | (x << ((-rot) & 31))) & 0xFFFFFFFF


def blake2s(data: bytes, key: bytes = b"", size: int = 32) -> bytes:
    return hashlib.blake2s(data, digest_size=size, key=key).digest()


case = b"NSR-0217"
a = bytes.fromhex("7a1c39e24fd865b0")
b = bytes.fromhex("e9136cb2a04f7d58")
nonce = bytes.fromhex("051160a96d7b299f")
digest = hashlib.sha256(normalized.astype(np.uint8).tobytes()).digest()
seed = blake2s(b"AP3/PCG\0" + digest + case + a + b + nonce)
rng = PCG(int.from_bytes(seed[0:8], "little"), int.from_bytes(seed[8:16], "little"))
order = np.arange(count)
for i in range(count - 1, 0, -1):
    j = rng.next() % (i + 1)
    order[i], order[j] = order[j], order[i]
ys, xs = ys0[order], xs0[order]
bits = ((green[ys, xs] >> 1) & 1).astype(np.uint8)[:109 * 8]
packed = np.packbits(bits).tobytes()
if packed[:4] != b"AP3F":
    raise SystemExit("bad AP3 layer header")
ct_len = struct.unpack(">I", packed[6:10])[0]
ciphertext = packed[10:10 + ct_len]
tag = packed[10 + ct_len:26 + ct_len]
k_enc = blake2s(b"AP3/ENC\0" + digest + case + a + b + nonce)
k_tag = blake2s(b"AP3/TAG\0" + digest + case + a + b + nonce)
expected = blake2s(b"AP3/AUTH\0" + packed[:10] + ciphertext, k_tag, 16)
if expected != tag:
    raise SystemExit("authentication tag mismatch")
keystream = b"".join(
    blake2s(b"AP3/KS\0" + nonce + struct.pack(">I", i), k_enc)
    for i in range((ct_len + 31) // 32)
)
plaintext = bytes(x ^ y for x, y in zip(ciphertext, keystream))
final = zlib.decompress(plaintext).decode()
print(final)
for line in final.splitlines():
    if line.startswith("proof="):
        print("[+] FLAG:", line.split("=", 1)[1])
