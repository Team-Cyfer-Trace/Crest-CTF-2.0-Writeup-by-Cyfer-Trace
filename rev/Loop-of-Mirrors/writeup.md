> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:05 a.m.
>
> **Official challenge:** Loop of Mirrors · **Category:** Reverse Engineering · **Difficulty:** Expert · **Points:** 1000 · **Solves:** 189
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.
>
> **Original author file:** [source-writeup.docx](source-writeup.docx)

---

# CREST CTF: mirror (Reverse Engineering) Writeup

**Flag:** CREST{pr1sms_tw1st_paths_bef0re_th3_last_echo_7c91d2ab}

Challenge: A stripped Linux x86-64 PIE (mirror, about 22 KB). It prompts reflection> and accepts exactly one flag line in CREST{...} format. Fully offline.

Tools: objdump, Python, Unicorn (CPU emulator). No debugger was available in the sandbox, so I emulated the validator instead.

## 1. Overview

The flag is 55 characters: CREST{ + 48-character body + } (the closing brace is checked at offset 0x36; every character must be in 0x21..0x7e). The body is never compared directly. Instead:
- The 48 body bytes are shuffled by a fixed permutation and split into three 16-byte blocks.
- Each block is run through its own tiny VM program and the result must equal an expected 16-byte value.
- Each VM program is stored encrypted in .rodata and decrypted with a key. Key 0 is a constant of the binary. Key 1 is a hash of block 0's plaintext, and Key 2 is a hash of block 1's plaintext. A wrong block therefore breaks every later stage, which is what "material recovered along the way matters to what follows" means.
- Control flow is hidden behind a hash-chained state machine: the next state value is computed from a running hash plus the stage's pass/fail result, so a failed check silently lands in a dead state instead of branching visibly.

Because every VM operation is invertible, the blocks can be solved one at a time in order.

## 2. Static structure

main (at 0x1050) reads a line, strips CR/LF and calls the validator at 0x1e00(buf, len). The validator is a dispatcher loop that mixes a 64-bit state and a 32-bit counter (0x1470 is the mixer) and compares the result against constants. Handlers in the order they run:

| State | Handler | What it does |
| --- | --- | --- |
| init 0x1ab5f0c3 | 0x203f | Length 0x37, CREST{ prefix, } suffix, charset check |
| 0x11d7ce6b | 0x2268 | Integrity-checks 6 qwords of .rodata, then derives K0 |
| 0xe27b4650 | 0x2062 | Builds the 48-byte permutation from K0 and splits the body into three blocks |
| 0x7a1e90cd | 0x1fcd | 0x17a0(K0, 0, …) decrypts program 0 |
| 0x55c028f4 | 0x23ff | VM-A (0x1310) on block 0, compare |
| 0x9f73341a | 0x245c | K1 = 0x1530(K0, block0) |
| 0x08dcc7e2 | 0x1e92 | 0x17a0(K1, 1, …) decrypts program 1 |
| 0xd4415b7f | 0x249a | Builds 4 key-shuffled S-boxes, VM-B (0x1c30) on block 1, compare |
| 0x6e2f19b8 | 0x26cc | K2 = 0x1530(K1, block1) |
| 0xb756d403 | 0x1f66 | 0x17a0(K2, 2, …) decrypts program 2 |
| 0x3c89ae61 | 0x220b | VM-C (0x1ae0) on block 2, compare, then final state 0xf04d216e means success |

Supporting routines:
- 0x1630 and 0x17a0 form the program decryptor. The result buffer starts with a 16-byte header (two constants passed in r8/r9) that is verified, so a wrong key is detected immediately.
- 0x1530 is a SplitMix-style hash over 16 bytes plus a 64-bit salt. It produces the next key.
- 0x1240 is the 16-byte equality test (XOR plus OR-reduce).

The decrypted buffer layout is: header (16 bytes), then the instructions (8 bytes each), then the expected 16-byte output.

## 3. The three VMs

### VM-A: 4×32-bit registers (0x1310, 36 instructions)

Instruction word (64-bit): op = w & 0xff, d = (w>>8)&0xf, a = (w>>12)&0xf, b = (w>>16)&0xf, imm = (w>>20)&0xfff, s = w>>32. Fields must be below 4 (bits 2–3 of each are rejected). The four dwords of the block are the registers.

| op | Effect | Inverse |
| --- | --- | --- |
| 0 | R[d] ^= rol((s ^ R[b]) + R[a], imm%31+1) | same operation |
| 1 | R[d] += rol(s ^ R[a], imm%31+1) | subtract |
| 2 | R[d] = (s\|1)*R[d] + rol(s ^ 0xa341316c, imm&31) | multiply by modular inverse of s\|1 |
| 3 | swap R[d], R[a] | same |
| 4 | swap if bit imm&31 of R[b] is set | same (checked that b is never d or a) |

The compiler's magic-number division (imm * 0x4211 >> 19) is just imm // 31.

### VM-B: 16 byte registers with S-boxes (0x1c30, 64 instructions)

Four 256-byte S-boxes sit at buf+0x280. They are shuffles of 0..255 seeded from K1, so each is a permutation and can be inverted. Per instruction, k = imm & 3 picks the S-box and c = w>>32 is a byte constant:

