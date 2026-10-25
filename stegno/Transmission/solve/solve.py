#!/usr/bin/env python3
"""Transmission — zero-width Unicode → Morse → Base32 → Base64 → XOR."""
from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "attachments" / "transmission.txt"

# The four invisible characters used by the challenge.
DASH = "\u200b"       # ZERO WIDTH SPACE
DOT = "\u034f"        # COMBINING GRAPHEME JOINER
SEPARATOR = "\u200c"  # ZERO WIDTH NON-JOINER
FILLER = "\u2060"     # WORD JOINER

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
    "---..": "8", "----.": "9",
}


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    hidden = [char for char in text if char in {DASH, DOT, SEPARATOR, FILLER}]
    if not hidden:
        raise SystemExit("no invisible characters found")

    symbols = "".join(
        "-" if char == DASH else "." if char == DOT else "|" if char == SEPARATOR else ""
        for char in hidden
    )
    groups = [group for group in symbols.split("|") if group]
    print(f"[+] invisible characters: {len(hidden)}")
    print(f"[+] Morse groups: {len(groups)}")

    letters = []
    for group in groups:
        if group not in MORSE:
            raise SystemExit(f"invalid Morse group: {group!r}")
        letters.append(MORSE[group])
    encoded = "".join(letters)
    print(f"[+] Base32: {encoded}")

    encoded += "=" * (-len(encoded) % 8)
    raw = base64.b32decode(encoded)
    raw += b"=" * (-len(raw) % 4)
    ciphertext = base64.b64decode(raw)

    key = b"KEY42"
    plaintext = bytes(byte ^ key[i % len(key)] for i, byte in enumerate(ciphertext))
    print(f"[+] FLAG: {plaintext.decode()}")


if __name__ == "__main__":
    main()
