> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:06 p.m.
>
> **Official challenge:** Recursion Ward · **Category:** Reverse Engineering · **Difficulty:** Medium · **Points:** 300 · **Solves:** 165
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.
>
> **Original author file:** [source-writeup.docx](source-writeup.docx)

---

# recursion_ward — CTF Writeup

Category: Reverse Engineering · Flag format: CREST{...}

**Flag:** CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}

## Summary

recursion_ward is an x86-64 PIE ELF that takes the candidate flag as argv[1] and prints Access granted. or Access denied.. The validator, check(const char *s, int len), has been control-flow flattened: one while/switch loop over a state variable, with decoy states mixed in. Each real state checks exactly one character of the input and then picks the next state. Walking the state graph from the start state to the accept state recovers the input directly, with no need to run or debug the binary.

## Recon

```text
$ file recursion_ward
ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
```

The strings output shows only usage: %s <flag>, Access granted. and Access denied., plus strlen, printf and a source-file name, check_gen.c. So the flag is not stored as a string; it is encoded in the logic of check.

## Structure of check

The prologue sets up the locals:
- [rbp-0x18] is the input pointer (rdi).
- [rbp-0x1c] is the input length (esi).
- [rbp-0x4] is the state variable, initialised to 0.

The function then has three parts.
1. Dispatcher (0x1219–0x1914). A long ladder of cmp [rbp-0x4], STATE / je BLOCK / jg default pairs. It behaves like a hand-unrolled binary search over about 60 state constants. Anything that is not a known state jumps to 0x250a, which returns 0.

2. State blocks (0x1919–0x24f7). Every real block has the same shape:

```text
cmp  [rbp-0x1c], K        ; length > K ?
jle  fail
mov  rax, [rbp-0x18]
add  rax, K               ; s + K
movzx eax, byte [rax]
cmp  al, CH               ; s[K] == CH ?
jne  fail
mov  [rbp-0x4], NEXT      ; transition
jmp  loop                 ; 0x2511 -> back to 0x1219
fail: mov [rbp-0x4], 0x2329   ; trap state
```

In C terms, each state is if (len > K && s[K] == CH) state = NEXT; else state = 0x2329;.

3. Terminal states.
- 0x2328 (accept) returns len == 0x32. The flag is exactly 50 characters.
- 0x2329 (trap) returns 0.

## The decoys

A second group of blocks, 0x21df to 0x24d0, checks odd characters such as W, O, 9, [, V, ;, >, backtick, space and x. They reuse offsets that real states also check, with contradicting characters. They chain into one another but no real state transitions into them, so they are unreachable from state 0. Following transitions from the start state, instead of reading the function top to bottom, ignores them automatically.

## Solving

The solver does four things:
- Disassembles check with objdump.
- Builds the dispatcher map state -> block address from the cmp [rbp-0x4], X; je Y pairs.
- Parses each block into (offset K, expected char CH, next state).
- Starts at state 0 and follows NEXT until 0x2328, recording s[K] = CH along the way.

```text
import subprocess, re
out = subprocess.check_output(['objdump','-d','-M','intel','--no-show-raw-insn','recursion_ward']).decode()
ins = [(int(a.strip().rstrip(':'),16), b.strip())
       for a,b in (l.split('\t',1) for l in out.split('<check>:')[1].split('\n') if '\t' in l)]

# block address -> (offset, char, next_state)
blocks = {}
for i,(a,t) in enumerate(ins):
    if re.match(r'cmp\s+DWORD PTR \[rbp-0x1c\],0x', t) and 0x1919 <= a < 0x24f7:
        off = ch = nxt = None
        for _,u in ins[i:i+12]:
            if (m := re.match(r'add\s+rax,(0x[0-9a-f]+)', u)): off = int(m[1],16)
            if (m := re.match(r'cmp\s+al,(0x[0-9a-f]+)', u)): ch = int(m[1],16)
            if (m := re.match(r'mov\s+DWORD PTR \[rbp-0x4\],(0x[0-9a-f]+)', u)):
                nxt = int(m[1],16); break
        blocks[a] = (off or 0, ch, nxt)

# dispatcher: state -> block address
disp = {0: 0x1919, 0x8b: 0x1b04}   # these two are reached via the fall-through at the end of the ladder
for i,(a,t) in enumerate(ins):
    m = re.match(r'cmp\s+DWORD PTR \[rbp-0x4\],(0x[0-9a-f]+)', t)
    if m and ins[i+1][1].startswith('je'):
        disp[int(m[1],16)] = int(ins[i+1][1].split()[1], 16)

state, s = 0, {}
while state != 0x2328:
    off, ch, state = blocks[disp[state]]
    s[off] = chr(ch)
print(''.join(s[k] for k in sorted(s)))
```

## The path

The start of the chain is shown below; each step has the form state: s[offset] == char -> next state.

| State | Offset | Char | Next |
| --- | --- | --- | --- |
| 0x0000 | 0 | C | 0x085d |
| 0x085d | 1 | R | 0x0369 |
| 0x0369 | 2 | E | 0x1075 |
| 0x1075 | 3 | S | 0x0515 |
| 0x0515 | 4 | T | 0x0e61 |
| 0x0e61 | 5 | { | 0x0228 |
| 0x0228 | 6 | f | 0x0fc6 |
| … | … | … | … |
| 0x0994 | 48 | h | 0x1103 |
| 0x1103 | 49 | } | 0x2328 |

The accept state is then reached with a length of exactly 50.

Reassembling the 50 characters by offset gives:

```text
CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}
```

## Verification

```text
$ ./recursion_ward 'CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}'
Access granted.
```

## Takeaways
- Flattening hides the order of the checks in the code layout, but the transition graph is still fully explicit. Each state's successor is a constant written right next to its comparison, so the graph can be extracted statically.
- Decoys only help the defender if they are reachable. Because the real path starts at a known state and follows constants, unreachable blocks never need to be analysed.
- Since check compares characters at fixed offsets, there is no hashing or arithmetic to invert. Emulation, symbolic execution or angr would also work, but a 30-line parser is quicker.

**Flag:** CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}
