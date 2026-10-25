#!/usr/bin/env python3
"""Ghost Domain — join TXT fragments by their changelog serial, then Base32-decode."""
from __future__ import annotations

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATT = ROOT / "attachments"


def main() -> None:
    zone = json.loads((ATT / "zone_dump.json").read_text())
    changelog = json.loads((ATT / "ops_changelog.json").read_text())["entries"]
    serial_by_host = {entry["host"]: entry["change_serial"] for entry in changelog}

    fragments = []
    for record in zone["records"]:
        if record.get("type") != "TXT" or "frag=" not in record.get("value", ""):
            continue
        host = record["name"]
        serial = record.get("serial_ref") or serial_by_host.get(host)
        if serial is None:
            continue
        fragment = record["value"].split("frag=", 1)[1]
        fragments.append((serial, host, fragment))

    for serial, host, fragment in sorted(fragments):
        print(f"{serial}  {host:<40}  {fragment}")

    blob = "".join(fragment for _, _, fragment in sorted(fragments))
    blob += "=" * (-len(blob) % 8)
    print(f"\n[+] concatenated: {blob}")
    print(f"[+] FLAG: {base64.b32decode(blob).decode()}")


if __name__ == "__main__":
    main()
