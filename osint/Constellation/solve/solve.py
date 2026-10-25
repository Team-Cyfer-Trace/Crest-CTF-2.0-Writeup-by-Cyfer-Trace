#!/usr/bin/env python3
"""Constellation — intersect the neighbour sets of three accounts."""
from __future__ import annotations

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "attachments" / "nodebook_export.json"


def main() -> None:
    data = json.loads(DATA.read_text())
    targets = ["kestrel", "fennec", "quartz"]

    adjacency: dict[str, set[str]] = {}
    for left, right in data["connections"]:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)

    common = set.intersection(*(adjacency[t] for t in targets)) - set(targets)
    print(f"[+] accounts connected to all three targets: {sorted(common)}")

    bios = {user["handle"]: user["bio"] for user in data["users"]}
    for handle in sorted(common):
        encoded = bios[handle]
        try:
            decoded = base64.b64decode(encoded).decode()
        except Exception:
            decoded = "(not base64)"
        print(f"[+] {handle} bio: {decoded}")


if __name__ == "__main__":
    main()
