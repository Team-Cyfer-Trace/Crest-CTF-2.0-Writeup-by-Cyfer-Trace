# Ghost Domain

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-OSINT-8A4B08?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-7A5A12?style=flat-square)
![Points](https://img.shields.io/badge/Points-200-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-302-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

A misconfigured DNS server has exposed a zone transfer belonging to `meridianlabs.ctf`. Alongside it, an internal operations changelog has mysteriously surfaced.

At first glance, the records appear ordinary, but hidden within the noise are fragments of something valuable. Neither file reveals the complete picture on its own.

Your mission is to investigate the leaked artifacts, connect the scattered clues, and reconstruct the hidden flag.

Not every record deserves your trust. Follow the right trail.

**Flag format:** `CREST{...}`

**Attachments:** [`zone_dump.json`](attachments/zone_dump.json) · [`ops_changelog.json`](attachments/ops_changelog.json)

## Flag

```text
CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** five TXT records carry `frag=` payloads with `serial_ref` values; sort those fragments by their changelog serial, concatenate, and Base32-decode.

- The zone dump contains 19 records, but only five have both `frag=` and a `serial_ref`.
- The changelog confirms the serial for each host.
- Serial order: `stage` → `portal` → `mx2` → `git` → `mail`.
- The concatenated Base32 string decodes directly to the flag.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/zone_dump.json`](attachments/zone_dump.json) | Leaked AXFR-style zone export |
| [`attachments/ops_changelog.json`](attachments/ops_changelog.json) | 20 internal change entries with serials |
| [`solve/solve.py`](solve/solve.py) | Joins fragments by serial and decodes Base32 |

## Run the solver

```bash
cd solve
python solve.py
```

Expected output:

```text
2024010209  stage.meridianlabs.ctf                    INJEKU2UPN5DA3RT
2024010268  portal.meridianlabs.ctf                   L52HENDOONTDG4TT
2024011069  mx2.meridianlabs.ctf                      L5QXEM3OG5PXG5LQ
2024012279  git.meridianlabs.ctf                      OAYHGM3EL52DAX3C
2024012711  mail.meridianlabs.ctf                     GNPXA5LCNQYWG7I=

[+] FLAG: CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

## Notes

- Some TXT records are ordinary SPF or domain-verification entries. They are decoys.
- The `mail` entry is a `zone re-signed` event. It is the newest serial, but the flag is not simply the last fragment; the fragments must still be concatenated in ascending serial order.
- The `serial_ref` in `zone_dump.json` matches the `change_serial` in the changelog for every fragment. That agreement is the trust check.

---

[← Back to OSINT](../README.md) · [All writeups](../../README.md)
