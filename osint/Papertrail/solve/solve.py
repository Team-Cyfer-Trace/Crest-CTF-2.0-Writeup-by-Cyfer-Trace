#!/usr/bin/env python3
"""Papertrail — filter .docx files by author, order fragments by memo number."""
from __future__ import annotations

import base64
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "attachments" / "docs" / "files"


def core_field(xml: str, tag: str) -> str | None:
    match = re.search(rf"<{tag}>(.*?)</{tag}>", xml, re.S)
    return match.group(1) if match else None


def main() -> None:
    fragments: list[tuple[int, str, str]] = []
    for path in sorted(DOCS.glob("doc_*.docx")):
        with zipfile.ZipFile(path) as archive:
            core = archive.read("docProps/core.xml").decode()
            document = archive.read("word/document.xml").decode()

        creator = core_field(core, "dc:creator")
        description = core_field(core, "dc:description") or ""
        if creator != "R. Chen" or "frag=" not in description:
            continue

        text = " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", document))
        memo = int(re.search(r"Internal Memo #(\d+)", text).group(1))
        fragment = description.split("frag=", 1)[1].strip()
        fragments.append((memo, path.name, fragment))
        print(f"[+] memo #{memo}  {path.name}  {fragment}")

    fragments.sort()
    blob = "".join(fragment for _, _, fragment in fragments)
    print(f"\n[+] concatenated: {blob}")
    print(f"[+] FLAG: {base64.b64decode(blob).decode()}")


if __name__ == "__main__":
    main()
