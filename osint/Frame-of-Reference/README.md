# Frame of Reference

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-OSINT-8A4B08?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-300-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-151-1F5F73?style=flat-square)

> **Solved by** Ishant Choudhary ([@griffin-dox](https://github.com/griffin-dox)) · **Team** Cyfer Trace · **Solved** 23 October 2026

## Challenge description

Three camera stills, and `field_report.txt` describing an incident window and location. Only one still actually corresponds to the incident — the other two are decoys (right time, wrong place / right place, wrong time). Recover the flag.

**Flag format:** `CREST{...}`

**Attachments:** [`cam_north_dock.jpg`](attachments/cam_north_dock.jpg) · [`cam_south_gate.jpg`](attachments/cam_south_gate.jpg) · [`cam_north_dock_earlier.jpg`](attachments/cam_north_dock_earlier.jpg) · [`field_report.txt`](attachments/field_report.txt)

## Flag

```text
CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

**In one line:** only `cam_north_dock.jpg` matches both the incident window (14:02–14:10) and the loading dock coordinates; its EXIF `UserComment` is Base64.

- The pixels are flat color. The evidence is in EXIF.
- `cam_south_gate.jpg` has the right time but the wrong GPS position.
- `cam_north_dock_earlier.jpg` has the right position but the wrong time.
- The matching still's `UserComment` decodes to the flag.

## Files

| Path | What it is |
| --- | --- |
| [`attachments/field_report.txt`](attachments/field_report.txt) | Incident window and reference coordinates |
| [`attachments/cam_north_dock.jpg`](attachments/cam_north_dock.jpg) | Still from the north dock |
| [`attachments/cam_south_gate.jpg`](attachments/cam_south_gate.jpg) | Still from the south gate |
| [`attachments/cam_north_dock_earlier.jpg`](attachments/cam_north_dock_earlier.jpg) | Earlier still from the north dock |
| [`solve/solve.py`](solve/solve.py) | EXIF time + GPS matcher and Base64 decoder |
| [`solve/requirements.txt`](solve/requirements.txt) | Python dependency (`Pillow`) |

## Run the solver

```bash
cd solve
python -m pip install -r requirements.txt
python solve.py
```

Expected output:

```text
cam_north_dock.jpg: taken=2024-03-14 14:06:22 gps=(41.890100, -87.623400) time_ok=True place_ok=True
[+] FLAG: CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}
```

## Notes

- The report's longitude is written as `-87.6234 W`. Normalize the sign once, then compare decimal degrees.
- `UserComment` has an 8-byte character-set prefix (`ASCII\0\0\0`) before the Base64 payload. Strip it before decoding.
- The filenames happen to agree with the metadata here, but the decision must rest on the EXIF values, not the names.

---

[← Back to OSINT](../README.md) · [All writeups](../../README.md)
