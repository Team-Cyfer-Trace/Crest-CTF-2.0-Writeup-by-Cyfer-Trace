# Forensics

Reconstructing what happened from logs, memory, disk images, and the things an attacker forgot to clean up.

**Team result:** 4 of 9 cleared · **Published writeups:** 4 (0 personal, 4 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Backdated](Backdated/) | Parth (`DeadStorm18`) | Hard | 550 | 87 | [read](Backdated/writeup.md) |
| [Breadcrumbs Trail](Breadcrumbs-Trail/) | Hrishikesh (`hrishikesh`) | Hard | 550 | 218 | [read](Breadcrumbs-Trail/writeup.md) |
| [Memory Lane](Memory-Lane/) | Bryan (`RadixCobra19`) | Hard | 550 | 42 | [read](Memory-Lane/writeup.md) |
| [Hived Off CRW1](Hived-Off-CRW1/) | Hrishikesh (`hrishikesh`) | Expert | 700 | 107 | [read](Hived-Off-CRW1/writeup.md) |

## Still open

| Challenge | Difficulty | Solves |
| --- | --- | ---: |
| Broken Chain | Hard | 9 |
| Lateral Whisper | Hard | 0 |
| Memory Echo | Hard | 0 |
| Silent Injection | Medium | 22 |
| Whispers in the Query | Expert | 0 |

## Notes

- `Backdated` cross-references a forged filesystem snapshot with an append-only audit journal.
- `Breadcrumbs Trail` correlates shell history, service state, auth/audit/syslog, and a recovery manifest; all ten official evidence files are archived here.
- `Hived Off CRW1` starts with an OLE2 document and an obfuscated VBA macro, then pivots into a Bleichenbacher oracle and XPath injection.
- `Memory Lane` reconstructs a credential-manager record table from a raw memory dump at a fixed base address.

---

[← All categories](../README.md) · [All writeups](../README.md)
