#!/usr/bin/env python3
"""Invert origami's XOR-unpacked per-byte VM constraints."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
binary = (ROOT / "attachments" / "origami").read_bytes()

# .data blob at vaddr 0x4020 (file 0x3020), 4-byte XOR key at vaddr 0x41cb.
enc = binary[0x3020:0x3020 + 0x1AB]
key = binary[0x31CB:0x31CB + 4]
code = bytes(c ^ key[i % 4] for i, c in enumerate(enc))


def rol8(value: int, amount: int) -> int:
    amount &= 7
    return ((value << amount) | (value >> ((8 - amount) & 7))) & 0xFF


out = bytearray()
i = 0
while i < len(code) and code[i] == 0x01:
    # PUSH_IN n; XOR k; ROL r; EQ v; AND
    op_push, n, op_xor, k, op_rol, r, op_eq, v, op_and = code[i:i + 9]
    if (op_push, op_xor, op_rol, op_eq, op_and) != (0x01, 0x02, 0x03, 0x04, 0x05):
        raise SystemExit(f"unexpected block at {i:#x}")
    candidates = [x for x in range(256) if rol8(x ^ k, r) == v]
    if len(candidates) != 1:
        raise SystemExit(f"block {n}: {len(candidates)} candidates")
    out.append(candidates[0])
    i += 9

tail = code[i:]
if tail != bytes.fromhex("062f05ff"):
    raise SystemExit(f"unexpected tail: {tail.hex()}")
print("[*] decoded bytes:", len(out))
print("[+] FLAG:", out.decode())
