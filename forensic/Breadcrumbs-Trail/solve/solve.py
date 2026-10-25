#!/usr/bin/env python3
"""Decode the Base64 recovery fragment from the Breadcrumbs Trail manifest."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent.parent
manifest = ROOT / "attachments" / "var_lib_app_worker_recovery_manifest.conf"
fields = {}
for line in manifest.read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        fields[key.strip()] = value.strip()

if fields.get("encoding") != "base64":
    raise SystemExit("unexpected fragment encoding")
flag = base64.b64decode(fields["fragment"]).decode()
print("[*] archive:", fields.get("id"), "checkpoint:", fields.get("checkpoint"))
print("[+] FLAG:", flag)
