> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:03 p.m.
>
> **Official challenge:** Latchkey · **Category:** Reverse Engineering · **Difficulty:** Medium · **Points:** 250 · **Solves:** 220
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.
>
> **Original author file:** [source-writeup.docx](source-writeup.docx)

---

# CTF Writeup: latchkey

**Event:** CREST CTF7  |  Category: Reverse engineering  |  Attachment: latchkey (x86-64 ELF, stripped)

**Flag:** CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}

## Challenge

A small access-control binary takes one string and prints only "Access granted." or "Access denied.". There are no helpful strings or errors. The task is to work out how it decides, then submit the accepted CREST{...} string.

## 1. Recon

```text
$ file latchkey
latchkey: ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
$ ./latchkey test
Access denied.
```
- The description says statically linked, but it is a small dynamic PIE (about 60 KB) that imports only puts, strlen and printf.
- strings shows the usage and granted/denied messages and no flag text.
- The .data section is large (0xb820 bytes), which hints at lookup tables.

## 2. Reversing the check

The real logic is a single function reached from __libc_start_main (0x1189). Annotated from the disassembly:

```text
s = 0                      ; [rbp-0x1c]
for i in range(len(argv[1])):
    if s == 0x2d: break    ; dead state
    idx = (s << 8) + argv[1][i]
    a = T1[idx]            ; u16 table at 0x4020
    b = T2[idx]            ; u16 table at 0x9c20
    s = a ^ b
    if s == 0x2c:          ; accept state
        if i == len-1: puts("Access granted."); return 0
        s = 0x2d           ; accept reached too early -> dead
if s == 0x2c: granted else denied
```

So the binary is a deterministic finite automaton (DFA). Each transition is stored as two XOR-masked halves in separate tables, which is why no flag bytes show up in strings. The tables are 0x5c00 bytes each, which is 46 states x 256 bytes x 2 bytes.
- Start state: 0
- Accept state: 0x2c (44)
- Dead state: 0x2d (45)
- Accept only counts if reached exactly on the last input byte.

## 3. Extracting the automaton

.data is mapped at vaddr 0x4000 and file offset 0x3000, so the tables sit at file offsets 0x3020 and 0x8c20.

```text
import struct
d = open('latchkey','rb').read()
N = 46*256
t1 = struct.unpack_from('<%dH'%N, d, 0x3020)
t2 = struct.unpack_from('<%dH'%N, d, 0x8c20)
nxt = lambda s,c: t1[(s<<8)+c] ^ t2[(s<<8)+c]
```

All computed next states fall in 1..45, which confirms the table layout.

## 4. Solving

I did a BFS from state 0 to state 44 over the transition graph, skipping the dead state:

```text
import collections
prev = {0: None}; q = collections.deque([0])
while q:
    s = q.popleft()
    for c in range(256):
        n = nxt(s, c)
        if n != 0x2d and n not in prev:
            prev[n] = (s, c); q.append(n)
# walk prev[44] back to 0 to recover the string
```

Printing the printable out-edges of each state shows that states 0 to 43 each have exactly one non-dead transition, one per flag character, in order. State 44 only loops to itself, and the binary treats reaching it before the last byte as a dead end, so any trailing byte is rejected. The accepted language therefore contains exactly one string:

```text
CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}
```

## 5. Verification

```text
$ ./latchkey 'CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}'
Access granted.
$ ./latchkey 'CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}x'
Access denied.
```

The trailing-byte case matches the "accept only on the last byte" rule from section 2.

## Takeaways
- When asked how a checker decides rather than what it compares, look for a table-driven state machine instead of string compares.
- XOR-splitting a table across two arrays defeats strings and naive pattern searches, but it is trivial to recombine once the indexing is known.
- Extracting the full transition table and searching the graph (BFS) is faster and more reliable than tracing the binary in a debugger, and it proves the solution is unique.
