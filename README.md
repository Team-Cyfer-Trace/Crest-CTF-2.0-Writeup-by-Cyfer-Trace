# CREST CTF 2.0 — Cyfer Trace Writeups

![CREST_CTF_2.0](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square) ![Team](https://img.shields.io/badge/Team-Cyfer_Trace-B4441F?style=flat-square) ![Team_score](https://img.shields.io/badge/Team_score-31%2F40-2F5D3A?style=flat-square)
![Team_writeups](https://img.shields.io/badge/Team_writeups-30-1F5F73?style=flat-square) ![Author_writeups](https://img.shields.io/badge/Author_writeups-8-4B4E8C?style=flat-square)

Field notes from **Team Cyfer Trace** at **CREST CTF 2.0 (CTF7)**, 22–23 October 2026.

This repository is organised by category, then by challenge. Every challenge folder contains the original brief, the files that were provided where available, the flag the team recovered, and a full writeup. Where a solve needed code, the solver is included and tested against the attached data.

The goal is simple: make each solve readable in five minutes and reproducible in ten.

## At a glance

| | |
| --- | ---: |
| Team score | **31 / 40** |
| Team points | **16,700** |
| Challenge names cleared | **30** |
| Flags captured | **31** (Nightfall carries two) |
| Published writeups | **30** (8 personal + 22 teammate) |
| Team members | **4** |
| Categories | **9** |
| Archived attachments | challenge files for the offline, file-based challenges; 93 MB files are linked only |

> **Attribution is explicit.** The eight writeups under “Personal writeups” are Ishant Choudhary's own solves. The twenty-two teammate writeups are attributed to the named author and handle in the challenge README, the writeup header, and the category index. They are **not** claimed as Ishant's personal work.

## Personal writeups by Ishant Choudhary

| Challenge | Category | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Close Enough](crypto/Close-Enough/) | Cryptography | Expert | 1200 | 122 | [read](crypto/Close-Enough/writeup.md) |
| [Truncated Trust](misc/Truncated-Trust/) | Miscellaneous | Hard | 600 | 91 | [read](misc/Truncated-Trust/writeup.md) |
| [Ghost Domain](osint/Ghost-Domain/) | OSINT | Medium | 200 | 302 | [read](osint/Ghost-Domain/writeup.md) |
| [Papertrail](osint/Papertrail/) | OSINT | Medium | 250 | 253 | [read](osint/Papertrail/writeup.md) |
| [Frame of Reference](osint/Frame-of-Reference/) | OSINT | Hard | 300 | 151 | [read](osint/Frame-of-Reference/writeup.md) |
| [Constellation](osint/Constellation/) | OSINT | Hard | 350 | 168 | [read](osint/Constellation/writeup.md) |
| [Ghost Machine](rev/Ghost-Machine/) | Reverse Engineering | Medium | 850 | 145 | [read](rev/Ghost-Machine/writeup.md) |
| [Transmission](stegno/Transmission/) | Steganography | Hard | 600 | 80 | [read](stegno/Transmission/writeup.md) |

## Teammate writeups

### Parth (`DeadStorm18`) — 5 writeups

| Challenge | Category | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Backdated](forensic/Backdated/) | Forensics | Hard | 550 | 87 | [read](forensic/Backdated/writeup.md) |
| [Loop of Mirrors](rev/Loop-of-Mirrors/) | Reverse Engineering | Expert | 1000 | 189 | [read](rev/Loop-of-Mirrors/writeup.md) |
| [Latchkey](rev/Latchkey/) | Reverse Engineering | Medium | 250 | 220 | [read](rev/Latchkey/writeup.md) |
| [Recursion Ward](rev/Recursion-Ward/) | Reverse Engineering | Medium | 300 | 165 | [read](rev/Recursion-Ward/writeup.md) |
| [Origami](rev/Origami/) | Reverse Engineering | Hard | 400 | 193 | [read](rev/Origami/writeup.md) |

### Bryan (`RadixCobra19`) — 4 writeups

