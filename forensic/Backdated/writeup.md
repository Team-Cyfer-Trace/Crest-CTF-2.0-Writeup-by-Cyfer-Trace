> **Solved and written by** Parth (`DeadStorm18`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:17 p.m.
>
> **Official challenge:** Backdated · **Category:** Forensics · **Difficulty:** Hard · **Points:** 550 · **Solves:** 87
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Writeup: Timestamp Forgery (journal vs snapshot)

**Flag:** `ctf7{t1m3st4mps_l13_but_j0urn4ls_d0nt}`

## Challenge

`snapshot.bin` holds per-file mtimes, which can be forged. `journal.jsonl` is an append-only log with a monotonically increasing `seq`, so it records the true creation order. The task is to cross-reference the two.

## 1. Parse the journal

It has 12 JSON lines, each in the form `{"seq", "file_id", "action": "CREATE", "ts"}`. Sorting by `seq` gives the real creation order. The `ts` values also increase with `seq`, so the journal is self-consistent.

## 2. Reverse the snapshot format

The file starts with the magic `BKD1`. A hex dump shows the structure, and the parse ends exactly at byte 1046, which confirms the layout:

| Field | Size |
|---|---|
| Magic `BKD1` | 4 |
| File count (big-endian) | 2 (= 12) |
| Per entry: file id | 2 |
| name length | 1 |
| name | n |
| mtime (unix, big-endian) | 4 |
| size | 4 |
| content | `size` bytes |

The `size` field includes a short hex digest that is appended to each file's text (for example `...settings\n2ad3dc86fd8e69c142ca`). Treating that digest as a separate field misaligns the whole parse.

## 3. Cross-reference

Joining on `file_id` and ordering by journal `seq`, the mtimes mostly climb from 2022 to 2026. The exception is the last file created:

| seq | file | claimed mtime |
|---|---|---|
| 11 | draft_proposal.txt | 2026-01-18 |
| **12** | **old_backup_2018.cfg** | **2022-06-20** |

The journal says `old_backup_2018.cfg` was created last, but its mtime is the oldest in the snapshot. A file created last cannot be older than everything else, so its timestamp was backdated. The filename's "2018" is part of the same disguise.

## 4. Extract the flag

The tampered file's content is a base64 string:

```
Y3RmN3t0MW0zc3Q0bXBzX2wxM19idXRfajB1cm40bHNfZDBudH0=
```

Decoding it gives the flag.

## Solver

```python
import struct, json, base64

d = open('snapshot.bin', 'rb').read()
assert d[:4] == b'BKD1'
n = struct.unpack('>H', d[4:6])[0]
p, ents = 6, []
for _ in range(n):
    fid = struct.unpack('>H', d[p:p+2])[0]
    ln = d[p+2]
    name = d[p+3:p+3+ln].decode()
    p += 3 + ln
    mtime, size = struct.unpack('>II', d[p:p+8]); p += 8
    ents.append((fid, name, mtime, d[p:p+size])); p += size

j = {r['file_id']: r for r in map(json.loads, open('journal.jsonl'))}
ents.sort(key=lambda e: j[e[0]]['seq'])

# last-created file should not have the oldest mtime
last = ents[-1]
assert last[2] == min(e[2] for e in ents)
print(last[1], base64.b64decode(last[3]).decode())
```

## Takeaways

- Per-file metadata like mtime is attacker-controlled, so check it against an independent, tamper-evident record such as an append-only journal.
- The disguise, an "ancient" filename plus an old timestamp, only works if nobody compares creation order.
