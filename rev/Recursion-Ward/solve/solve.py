#!/usr/bin/env python3
"""Walk recursion_ward's flattened state graph and recover the accepted flag."""
from pathlib import Path

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent.parent
binary_path = ROOT / "attachments" / "recursion_ward"

with binary_path.open("rb") as fh:
    elf = ELFFile(fh)
    symtab = elf.get_section_by_name(".symtab")
    check = next(sym for sym in symtab.iter_symbols() if sym.name == "check")
    text = elf.get_section_by_name(".text")
    text_base = text["sh_addr"]
    text_data = text.data()
    start = check["st_value"] - text_base
    code = text_data[start:start + check["st_size"]]

md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = [(i.address, i.mnemonic, i.op_str) for i in md.disasm(code, check["st_value"])]

# Dispatcher: cmp dword ptr [rbp - 4], STATE ; je BLOCK
dispatcher: dict[int, int] = {}
for idx, (_, mnemonic, operands) in enumerate(ins):
    if mnemonic == "cmp" and operands.startswith("dword ptr [rbp - 4],"):
        state = int(operands.rsplit(",", 1)[1].strip(), 16)
        if idx + 1 < len(ins) and ins[idx + 1][1] == "je":
            dispatcher[state] = int(ins[idx + 1][2], 16)

# State blocks: length guard, add rax, K, cmp al, CH, mov [rbp-4], NEXT
blocks: dict[int, tuple[int, int, int]] = {}
for idx, (address, mnemonic, operands) in enumerate(ins):
    if mnemonic == "cmp" and operands.startswith("dword ptr [rbp - 0x1c],"):
        offset = 0
        expected = None
        nxt = None
        for _, m2, o2 in ins[idx:idx + 14]:
            if m2 == "add" and o2.startswith("rax,"):
                offset = int(o2.split(",", 1)[1], 16)
            elif m2 == "cmp" and o2.startswith("al,"):
                expected = int(o2.split(",", 1)[1], 16)
            elif m2 == "mov" and o2.startswith("dword ptr [rbp - 4],"):
                nxt = int(o2.rsplit(",", 1)[1], 16)
                break
        if expected is not None and nxt is not None:
            blocks[address] = (offset, expected, nxt)

state = 0
recovered: dict[int, str] = {}
seen: set[int] = set()
while state != 0x2328:
    if state in seen:
        raise SystemExit(f"state loop at {state:#x}")
    seen.add(state)
    block = dispatcher[state]
    offset, expected, state = blocks[block]
    recovered[offset] = chr(expected)

flag = "".join(recovered[i] for i in range(max(recovered) + 1))
print("[*] states followed:", len(seen))
print("[+] FLAG:", flag)
