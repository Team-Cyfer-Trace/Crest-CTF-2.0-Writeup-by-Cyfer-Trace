# Ghost Machine

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-Reverse_Engineering-4B4E8C?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-7A5A12?style=flat-square)
![Points](https://img.shields.io/badge/Points-850-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-145-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

It asks for a flag. It says yes or no. The interesting logic is not in native code — it runs inside something the binary built for itself. Learn the machine, then the program on it.

Run: `chmod +x ghostvm`, then `./ghostvm` and enter your flag at the `ghost>` prompt.

**Attachment:** [`ghostvm`](attachments/ghostvm)

## Flag

```text
CREST{d1s4ss3mbl3_th3_v01d}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** the binary sets up a 256-entry handler table, populates 14 opcodes, and runs an encrypted 5-byte-instruction VM; the 27-character checker uses only invertible operations, so each input byte can be recovered backwards.

- The VM bytecode is XOR/rotate encrypted at file offset `0x82140`.
- The opcode set includes `PUSH`, `IN`, `RGET`, `RSET`, `DUP`, `ADD`, `XOR`, `OR`, `MUL`, `ROL`, `LEN`, `SBOX`, `JNZ`, and `HALT`.
- The checker is 27 identical blocks, one per input character.
- The flag is recovered by inverting the S-box, rotate, multiply, and add, then verified by the VM.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/ghostvm`](attachments/ghostvm) | Stripped, statically linked x86-64 ELF |
| [`solve/dis.py`](solve/dis.py) | Bytecode decoder / disassembler |
| [`solve/solve.py`](solve/solve.py) | Inverse solver and forward VM verifier |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output:

```text
[+] recovered bytes: b'CREST{d1s4ss3mbl3_th3_v01d}'
[+] VM accepts: True
[+] FLAG: CREST{d1s4ss3mbl3_th3_v01d}
```

Disassemble the full program with:

```bash
python dis.py | less
```

## Notes

- The VM uses 32-bit wrapping arithmetic. Every multiplier in the checker is odd, so it has a modular inverse modulo `2^32`.
- The default handler is a no-op, which is why the disassembly contains many junk opcodes. The real instruction set is the 14 entries that point at actual handlers.
- `ghostvm` is included for reproducibility. Do not run untrusted binaries outside an isolated environment.

---

[← Back to Reverse Engineering](../README.md) · [All writeups](../../README.md)
