# Ghost Domain — full writeup

[← Back to OSINT](../README.md) · [Challenge overview](README.md)

**Category:** OSINT · **Difficulty:** Medium · **Points:** 200 · **Solves:** 302 · **Flag:** `CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}`

## TL;DR

1. `zone_dump.json` contains 19 DNS records. Five TXT records carry `frag=` values and a `serial_ref`.
2. `ops_changelog.json` supplies a `change_serial` for every host. The serials agree with the zone's `serial_ref`.
3. Sort the five fragments by serial ascending, concatenate, and Base32-decode.
4. The result is the flag — no semantic reordering needed.

## The leak

Two files:

| File | Contents |
| --- | --- |
| `zone_dump.json` | A zone transfer for `meridianlabs.ctf` |
| `ops_changelog.json` | 20 internal change entries keyed by host and serial |

The challenge text warns that "neither file reveals the complete picture on its own" and "not every record deserves your trust." The first clue says **join** the files; the second says **filter** the records.

## Step 1 — Find the fragments

Only five TXT records have both an encoded payload and a serial reference:

```json
{
  "name": "stage.meridianlabs.ctf",
  "type": "TXT",
  "serial_ref": 2024010209,
  "value": "frag=INJEKU2UPN5DA3RT"
}
```

The other TXT records are ordinary SPF or domain-verification entries:

```text
v=spf1 include:_spf.example.net ~all
MS=ms-fake-verification-code
```

They look plausible, which is the point. They have no `frag=` and no `serial_ref`, so they never enter the reconstruction.

## Step 2 — Join the zone and the changelog

The changelog is a host → serial map. Every fragment host appears in it:

| Host | `change_serial` | Changelog note |
| --- | ---: | --- |
| `stage.meridianlabs.ctf` | `2024010209` | TXT record rotated |
| `portal.meridianlabs.ctf` | `2024010268` | SPF/verification updated |
| `mx2.meridianlabs.ctf` | `2024011069` | TXT record rotated |
| `git.meridianlabs.ctf` | `2024012279` | SPF/verification updated |
| `mail.meridianlabs.ctf` | `2024012711` | zone re-signed |

The `serial_ref` values in the zone match these exactly. That is the trust check: a fragment is only usable if both files agree on when the host changed.

## Step 3 — Order by serial

The serial format is `YYYYMMDDNN`, so numeric ascending order is chronological:

| # | Serial | Host | Fragment |
| ---: | ---: | --- | --- |
| 1 | `2024010209` | `stage` | `INJEKU2UPN5DA3RT` |
| 2 | `2024010268` | `portal` | `L52HENDOONTDG4TT` |
| 3 | `2024011069` | `mx2` | `L5QXEM3OG5PXG5LQ` |
| 4 | `2024012279` | `git` | `OAYHGM3EL52DAX3C` |
| 5 | `2024012711` | `mail` | `GNPXA5LCNQYWG7I=` |

Concatenated:

```text
INJEKU2UPN5DA3RTL52HENDOONTDG4TTL5QXEM3OG5PXG5LQOAYHGM3EL52DAX3CGNPXA5LCNQYWG7I=
```

This is Base32: uppercase `A–Z` and `2–7`, with `=` padding.

```bash
echo 'INJEKU2UPN5DA3RTL52HENDOONTDG4TTL5QXEM3OG5PXG5LQOAYHGM3EL52DAX3CGNPXA5LCNQYWG7I=' | base32 -d
```

## Step 4 — Decode

The Base32 decode produces:

```text
CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

Leetspeak: "zone transfers aren't supposed to be public."

## The solver

```python
zone = json.loads((ATT / "zone_dump.json").read_text())
changelog = json.loads((ATT / "ops_changelog.json").read_text())["entries"]
serial_by_host = {e["host"]: e["change_serial"] for e in changelog}

fragments = []
for record in zone["records"]:
    if record.get("type") != "TXT" or "frag=" not in record.get("value", ""):
        continue
    host = record["name"]
    serial = record.get("serial_ref") or serial_by_host.get(host)
    if serial is None:
        continue
    fragments.append((serial, host, record["value"].split("frag=", 1)[1]))

blob = "".join(fragment for _, _, fragment in sorted(fragments))
blob += "=" * (-len(blob) % 8)
print(base64.b32decode(blob).decode())
```

Full script: [`solve/solve.py`](solve/solve.py).

## Why the earlier "semantic reorder" was wrong

A first pass can notice that the decoded leetspeak words are out of order and try to rearrange them by meaning. That is tempting, but it is not the intended rule.

The data contains an explicit ordering key: `change_serial`. Sorting by it produces the same final flag without guessing. The changelog is not just context; it is the ordering and trust layer.

## Flag

```text
CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

## What I learned

- **A zone transfer is a data leak, not just a misconfiguration.** TXT records are public by design and should never hold secrets.
- **Join keys matter.** The hostname is the join key between the zone and the changelog; the serial is the ordering key.
- **"Not every record deserves trust" is a filter instruction.** Records without a fragment, a serial, or a changelog entry are noise.
- **Prefer the explicit order.** If the data contains a serial, sort by it before trying to make the plaintext read naturally.

## Reproduce

```bash
cd solve
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to OSINT](../README.md) · [Challenge overview](README.md)
