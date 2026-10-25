# Reverse Engineering

Reading binaries against their will. Custom VMs, flattened control flow, packed sections, and checks that only look opaque.

**Team result:** 6 of 7 cleared · **Published writeups:** 6 (1 personal, 5 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Ghost Machine](Ghost-Machine/) | Ishant Choudhary (`griffin-dox`) | Medium | 850 | 145 | [read](Ghost-Machine/writeup.md) |
| [Loop of Mirrors](Loop-of-Mirrors/) | Parth (`DeadStorm18`) | Expert | 1000 | 189 | [read](Loop-of-Mirrors/writeup.md) |
| [Latchkey](Latchkey/) | Parth (`DeadStorm18`) | Medium | 250 | 220 | [read](Latchkey/writeup.md) |
| [Recursion Ward](Recursion-Ward/) | Parth (`DeadStorm18`) | Medium | 300 | 165 | [read](Recursion-Ward/writeup.md) |
| [Origami](Origami/) | Parth (`DeadStorm18`) | Hard | 400 | 193 | [read](Origami/writeup.md) |
| [Ghost Writer CRW1](Ghost-Writer-CRW1/) | Hrishikesh (`hrishikesh`) | Expert | 700 | 138 | [read](Ghost-Writer-CRW1/writeup.md) |

## Still open

| Challenge | Difficulty | Solves |
| --- | --- | ---: |
| Compiler Fingerprint | Hard | 0 |

## Notes

- `Ghost Machine` is a custom VM with 14 real opcodes and a 256-bit state; the solver disassembles the VM bytecode and inverts the checker.
- `Ghost Writer CRW1` reverses a big-endian MIPS client protocol, then exploits a large-bin UAF in the x86-64 backend.
- `Latchkey` splits a DFA transition table across two XOR-shared tables; the solver reconstructs the accepting path.
- `Loop of Mirrors` encrypts three blocks with three hash-chained VM programs; the author emulated the validator with Unicorn.
- `Origami` XOR-unpacks a per-byte VM and inverts XOR/ROL constraints directly.
- `Recursion Ward` flattens its checker into a state machine; the solver follows the real state graph from start to accept.

---

[← All categories](../README.md) · [All writeups](../README.md)
