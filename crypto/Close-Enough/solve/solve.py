#!/usr/bin/env python3
"""Close Enough — Fermat factoring → RSA route → AES-GCM.

Run from anywhere:
    python solve/solve.py

Challenge files are read from ../attachments/.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
ATT = ROOT / "attachments"


def fermat_factor(n: int, max_iter: int = 1000) -> tuple[int, int] | None:
    """Return (p, q) when p and q are close enough for Fermat's method."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            if p > 1 and p * q == n:
                return p, q
        a += 1
    return None


def rsa_decrypt(ciphertext: int, key: dict, factors: tuple[int, int]) -> bytes:
    n = int(key["n"])
    e = int(key["e"])
    p, q = factors
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    value = pow(ciphertext, d, n)
    length = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(length, "big")


def main() -> None:
    keyset = json.loads((ATT / "keyset.json").read_text())
    messages = json.loads((ATT / "messages.json").read_text())
    public = {item["id"]: item for item in keyset["public"]}

    weak: dict[str, tuple[dict, tuple[int, int]]] = {}
    for key_id, key in public.items():
        factors = fermat_factor(int(key["n"]))
        if factors:
            weak[key_id] = (key, factors)
    print(f"[+] vulnerable keys: {', '.join(sorted(weak))}")

    route = [m for m in messages["messages"] if m.get("kind") == "route"]
    recovered: dict[str, tuple[str, bytes]] = {}
    for record in route:
        for key_id in sorted(weak):
            key, factors = weak[key_id]
            plaintext = rsa_decrypt(int(record["c"]), key, factors)
            if plaintext.startswith(b"CR5\x00"):
                recovered[record["rid"]] = (key_id, plaintext)
                break

    for rid, (key_id, plaintext) in recovered.items():
        print(f"[+] {rid} via {key_id}: {plaintext.decode(errors='replace')}")

    final = next(
        plaintext
        for _, plaintext in recovered.values()
        if plaintext.startswith(b"CR5\x00FINAL\x02")
    )
    fields = dict(
        part.split("=", 1)
        for part in final.decode().split("|")
        if "=" in part
    )
    aes_key = bytes.fromhex(fields["K"])

    payload = messages["payload"]
    plaintext = AESGCM(aes_key).decrypt(
        bytes.fromhex(payload["n"]),
        bytes.fromhex(payload["c"]) + bytes.fromhex(payload["t"]),
        bytes.fromhex(payload["a"]),
    )
    print(f"\n[+] FLAG: {plaintext.decode()}")


if __name__ == "__main__":
    main()