| op | Effect |
| --- | --- |
| 0 | B[d] = c + B[b] + S[k][B[d] ^ B[a]] |
| 1 | B[d] += rol8(c ^ B[a], imm%7 + 1) |
| 2 | B[d] = S[k][B[d]] |
| 3 | swap B[d], B[a] |
| 4 | rotate the whole 16-byte vector left by imm%15 + 1 |
| 5 | swap B[d], B[a] if bit imm&7 of B[b] is set |

Inverse: use S^-1, undo additions by subtraction, and rotate the other way.

### VM-C: 20-round ARX network (0x1ae0)

State (A,B,C,D) is the four dwords of the block. Round i (1..20) uses imm, k = w>>32, and r11 = i * 0x7f4a7c15. Each instruction must satisfy (w & 0xcff) == 0xc0.

```text
rc1 = ~imm & 31          rc2 = ((imm>>5)+1) & 31
A1 = ((rol(A,rc1) + B) ^ k)
B1 = rol(B,rc2);   Y = B1 ^ A1
C1 = rol(C,rc1)
e  = rol((imm*0x9e3779b9) ^ (k ^ r11), i) ^ (C1 + D)
D1 = rol(D,rc2);   X = D1 ^ e
imm bit 10 set  -> C' = A1, A' = e   else C' = e, A' = A1
imm bit 11 set  -> D' = Y,  B' = X   else D' = X, B' = Y
```

Every step can be peeled off from the output side (undo the swap choices, then the rotations, XORs and additions in reverse).

## 4. Solving method

Because the programs only decrypt correctly if the earlier blocks are right, the solve is sequential.
- Emulate the validator. I mapped the ELF's PT_LOAD segments into Unicorn, called 0x1e00 directly with a candidate flag, and hooked addresses inside the handlers to dump the decrypted program buffer, the expected output and the key slots. This removes the need to port the decryptor and the hash chain, since the real code runs.
- Permutation. I fed a flag whose body bytes were all distinct (chr(33+i)) and read the blocks back at rsp+0x2c0. That gives perm[j] = body index of block byte j. The permutation does not depend on the input, only on constants: [35,13,19,43,26,11,28,14,12,21,45,3,41,4,32,34,23,40,16,22,37,5,31,7,44,6,30,18,42,29,39,46,2,8,17,25,33,36,38,9,0,10,20,24,47,15,1,27]
- Block 0. Key 0 is input-independent, so program 0 was dumped once and inverted from the expected output at buf+0x130. Result: epb1tt3a_f2scms_.
- Block 1. I rebuilt the flag with block 0 in place so the emulator derived the correct K1 (0x00aef57973eaceb4), then dumped program 1 and the S-boxes. Expected output is at buf+0x210. Result: r7h0hsatd_l_9__a.
- Block 2. With blocks 0 and 1 in place, K2 was correct (0x35503aae0a4acfa6). Program 2's expected output is at buf+0xb0. Result: 1ws_tco1pseebtrh.
- Reassemble. Place block[j] at body position perm[j], then wrap in CREST{ }.

At every stage I checked my Python port by running it forward on the emulator's input and confirming it matched the emulator's output byte for byte, and I re-ran the forward VM on the recovered block to confirm it reproduces the expected value. All recovered blocks are printable ASCII, which was a useful sanity check that the inversion was right.

### Core of the solver (VM-C inverse)

```text
def inv(prog, out):
    A,B,C,D = struct.unpack('<4I', out)
    for i,imm,k,r11 in reversed(list(rounds(prog))):
        rc1 = (~imm) & 31; rc2 = ((imm>>5)+1) & 31
        Y,X = (D,B) if imm & 0x800 else (B,D)
        A1,e = (C,A) if imm & 0x400 else (A,C)
        B1 = Y ^ A1;  D1 = X ^ e
        B0 = ror(B1, rc2);  D0 = ror(D1, rc2)
        C1 = ((e ^ rol(((imm*0x9e3779b9)&M) ^ (k ^ r11), i)) - D0) & M
        C0 = ror(C1, rc1)
        A0 = ror(((A1 ^ k) - B0) & M, rc1)
        A,B,C,D = A0,B0,C0,D0
    return struct.pack('<4I', A,B,C,D)
```

## 5. Result

| Block | Plaintext |
| --- | --- |
| 0 | epb1tt3a_f2scms_ |
| 1 | r7h0hsatd_l_9__a |
| 2 | 1ws_tco1pseebtrh |

After undoing the permutation:

```text
CREST{pr1sms_tw1st_paths_bef0re_th3_last_echo_7c91d2ab}
```

Verification on the real binary:

```text
$ echo 'CREST{pr1sms_tw1st_paths_bef0re_th3_last_echo_7c91d2ab}' | ./mirror
A mirror remembers one reflection.
reflection> The mirror holds.
```

## 6. Takeaways
- When control flow is hidden behind a hash-chained state machine, skip untangling the dispatcher and emulate the function with hooks at the interesting addresses.
- Chained key derivation (each block's plaintext keys the next stage) forces a stage-by-stage solve, but also makes each stage independently solvable once its key is known.
- ARX-style VMs built from add, rotate, XOR, odd-multiply and swap are all invertible. Check for register aliasing (d == a or d == b), which is the one thing that would break a simple reverse pass. Here the program generator never produced it.