| Challenge | Category | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Same Key Twice](crypto/Same-Key-Twice/) | Cryptography | Hard | 550 | 69 | [read](crypto/Same-Key-Twice/writeup.md) |
| [Biased Signatures](crypto/Biased-Signatures/) | Cryptography | Hard | 600 | 90 | [read](crypto/Biased-Signatures/writeup.md) |
| [Memory Lane](forensic/Memory-Lane/) | Forensics | Hard | 550 | 42 | [read](forensic/Memory-Lane/writeup.md) |
| [NP In Disguise](misc/NP-In-Disguise/) | Miscellaneous | Hard | 600 | 96 | [read](misc/NP-In-Disguise/writeup.md) |

### Hrishikesh (`hrishikesh`) — 13 writeups

| Challenge | Category | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Shift Register CRW3](crypto/Shift-Register-CRW3/) | Cryptography | Expert | 700 | 77 | [read](crypto/Shift-Register-CRW3/writeup.md) |
| [Noise Updated](crypto/Noise-Updated/) | Cryptography | Expert | 900 | 143 | [read](crypto/Noise-Updated/writeup.md) |
| [Breadcrumbs Trail](forensic/Breadcrumbs-Trail/) | Forensics | Hard | 550 | 218 | [read](forensic/Breadcrumbs-Trail/writeup.md) |
| [Hived Off CRW1](forensic/Hived-Off-CRW1/) | Forensics | Expert | 700 | 107 | [read](forensic/Hived-Off-CRW1/writeup.md) |
| [Hidden Frequencies](misc/Hidden-Frequencies/) | Miscellaneous | Hard | 550 | 93 | [read](misc/Hidden-Frequencies/writeup.md) |
| [Nightfall](multi/Nightfall/) | Multi | Hard | 200 | 188 | [read](multi/Nightfall/writeup.md) (2 flags) |
| [Keymaster CRW2](network/Keymaster-CRW2/) | Networking | Expert | 700 | 146 | [read](network/Keymaster-CRW2/writeup.md) |
| [Ghost Writer CRW1](rev/Ghost-Writer-CRW1/) | Reverse Engineering | Expert | 700 | 138 | [read](rev/Ghost-Writer-CRW1/writeup.md) |
| [Afterimage Protocol](stegno/Afterimage-Protocol/) | Steganography | Expert | 1000 | 144 | [read](stegno/Afterimage-Protocol/writeup.md) |
| [Well Known](web/Well-Known/) | Web | Easy | 200 | 196 | [read](web/Well-Known/writeup.md) |
| [White Pixel](web/White-Pixel/) | Web | Medium | 200 | 74 | [read](web/White-Pixel/writeup.md) |
| [Session Drift](web/Session-Drift/) | Web | Medium | 300 | 174 | [read](web/Session-Drift/writeup.md) |
| [Query Shadow](web/Query-Shadow/) | Web | Hard | 400 | 232 | [read](web/Query-Shadow/writeup.md) |

## Repository map

```text
crypto/      5 writeups   Close Enough · Biased Signatures · Noise Updated · Same Key Twice · Shift Register CRW3
forensic/    4 writeups   Backdated · Breadcrumbs Trail · Hived Off CRW1 · Memory Lane
misc/        3 writeups   Truncated Trust · Hidden Frequencies · NP In Disguise
multi/       1 writeup    Nightfall
network/     1 writeup    Keymaster CRW2
osint/       4 writeups   Constellation · Frame of Reference · Ghost Domain · Papertrail
rev/         6 writeups   Ghost Machine · Ghost Writer CRW1 · Latchkey · Loop of Mirrors · Origami · Recursion Ward
stegno/      2 writeups   Transmission · Afterimage Protocol
web/         4 writeups   Query Shadow · Session Drift · Well Known · White Pixel
extras/      unlisted material, including one writeup with no matching official challenge
```

## Reproducing the solves

