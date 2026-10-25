# Ghost Machine — full writeup

[← Back to Reverse Engineering](../README.md) · [Challenge overview](README.md)

**Category:** Reverse Engineering · **Difficulty:** Medium · **Points:** 850 · **Solves:** 145 · **Flag:** `CREST{d1s4ss3mbl3_th3_v01d}`

## TL;DR

- `ghostvm` is a stripped, statically linked x86-64 ELF. Running it with a wrong input prints `Nope.`
- `main` builds a 256-entry table of function pointers, installs 14 real handlers, and hands control to a VM.
- The VM executes 5-byte instructions: one opcode byte and a 32-bit little-endian argument.
- The bytecode is encrypted with a repeating XOR and a position-dependent rotate.
- The checker has one block per input character. Every operation is invertible, so the flag falls out backwards.

## Recon

The binary is static and stripped. The useful strings are in `.rodata`:

| Address | String |
| --- | --- |
| `0x480010` | `Access granted.` |
| `0x480020` | `Nope.` |
| `0x480026` | `ghost> ` |

Following the references from the entry point at `0x401830` shows the setup:

1. Fill a 256-entry function-pointer table at `0x4adb20` with a default no-op handler (`0x401d10`).
2. Overwrite 14 entries with real handlers.
3. Print `ghost> ` and read the input into `0x4ae340`; the length goes to `0x4ae320`.
4. Call the VM at `0x401d60`. A non-zero return prints `Access granted.`

A table of function pointers set up in `main` is the classic shape of a bytecode VM. Mapping the table index to each handler address gives the opcode set directly.

## The VM

The VM state is a 0x148-byte stack struct:

| Offset | Field |
| --- | --- |
| `+0x000` | data stack, 64 dwords |
| `+0x100` | stack pointer |
| `+0x104` | `r0`–`r7` |
| `+0x124` | program counter |
| `+0x128` | running flag |
| `+0x12c` | result |

### Fetch and decode

The bytecode is stored encrypted at virtual address `0x482140`. In the file, the same bytes are at offset `0x82140`. Each instruction is five bytes:

```text
opcode = 1 byte
argument = 4 bytes, little-endian
```

Byte `i` is decoded as:

```text
plain[i] = code[i] XOR key[i & 15] XOR ((7 * i) & 0xff)
```

The 16-byte key is at file offset `0x83200`; the S-box is at `0x83100`. The program counter advances by five bytes per instruction.

### Opcodes

| Opcode | Mnemonic | Semantics |
| ---: | --- | --- |
| `0xcd` | `PUSH` | Push the 32-bit immediate |
| `0x99` | `IN` | Push `input[imm]`, or 0 if out of range |
| `0xcf` | `RGET` | Push `reg[imm & 7]` |
| `0xea` | `RSET` | Pop into `reg[imm & 7]` |
| `0x5d` | `DUP` | Duplicate the top of stack |
| `0x17` | `ADD` | Add the top two values |
| `0x35` | `XOR` | XOR the top two values |
| `0x4d` | `OR` | OR the top two values |
| `0x1a` | `MUL` | Multiply the top two values |
| `0x68` | `ROL` | Rotate the top value left by `imm` |
| `0x26` | `LEN` | Push the input length |
| `0xa9` | `SBOX` | `top = (imm & 0xff) XOR sbox[top & 0xff]` |
| `0xe8` | `JNZ` | Pop; if non-zero, set `pc = imm` |
| `0x60` | `HALT` | Pop `v`; result is `(v == 0)` |
| other | `NOP` | Do nothing (junk padding) |

## The checker program

The program starts with a length check:

```text
LEN; PUSH 0x1b; XOR; RSET r1     ; r1 = len ^ 27
```

It then runs one fixed block for each of the 27 input characters:

```text
IN i
SBOX k_i
RGET r0 ; ADD                   ; + previous x
ROL n_i
PUSH m_i ; MUL                  ; x = (...) * m_i
DUP ; RSET r0                   ; r0 = x, carried to the next block
DUP ; PUSH c1 ; XOR ; RSET r3
DUP ; RGET r2 ; XOR ; RSET r2   ; r2 ^= x
PUSH c2 ; XOR ; RGET r1 ; OR ; RSET r1   ; r1 |= (x ^ c2)
```

At the end, the program pushes `r1` and halts. It accepts only when `r1 == 0`, which requires:

- `len == 27`, and
- `x_i == c2_i` for every block.

## Solving backwards

Each block is a chain of invertible operations. The multipliers `m_i` are odd, so they have inverses modulo `2^32`. For each block, in program order:

1. Start with `x = c2_i`.
2. `y = ROR(x * m_i⁻¹, n_i) - r0_prev (mod 2^32)`.
3. `r0_prev = x`.
4. Find the byte `c` satisfying `(k_i & 0xff) XOR sbox[c] == y`.
5. The `IN i` argument gives that byte's position in the flag.

The S-box is a permutation, so the lookup has exactly one candidate per block. The recovered bytes form the flag directly.

```python
y = (x * pow(multiplier, -1, 1 << 32)) & 0xffffffff
y = rol(y, (32 - rotate) % 32)
y = (y - previous) & 0xffffffff
previous = x
byte = next(c for c in range(256) if (sbox_imm & 0xff) ^ SBOX[c] == y)
```

## Verification

The solver also contains a forward VM emulator. Running the recovered flag through it returns `True`:

```text
[+] recovered bytes: b'CREST{d1s4ss3mbl3_th3_v01d}'
[+] VM accepts: True
```

Against the real binary:

```bash
echo "CREST{d1s4ss3mbl3_th3_v01d}" | ./ghostvm
# ghost> Access granted.
```

## Flag

```text
CREST{d1s4ss3mbl3_th3_v01d}
```

## What I learned

- **Function-pointer tables are a VM tell.** A 256-entry table with a default no-op and a handful of real handlers is a compact way to build an interpreter.
- **Junk opcodes are not a problem.** The entries still pointing at the default handler are padding; ignore them.
- **Invertible operations are meant to be reversed.** Add, rotate, odd multiply, and a permutation S-box need no brute force or symbolic execution.
- **Verify the recovery.** A forward emulator turns a plausible flag into a proven one.

## Reproduce

```bash
cd solve
python dis.py | less       # full disassembly
python solve.py            # inverse solve + forward verification
```

Full scripts: [`solve/dis.py`](solve/dis.py) · [`solve/solve.py`](solve/solve.py)

---

[← Back to Reverse Engineering](../README.md) · [Challenge overview](README.md)
