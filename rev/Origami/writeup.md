> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:06 p.m.
>
> **Official challenge:** Origami · **Category:** Reverse Engineering · **Difficulty:** Hard · **Points:** 400 · **Solves:** 193
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.
>
> **Original author file:** [source-writeup.docx](source-writeup.docx)

---

# CTF Writeup: origami

**Event:** CREST CTF7  |  Category: Reverse engineering  |  Attachment: origami (x86-64 ELF, stripped)

**Flag:** CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}

## Challenge

Another access-control binary. Its .data section is obfuscated garbage until the program starts running, so something unpacks before the real check. The task is to find the accepted CREST{...} string.

## 1. Recon

```text
$ file origami
origami: ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
$ ./origami test
Access denied.
```
- The description says statically linked, but it is a small dynamic PIE (about 15 KB) importing puts, printf, strlen, malloc and free.
- strings shows only the usage and granted/denied messages, no flag text.
- .data is 0x1cf bytes at vaddr 0x4000 (file offset 0x3000) and holds the obfuscated blob.
- .init_array points to frame_dummy, so the unpacking is not a constructor. It happens inside the check function.

## 2. Reversing the check

The check function (0x1228) allocates a 0x1ab-byte buffer with malloc and fills it by XORing the .data blob at 0x4020 with a repeating 4-byte key stored at 0x41cb:

```text
for i in 0..0x1aa:
    code[i] = data[0x4020 + i] ^ key[i % 4]     ; key at 0x41cb
```

It then interprets code as bytecode for a small stack VM. State: an instruction pointer, a stack of bytes, a stack pointer, and an accumulator that starts at 1.

| Opcode | Operand | Effect |
| --- | --- | --- |
| 01 | n | push input[n], or 0 if n is past the end of the input |
| 02 | k | top ^= k |
| 03 | r | top = rotate-left-8(top, r & 7) |
| 04 | v | top = (top == v) |
| 05 | none | pop; accumulator = accumulator AND popped value |
| 06 | n | push (strlen(input) == n) |
| ff | none | halt |
| other | none | free, print "Access denied.", exit 1 |

After the loop, the binary prints "Access granted." only if the accumulator is still non-zero.

## 3. Unpacking and disassembling

The key bytes are c4 c0 0c bc. Decoding the blob and disassembling it gives a very regular program:

```text
d = open('origami','rb').read()
enc = d[0x3020:0x3020+0x1ab]
key = d[0x31cb:0x31cb+4]          # vaddr 0x41cb -> file offset 0x31cb
code = bytes(c ^ key[i % 4] for i, c in enumerate(enc))
```

The first block of the decoded program reads:

```text
PUSH_IN 0 ; XOR 46 ; ROL 4 ; EQ 214 ; AND
PUSH_IN 1 ; XOR 148 ; ROL 5 ; EQ 216 ; AND
PUSH_IN 2 ; XOR 216 ; ROL 2 ; EQ 118 ; AND
...
```

There are 47 such blocks, one per input byte, followed by LEN_EQ 47 ; AND ; HALT.

## 4. Solving

Each block constrains one input byte x independently: rol8(x ^ k, r) == v. Brute-forcing x over 0..255 for every block returned exactly one solution each, so the accepted string is unique:

```text
rol = lambda x, b: ((x << (b & 7)) | (x >> (8 - (b & 7)))) & 0xff
sols = [x for x in range(256) if rol(x ^ k, r) == v]
```

Concatenating the 47 bytes gives:

```text
CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}
```

## 5. Verification

```text
$ ./origami 'CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}'
Access granted.
```

## Takeaways
- When .data looks like noise, look for a short XOR loop right before the check. Here the key was stored 4 bytes before the end of .data.
- A VM check is only as strong as its instruction set. Because every block is an independent per-byte constraint, the program can be inverted by brute force without running a debugger or a symbolic executor.
- Writing the 40-line disassembler first made the structure obvious: 47 identical blocks plus a length check.
