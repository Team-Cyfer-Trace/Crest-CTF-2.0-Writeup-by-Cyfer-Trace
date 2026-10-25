#!/usr/bin/env python3
"""Ghost Machine — invert each VM block and recover the accepted flag."""
from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = ROOT / "attachments" / "ghostvm"

CODE_OFFSET = 0x82140
CODE_SIZE = 0x1000
KEY_OFFSET = 0x83200
KEY_SIZE = 0x10
SBOX_OFFSET = 0x83100

MASK = 0xFFFFFFFF
NAMES = {
    0xCD: "PUSH",
    0x99: "IN",
    0xCF: "RGET",
    0xEA: "RSET",
    0x5D: "DUP",
    0x17: "ADD",
    0x35: "XOR",
    0x4D: "OR",
    0x1A: "MUL",
    0x68: "ROL",
    0x26: "LEN",
    0xA9: "SBOX",
    0xE8: "JNZ",
    0x60: "HALT",
}


def rol(value: int, count: int) -> int:
    count %= 32
    return value if count == 0 else ((value << count) | (value >> (32 - count))) & MASK


def load_program() -> list[tuple[str, int]]:
    data = BINARY.read_bytes()
    code = data[CODE_OFFSET : CODE_OFFSET + CODE_SIZE]
    key = data[KEY_OFFSET : KEY_OFFSET + KEY_SIZE]
    program = []
    for pc in range(0, CODE_SIZE, 5):
        chunk = bytes(
            (code[pc + i] ^ key[(pc + i) & 15] ^ ((7 * (pc + i)) & 0xFF)) & 0xFF
            for i in range(5)
        )
        name = NAMES.get(chunk[0])
        if name:
            program.append((name, struct.unpack("<I", chunk[1:])[0]))
        if name == "HALT":
            break
    return program


def run(program: list[tuple[str, int]], candidate: bytes) -> bool:
    stack: list[int] = []
    regs = [0] * 8
    for name, arg in program:
        if name == "PUSH":
            stack.append(arg)
        elif name == "IN":
            stack.append(candidate[arg] if arg < len(candidate) else 0)
        elif name == "RGET":
            stack.append(regs[arg & 7])
        elif name == "RSET":
            regs[arg & 7] = stack.pop()
        elif name == "DUP":
            stack.append(stack[-1])
        elif name == "ADD":
            stack[-1] = (stack[-1] + stack.pop()) & MASK
        elif name == "XOR":
            stack[-1] ^= stack.pop()
        elif name == "OR":
            stack[-1] |= stack.pop()
        elif name == "MUL":
            stack[-1] = (stack[-1] * stack.pop()) & MASK
        elif name == "ROL":
            stack[-1] = rol(stack[-1], arg & 31)
        elif name == "LEN":
            stack.append(len(candidate))
        elif name == "SBOX":
            stack[-1] = (arg & 0xFF) ^ SBOX[stack[-1] & 0xFF]
        elif name == "HALT":
            return stack.pop() == 0
    raise RuntimeError("program ended without HALT")


def main() -> None:
    global SBOX
    data = BINARY.read_bytes()
    SBOX = data[SBOX_OFFSET : SBOX_OFFSET + 256]
    program = load_program()

    blocks: list[dict] = []
    current = None
    for name, arg in program:
        if name == "IN":
            current = {"index": arg, "ops": []}
            blocks.append(current)
        if current is not None:
            current["ops"].append((name, arg))

    recovered: dict[int, int] = {}
    previous = 0
    for block in blocks:
        ops = block["ops"]
        sbox_imm = next(arg for name, arg in ops if name == "SBOX")
        rotate = next(arg for name, arg in ops if name == "ROL") & 31
        mul_at = next(i for i, (name, _) in enumerate(ops) if name == "MUL")
        multiplier = ops[mul_at - 1][1]

        reg1_at = next(i for i, (name, arg) in enumerate(ops) if name == "RGET" and arg == 1)
        target_op, target = ops[reg1_at - 2]
        assert target_op == "PUSH"
        x = target

        y = (x * pow(multiplier, -1, 1 << 32)) & MASK
        y = rol(y, (32 - rotate) % 32)
        y = (y - previous) & MASK
        previous = x

        if y >= 256:
            raise RuntimeError(f"block {block['index']}: non-byte intermediate {y}")
        candidates = [c for c in range(256) if (sbox_imm & 0xFF) ^ SBOX[c] == y]
        if len(candidates) != 1:
            raise RuntimeError(f"block {block['index']}: {len(candidates)} S-box candidates")
        recovered[block["index"]] = candidates[0]

    flag = bytes(recovered[i] for i in sorted(recovered))
    print(f"[+] recovered bytes: {flag!r}")
    print(f"[+] VM accepts: {run(program, flag)}")
    print(f"[+] FLAG: {flag.decode()}")


if __name__ == "__main__":
    main()
