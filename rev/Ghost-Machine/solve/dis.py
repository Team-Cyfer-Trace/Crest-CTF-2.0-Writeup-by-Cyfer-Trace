#!/usr/bin/env python3
"""Disassemble the Ghost Machine bytecode stored in the ghostvm binary."""
from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = ROOT / "attachments" / "ghostvm"

CODE_OFFSET = 0x82140
CODE_SIZE = 0x1000
KEY_OFFSET = 0x83200
KEY_SIZE = 0x10

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


def main() -> None:
    data = BINARY.read_bytes()
    code = data[CODE_OFFSET : CODE_OFFSET + CODE_SIZE]
    key = data[KEY_OFFSET : KEY_OFFSET + KEY_SIZE]

    for pc in range(0, CODE_SIZE, 5):
        chunk = bytes(
            (code[pc + i] ^ key[(pc + i) & 15] ^ ((7 * (pc + i)) & 0xFF)) & 0xFF
            for i in range(5)
        )
        opcode = chunk[0]
        argument = struct.unpack("<I", chunk[1:])[0]
        print(f"{pc:04x}  {NAMES.get(opcode, f'0x{opcode:02x}'):<6} 0x{argument:08x}")
        if opcode == 0x60:
            break


if __name__ == "__main__":
    main()
