# Frame of Reference — full writeup

[← Back to OSINT](../README.md) · [Challenge overview](README.md)

**Category:** OSINT · **Difficulty:** Hard · **Points:** 300 · **Solves:** 151 · **Flag:** `CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}`

## TL;DR

- Read the incident window and reference coordinates from `field_report.txt`.
- Dump `DateTimeOriginal`, GPS, and `UserComment` from all three JPEGs.
- Only one still satisfies **both** the time and the place.
- Its `UserComment` is Base64; decode it.

## The report

```text
INCIDENT REPORT - Meridian Labs Facility, 2024-03-14
-----------------------------------------------------
A badge-less entry was logged at the north loading dock between
14:02 and 14:10 local time. Facilities has pulled three camera
stills from around that period for review. Cross-reference each
image's embedded metadata against the incident window AND the
loading dock's known coordinates (approx. 41.8901 N, -87.6234 W)
to identify which still actually corresponds to the incident.
```

Two constraints:

| Constraint | Value |
| --- | --- |
| Time window | 2024-03-14, 14:02–14:10 local |
| Location | 41.8901 N, 87.6234 W (north loading dock) |

The stills are flat color frames. There is nothing to see in the pixels; the report explicitly points at embedded metadata.

## Step 1 — Read the EXIF

With `exiftool`:

```bash
exiftool -a -G1 -s \
  cam_north_dock.jpg \
  cam_south_gate.jpg \
  cam_north_dock_earlier.jpg
```

The relevant fields:

| File | `DateTimeOriginal` | GPS (DMS) | `UserComment` (Base64) |
| --- | --- | --- | --- |
| `cam_north_dock.jpg` | 2024:03:14 14:06:22 | 41°53'24.36" N, 87°37'24.24" W | `Q1JFU1R7ZXgxZl90MW0zc3Q0bXBzX2QwbnRfbDEzX2J1dF9wMzBwbDNfZDB9` |
| `cam_south_gate.jpg` | 2024:03:14 14:05:10 | 41°53'15.72" N, 87°37'48.36" W | `Y2FtZXJhIGZpcm13YXJlIHYzLjIuMSBjYWxpYnJhdGlvbiBmcmFtZQ==` |
| `cam_north_dock_earlier.jpg` | 2024:03:14 11:47:03 | 41°53'24.36" N, 87°37'24.24" W | `cm91dGluZSBtYWludGVuYW5jZSBsb2csIG5vdGhpbmcgaGVyZQ==` |

## Step 2 — Convert GPS to decimal degrees

```text
decimal = degrees + minutes / 60 + seconds / 3600
```

Apply the hemisphere sign: south and west are negative.

| File | Latitude | Longitude |
| --- | ---: | ---: |
| `cam_north_dock.jpg` | 41.8901 | -87.6234 |
| `cam_south_gate.jpg` | 41.8877 | -87.6301 |
| `cam_north_dock_earlier.jpg` | 41.8901 | -87.6234 |

## Step 3 — Check both constraints

| File | Time in 14:02–14:10? | At the dock? | Result |
| --- | --- | --- | --- |
| `cam_north_dock.jpg` | Yes — 14:06:22 | Yes | **Match** |
| `cam_south_gate.jpg` | Yes — 14:05:10 | No — about 0.0024° N and 0.0067° W away | Right time, wrong place |
| `cam_north_dock_earlier.jpg` | No — 11:47:03 | Yes | Right place, wrong time |

Each decoy passes exactly one test. Only the north dock still passes both.

## Step 4 — Decode the comment

```bash
echo 'Q1JFU1R7ZXgxZl90MW0zc3Q0bXBzX2QwbnRfbDEzX2J1dF9wMzBwbDNfZDB9' | base64 -d
```

Output:

```text
CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}
```

The decoy comments decode to ordinary maintenance text, which confirms they were never the intended path.

## A pure-Python version

Pillow exposes the EXIF sub-IFD and GPS IFD directly:

```python
from PIL import Image

exif = Image.open("cam_north_dock.jpg").getexif()
sub = exif.get_ifd(0x8769)    # DateTimeOriginal, UserComment
gps = exif.get_ifd(0x8825)    # GPSLatitude, GPSLongitude

taken = sub[36867]            # '2024:03:14 14:06:22'
comment = sub[37510]          # b'ASCII\x00\x00\x00Q1JFU1R7...'
```

The full solver normalizes the DMS values, compares against the report, and decodes the matching comment. See [`solve/solve.py`](solve/solve.py).

## Flag

```text
CREST{ex1f_t1m3st4mps_d0nt_l13_but_p30pl3_d0}
```

## What I learned

- **Metadata is evidence.** A flat image can still carry a time, a place, and a message.
- **Check constraints together.** Each decoy is designed to pass one check and fail the other; evaluating either field alone gives the wrong answer.
- **Normalize units before comparing.** DMS → decimal and west longitude → negative are the two places this problem can silently go wrong.
- **Look at every free-text EXIF field.** `UserComment`, `ImageDescription`, and XMP are common hiding places for encoded data.

## Reproduce

```bash
cd solve
python -m pip install -r requirements.txt
python solve.py
```

Full solver: [`solve/solve.py`](solve/solve.py)

---

[← Back to OSINT](../README.md) · [Challenge overview](README.md)
