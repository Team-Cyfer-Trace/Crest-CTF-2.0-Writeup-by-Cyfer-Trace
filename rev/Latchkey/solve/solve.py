#!/usr/bin/env python3
"""Recover the accepted string from latchkey's XOR-split DFA tables."""
from pathlib import Path
import collections
import struct

ROOT = Path(__file__).resolve().parent.parent
binary = (ROOT / "attachments" / "latchkey").read_bytes()

# .data is mapped at vaddr 0x4000, file offset 0x3000.
# Two 46*256-entry u16 transition tables live at 0x4020 and 0x9c20.
N = 46 * 256
T1 = struct.unpack_from(f"<{N}H", binary, 0x3020)
T2 = struct.unpack_from(f"<{N}H", binary, 0x8c20)
ACCEPT = 0x2C
DEAD = 0x2D


def step(state: int, ch: int) -> int:
    index = (state << 8) + ch
    return T1[index] ^ T2[index]


# Breadth-first search over the DFA, ignoring the dead state.
prev: dict[int, tuple[int, int] | None] = {0: None}
queue = collections.deque([0])
while queue:
    state = queue.popleft()
    for ch in range(256):
        nxt = step(state, ch)
        if nxt != DEAD and nxt not in prev:
            prev[nxt] = (state, ch)
            queue.append(nxt)

if ACCEPT not in prev:
    raise SystemExit("accept state is unreachable")

out = bytearray()
state = ACCEPT
while prev[state] is not None:
    state, ch = prev[state]
    out.append(ch)
flag = bytes(reversed(out)).decode()
print("[*] states visited:", len(prev))
print("[+] FLAG:", flag)
