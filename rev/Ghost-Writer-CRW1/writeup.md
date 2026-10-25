> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 11:05 a.m.
>
> **Official challenge:** Ghost Writer CRW1 · **Category:** Reverse Engineering · **Difficulty:** Expert · **Points:** 700 · **Solves:** 138
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Ghost Writer CRW1 — Solve

**Flag:** `ctf7{mips_re_largebin_attack_chain}`

## Stage 1 — MIPS protocol recovery (`gw-client`)

Ran `gw-client` under `qemu-mips` in Kali/WSL, disassembled with radare2 (no PIE,
statically linked). `main()` takes `argv[1] host, argv[2] port`, REPL commands:
`new/edit/delete/view/diag/quit`.

`send_hdr(opcode, id, len)` builds a 16-byte big-endian header and sends it,
followed by raw payload bytes for `new`/`edit`:

```
struct {
    uint32_t magic;  // 0x47575031 = "GWP1"
    uint32_t opcode; // 1=new 2=edit 3=delete 4=view 6=diag (5 unused)
    uint32_t id;     // note slot 0..15
    uint32_t len;    // payload length (new/edit only; 0 otherwise)
} // all fields network byte order (big-endian)
```

## Stage 2 — heap exploit against `noted` (x86-64, non-PIE, glibc 2.36)

`main()` dispatch table (jump table @ 0x4020c0) implements:

- `new(id,len)`  : `notes[id]=malloc(len); sizes[id]=len; read(notes[id],len)`
- `edit(id,len)` : `read(notes[id],len)` — **no bounds re-check, no NULL check**
- `delete(id)`   : `free(notes[id])` — **does not NULL the pointer** → UAF
- `view(id)`     : `write(1, notes[id], sizes[id])`
- `diag`         : `((*g_diag)+0x18)()` — calls through a global function-table
  pointer (`g_diag`, default points to `default_diag` struct whose `+0x18`
  slot holds `diag_default()`). `win()` at `0x4011e6` reads `/flag.txt` and
  writes it back to the client.

### Bug chain

`delete()` frees `notes[id]` but leaves the pointer live → classic UAF via
`edit`/`view` on a "deleted" id.

### Large-bin attack

1. Allocate chunk **P** (size `0x430`, lands in unsorted bin on free, then
   large bin — above the tcache max of `0x408` so it isn't tcache'd).
2. Allocate chunk **Q** (size `0x420` — also above tcache max, smaller than
   P, same `largebin_index` bucket).
3. Guard allocations after each so neither chunk is adjacent to top (no
   auto-consolidation on free).
4. `delete(P)`, then issue an unrelated **large** `malloc` (`>` both P and Q,
   and non-smallbin-range so the "last remainder" fast path doesn't eat it)
   to force `_int_malloc` to drain the unsorted bin and place P alone into
   its large bin (self-referential `fd_nextsize`/`bk_nextsize`).
5. UAF-`edit(P)`: overwrite `P->bk_nextsize` (offset 24 in the user buffer)
   with `&g_diag - 0x20`.
6. `delete(Q)`, then another large forcing `malloc` drains the unsorted bin
   and inserts Q into the *same* large bin as P. Because `Q size < P size`,
   glibc's "smaller than smallest" fast path in the large-bin insertion code
   executes with **no `fd_nextsize`/`bk_nextsize` consistency check**:
   ```
   victim->bk_nextsize = P->bk_nextsize;              // = &g_diag - 0x20
   victim->bk_nextsize->fd_nextsize = victim;          // *(&g_diag) = chunk(Q)
   ```
   This sets `g_diag = chunk_addr(Q)` (`Q_user_ptr - 0x10`).
7. UAF-`edit(Q)`: since `diag` dereferences `*(g_diag)+0x18` = `Q_user_ptr+0x8`,
   write `win()`'s address (`0x4011e6`) at offset 8 of Q's buffer.
8. Send `diag` → server calls `win()`, which reads `/flag.txt` and streams it
   back over the socket.

## Files

- `gw-client`, `noted` — downloaded challenge binaries.
- `exploit.py` — final working exploit (pure stdlib `socket`/`struct`, no
  pwntools needed). Run with `python3 exploit.py` against
  `nc 2.31.70.16 16251`.
