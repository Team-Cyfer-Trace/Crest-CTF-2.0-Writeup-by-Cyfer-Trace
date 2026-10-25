# Constellation — full writeup

[← Back to OSINT](../README.md) · [Challenge overview](README.md)

**Category:** OSINT · **Difficulty:** Hard · **Points:** 350 · **Solves:** 168 · **Flag:** `CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}`

## TL;DR

- Build an undirected adjacency map from `connections`.
- Intersect the neighbour sets of `kestrel`, `fennec`, and `quartz`.
- The intersection contains exactly one account: `nova_7`.
- `nova_7`'s bio is Base64; decode it.

## The brief

`brief.txt` is short and specific:

```text
TASKING
-------
Three accounts of interest: kestrel, fennec, quartz.
We believe a single unidentified account is directly connected to
all three. Identify that account from the attached export and
check what they've put in their bio.
```

The phrase **directly connected to all three** is the whole challenge. It does not ask for a path, a mutual friend chain, or a post history. It asks for one node that shares an edge with each target.

## The export

`nodebook_export.json` has three top-level keys:

| Key | Contents |
| --- | --- |
| `users` | 26 handles and short bios |
| `connections` | Undirected pairs of handles |
| `posts` | Filler posts with no useful information |

The posts are a distraction. The graph and the bios are the signal.

## Step 1 — Build the adjacency map

```python
adj = {}
for a, b in data["connections"]:
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)
```

Because the edges are undirected, each pair is inserted in both directions.

## Step 2 — Intersect the neighbour sets

The three target neighbourhoods are:

| Target | Connected to |
| --- | --- |
| `kestrel` | `ochre`, `marl`, `nova_3`, `pallid`, `talon`, `nova_7`, `birch`, `bramble`, `wren` |
| `fennec` | `birch`, `nova_8`, `bramble`, `pallid`, `nova_4`, `nova_7`, `quartz`, `nova_1`, `nova_2`, `nova_5`, `gable`, `sable` |
| `quartz` | `marl`, `nova_4`, `nova_5`, `fennec`, `ochre`, `talon`, `nova_7`, `hollow` |

`kestrel` and `fennec` share `{birch, pallid, bramble, nova_7}`. Intersecting that with `quartz` removes `birch`, `pallid`, and `bramble`. Only `nova_7` remains.

The near misses are useful to sanity-check the result:

- `ochre` and `talon` touch `kestrel` and `quartz`, but not `fennec`.
- `nova_4` and `nova_5` touch `fennec` and `quartz`, but not `kestrel`.
- `marl` touches `kestrel` and `quartz`, but not `fennec`.

## Step 3 — Read the anomalous bio

Every other bio is a normal sentence: "professional lurker", "ask me about ferns", "coffee, code, repeat". `nova_7`'s bio is:

```text
Q1JFU1R7bXV0dTRsX2ZyMTNuZHNfYXIzX2FfZ3I0cGhfcXUzcnl9
```

The alphabet (`A–Z`, `a–z`, `0–9`), the length being a multiple of four, and the leading `Q1JFU1R7` — which is the Base64 encoding of `CREST{` — all point to Base64.

```bash
echo 'Q1JFU1R7bXV0dTRsX2ZyMTNuZHNfYXIzX2FfZ3I0cGhfcXUzcnl9' | base64 -d
```

## Flag

```text
CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}
```

## What I learned

- **Read the wording precisely.** "Directly connected to all three" is a one-hop intersection, not a shortest-path problem.
- **Use the structure of the data.** With 26 users, a manual pass is possible, but a five-line adjacency map is faster and provable.
- **Look for the odd field.** In a dataset where every bio is prose, a Base64 string is not subtle once you stop reading the visible text as the only content.

## Reproduce

```bash
cd solve
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to OSINT](../README.md) · [Challenge overview](README.md)
