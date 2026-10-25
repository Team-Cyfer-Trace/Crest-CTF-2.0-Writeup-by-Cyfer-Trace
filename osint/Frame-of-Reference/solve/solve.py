#!/usr/bin/env python3
"""Frame of Reference — match EXIF time and GPS against the field report.

Requires Pillow:
    python -m pip install -r solve/requirements.txt
"""
from __future__ import annotations

import base64
import re
from datetime import datetime
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ATT = ROOT / "attachments"
REPORT = ATT / "field_report.txt"

# EXIF tag ids
EXIF_IFD = 0x8769
GPS_IFD = 0x8825
DATETIME_ORIGINAL = 36867
USER_COMMENT = 37510


def dms_to_decimal(dms, ref: str) -> float:
    degrees, minutes, seconds = (float(x) for x in dms)
    value = degrees + minutes / 60 + seconds / 3600
    return -value if ref.upper() in {"S", "W"} else value


def read_still(path: Path) -> dict:
    exif = Image.open(path).getexif()
    sub = exif.get_ifd(EXIF_IFD)
    gps = exif.get_ifd(GPS_IFD)

    comment = sub.get(USER_COMMENT, b"")
    if isinstance(comment, bytes):
        comment = comment.split(b"\x00", 1)[-1].decode(errors="replace")

    return {
        "file": path.name,
        "taken": datetime.strptime(sub[DATETIME_ORIGINAL], "%Y:%m:%d %H:%M:%S"),
        "lat": dms_to_decimal(gps[2], gps[1]),
        "lon": dms_to_decimal(gps[4], gps[3]),
        "comment": comment,
    }


def main() -> None:
    report = REPORT.read_text()
    date = re.search(r"(\d{4}-\d{2}-\d{2})", report).group(1)
    start, end = re.search(r"between\s+(\d{2}:\d{2})\s+and\s+(\d{2}:\d{2})", report).groups()
    lat, lon = (float(x) for x in re.search(r"([-\d.]+)\s*N,\s*([-\d.]+)\s*W", report).groups())
    target_lat, target_lon = abs(lat), -abs(lon)

    stills = [read_still(p) for p in sorted(ATT.glob("*.jpg"))]
    for still in stills:
        in_window = (
            still["taken"].strftime("%Y-%m-%d") == date
            and start <= still["taken"].strftime("%H:%M") <= end
        )
        at_dock = abs(still["lat"] - target_lat) < 0.0005 and abs(still["lon"] - target_lon) < 0.0005
        print(
            f"{still['file']}: taken={still['taken']} "
            f"gps=({still['lat']:.6f}, {still['lon']:.6f}) "
            f"time_ok={in_window} place_ok={at_dock}"
        )
        if in_window and at_dock:
            flag = base64.b64decode(still["comment"]).decode()
            print(f"\n[+] FLAG: {flag}")


if __name__ == "__main__":
    main()
