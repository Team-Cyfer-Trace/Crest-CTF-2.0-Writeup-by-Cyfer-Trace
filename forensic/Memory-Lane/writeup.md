> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:47 p.m.
>
> **Official challenge:** Memory Lane · **Category:** Forensics · **Difficulty:** Hard · **Points:** 550 · **Solves:** 42
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Memory Lane — Forensics Writeup

**Category:** Forensics (memory)  
**Flag:** `ctf7{m3m0ry_w4lk1ng_cr3d_c4rv3}`

## Challenge

A raw memory dump (`memdump.bin`, 3 MiB) from a host running a proprietary credential-manager service. Hints from prior IR notes:

- Process has **no ASLR**, fixed base `0x555555554000`.
- The in-memory record table starts with the 4-byte magic `CRDM`.

## TL;DR

1. Locate `CRDM` headers (3 hits, only 1 is valid).
2. Parse the header → get a seed and a pointer to the head of a linked list of records.
3. Translate virtual addresses to file offsets with `offset = vaddr - 0x555555554000`.
4. Walk the linked list; each record payload is XOR-encrypted with an LCG keystream seeded from `header_seed ^ low32(record_vaddr)`.
5. Record #4 decrypts to the flag.

## Step 1 — Triage

```bash
file memdump.bin           # "data" (no recognizable format, flat raw image)
strings -n 8 memdump.bin | head
```

`strings` output is full of **decoys**: `svc_backup:Passw0rd#99`, `admin:hunter2!2023`, `root:toor_legacy_do_not_use`, AWS example keys, JDBC/Mongo/FTP URLs, etc. None of them is the flag, and there is no `ctf7{` in plaintext (`grep -a 'ctf7{'` is empty), so the flag must be hidden/encrypted.

## Step 2 — Find the record table

```python
import re
[m.start() for m in re.finditer(rb'CRDM', d)]
# [0xfef6e, 0x10edf5, 0x1b3fbe]
```

Header layout (reverse engineered from the hexdump):

| Offset | Size | Field |
|---|---|---|
| 0x00 | 4 | magic `CRDM` |
| 0x04 | 1 | version (`02`) |
| 0x05 | 1 | record count |
| 0x06 | 1 | flags (`00`) |
| 0x07 | 4 | seed (LE u32) |
| 0x0B | 8 | pointer to first record (LE, virtual address) |

The three candidates:

| File offset | count | head pointer | Valid? |
|---|---|---|---|
| `0xfef6e` | 7 | `0x555555594676` | ✅ inside image |
| `0x10edf5` | 3 | `0x555555553000` | ❌ below base |
| `0x1b3fbe` | 3 | `0x555555864000` | ❌ past end of dump (`0x310000` > 3 MiB) |

Two are decoys. The real one is at `0xfef6e` with seed `0xe909e451`.

## Step 3 — Virtual → file offset

The hint about the fixed load address is what makes the pointers usable. The dump is a flat image of the process, so:

```
file_offset = vaddr - 0x555555554000
```

Head record: `0x555555594676 - 0x555555554000 = 0x40676`.

## Step 4 — Walk the linked list

Record layout:

```
+0   u64  next   (virtual address, 0 = end)
+8   u16  length
+10  ...  payload (length bytes, encrypted)
```

Chain (this also confirms the address mapping, since all 7 hops land in range and terminate at `0`):

```
0x555555594676 -> 0x55555575f1c2 -> 0x5555556ed7f5 -> 0x5555556aecba
 -> 0x55555570575e -> 0x5555557e1609 -> 0x5555555b4f91 -> 0
```

Payload lengths: 50, 53, 51, 46, 31, 51, 43. The data is high-entropy, so it is encrypted.

## Step 5 — Break the encryption

Dead ends tried first: single/repeating-key XOR (header seed as key), printable-ASCII column analysis, RC4, shifted keys. None gave readable output.

What cracked it: treat the header seed as a **PRNG seed** and brute force common generators and per-record seed derivations, scoring output by printable-ASCII ratio. A perfect score (1.0) appeared for:

- seed = `header_seed ^ (record_vaddr & 0xffffffff)`
- generator = POSIX-style LCG: `x = x*1103515245 + 12345 (mod 2^32)`
- keystream byte = `(x >> 16) & 0xff`

```python
x = (seed ^ (vaddr & 0xffffffff)) & 0xffffffff
for c in ct:
    x = (1103515245 * x + 12345) & 0xffffffff
    pt.append(c ^ ((x >> 16) & 0xff))
```

## Step 6 — Decrypted records

| # | vaddr | Plaintext |
|---|---|---|
| 0 | `0x555555594676` | `jdbc:postgresql://db01.internal:5432/prod?user=svc` |
| 1 | `0x55555575f1c2` | `https://intranet.corp.local/vault/rotate?token=8f3ac9` |
| 2 | `0x5555556ed7f5` | `mongodb://cluster0.internal:27017/?authSource=admin` |
| 3 | `0x5555556aecba` | `C:\Users\svc_acct\AppData\Local\Temp\creds.tmp` |
| **4** | `0x55555570575e` | **`ctf7{m3m0ry_w4lk1ng_cr3d_c4rv3}`** |
| 5 | `0x5555557e1609` | `mongodb://cluster0.internal:27017/?authSource=admin` |
| 6 | `0x5555555b4f91` | `api_key=sk_live_51Hxxxxxxxxxxxxxxxxxxxxxxxx` |

## Flag

```
ctf7{m3m0ry_w4lk1ng_cr3d_c4rv3}
```

## Solver

See `solve.py` (run: `python3 solve.py memdump.bin`).

## Takeaways

- Fixed base addresses turn raw pointers in a flat dump into direct file offsets.
- Validate candidate headers by checking that their pointers fall inside the image; most `CRDM` hits were decoys.
- A "random-looking" payload next to a 4-byte header field is often a PRNG seed, so check that field before hunting for a key elsewhere.
- Plaintext decoys in `strings` are noise; the real secret was never stored in cleartext.