| Challenge | Solver | Dependencies | Expected output |
| --- | --- | --- | --- |
| Close Enough | [`solve/solve.py`](crypto/Close-Enough/solve/solve.py) | stdlib | `CREST{close_enough_was_only_the_first_lock}` |
| Transmission | [`solve/solve.py`](stegno/Transmission/solve/solve.py) | stdlib | `CREST{bl4nk_5p4ces_4re_d3lusi0ns}` |
| Truncated Trust | [`solve/solve.py`](misc/Truncated-Trust/solve/solve.py) | stdlib | `ctf7{trunc4t3d_lcg_l4tt1c3_r3c0v3ry}` |
| Constellation | [`solve/solve.py`](osint/Constellation/solve/solve.py) | stdlib | `CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}` |
| Frame of Reference | [`solve/solve.py`](osint/Frame-of-Reference/solve/solve.py) | Pillow | `CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}` |
| Ghost Domain | [`solve/solve.py`](osint/Ghost-Domain/solve/solve.py) | stdlib | `CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}` |
| Papertrail | [`solve/solve.py`](osint/Papertrail/solve/solve.py) | python-docx | `CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}` |
| Ghost Machine | [`solve/solve.py`](rev/Ghost-Machine/solve/solve.py) | stdlib | `CREST{d1s4ss3mbl3_th3_v01d}` |
| Latchkey | [`solve/solve.py`](rev/Latchkey/solve/solve.py) | stdlib | `CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}` |
| Origami | [`solve/solve.py`](rev/Origami/solve/solve.py) | stdlib | `CREST{byt3c0d3_vms_hide_l0g1c_n0t_h1de_1t_w3ll}` |
| Recursion Ward | [`solve/solve.py`](rev/Recursion-Ward/solve/solve.py) | capstone, pyelftools | `CREST{fl4tt3n3d_c0ntr0l_fl0w_1s_st1ll_j5t_a_gr4ph}` |
| Breadcrumbs Trail | [`solve/solve.py`](forensic/Breadcrumbs-Trail/solve/solve.py) | stdlib | `CREST{Breadcrumbs2026Trail9X}` |
| Hidden Frequencies | [`solve/solve.py`](misc/Hidden-Frequencies/solve/solve.py) | numpy | `ctf7{fr3qu3ncy_d0m41n_s3cr3ts}` |
| Afterimage Protocol | [`solve/solve.py`](stegno/Afterimage-Protocol/solve/solve.py) | numpy, Pillow | `CREST{f1lt3rs_b3f0r3_p1x3ls_9f42d8e1}` |

Run any solver from its `solve/` directory. Each one reads challenge data from `../attachments/` and never from an absolute path. The remote-service challenges do not have offline solvers because their targets were taken down after the event.

## Scope and attribution

- **Personal work:** 8 writeups by Ishant Choudhary (`griffin-dox`).
- **Teammate work:** 22 writeups by Parth (`DeadStorm18`, 5), Bryan (`RadixCobra19`, 4), and Hrishikesh (`hrishikesh`, 13 names / 14 flags).
- **Flags are exact.** Prefixes vary by challenge: `CREST{...}`, `ctf7{...}`, and lowercase `crest{...}` are all preserved.
- **Nightfall** is one challenge name but two flags (user and root), which is why the team board shows 31 captures from 30 names.
- **Same Key Twice** ships two 93 MB `.cblog` files. They are linked from the challenge README instead of committed, so the repository stays usable.
- **Linear In Disguise** does not match any of the 40 official challenge names. It is preserved under [`extras/unlisted/`](extras/unlisted/Linear-In-Disguise/) and is not counted in any total.
- The earlier `writeup/osint-1-ghost_domain_writeup.md` draft is not used; the corrected [`osint/Ghost-Domain/writeup.md`](osint/Ghost-Domain/writeup.md) is authoritative.

## Team

| Name | Handle | Solves | Points | Published writeups |
| --- | --- | ---: | ---: | ---: |
| Ishant Choudhary | [`griffin-dox`](https://github.com/griffin-dox) | 8 | 4,350 | 8 |
| Hrishikesh | `hrishikesh` | 14 | 7,550 | 13 names / 14 flags |
| Parth | `DeadStorm18` | 5 | 2,500 | 5 |
| Bryan | `RadixCobra19` | 4 | 2,300 | 4 |

## Future updates

The archive is complete for every challenge the team cleared. The ten challenges that remained open are listed in their category READMEs; if any are solved later, add a folder using the same `README.md` + `writeup.md` + `attachments/` + `solve/` layout and update the category table.

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`NOTICE.md`](NOTICE.md) for attribution and reuse details.

---

Repository owner: [Ishant Choudhary (@griffin-dox)](https://github.com/griffin-dox) · Event: [Crest CTF 2.0 on CTF7](https://ctf7.com/console/event/crest-ctf-20/home/).
