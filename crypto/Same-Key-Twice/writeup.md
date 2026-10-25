> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:44 p.m.
>
> **Official challenge:** Same Key Twice · **Category:** Cryptography · **Difficulty:** Hard · **Points:** 550 · **Solves:** 69
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Same Key Twice — Writeup

**Category:** Crypto
**Flag:** `CREST{nonce_reuse_breaks_confidentiality_and_integrity}`

## Challenge

Two "independent" secure-chat session exports, `alpha.cblog` and `bravo.cblog`, each
containing 500,000 lines of routine telemetry noise with a handful of real protocol
records hidden inside. `chall.py` wasn't provided, so the crypto scheme had to be
reverse-engineered from the data itself.

> Two supposedly independent secure-chat sessions were recovered from a noisy
> telemetry archive. The exports contain 500,000 routine operational events each,
> with a small number of protocol records mixed into the stream. Record order is
> not trustworthy. A handful of strings resembling flags appear in unrelated
> operational events; do not assume a flag-shaped string is valid merely because
> it matches the format.
>
> Flag format: `CREST{...}`

## Recon

Both files start with a header line `CREST-CHAT/2`, then one JSON object per line.

- **Noise lines** (500k each): `{"ts","host","level","event","msg","rid","latency_ms","status"}`
  — generic fake ops-log chatter. Grepping for `CREST\{[^}]*\}` across these turned
  up ~18 flag-shaped strings sitting in plaintext `msg` fields
  (`CREST{cache_warmup_was_the_issue}`, `CREST{stale_route_table}`, etc.). These are
  the decoys the challenge explicitly warned about — never encrypted, not validated
  by anything, just red herrings.
- **Protocol records** (12 per session): `{"sid","seq","nonce","ct","tag","wire_len","trace"}`.
  These are the actual AEAD-encrypted chat messages.

## The bug

Nonces were built as `"CRST" + seq` (an 8-byte big-endian counter), starting from 0.
Both `alpha` and `bravo` sessions independently started their counters at 0 — meaning
for every `seq` value, both sessions encrypted under the **same key and the same
nonce**. Classic two-time-pad.

On top of that, two extra records at `seq=7` reused that exact nonce a third and
fourth time:
- `sid: telemetry`, channel `health-check`, 64 bytes
- `sid: archive`, channel `retention-export`, 55 bytes

Their ciphertexts' first 16 bytes matched `alpha`'s `seq=7` ciphertext exactly
(XOR = 0), confirming all four records share one keystream. Since `telemetry` and
`archive` are much longer than the 16-byte alpha/bravo messages, XORing *them*
together gives a 55-byte-long two-time pad — far more material to crib-drag than
any alpha/bravo pair.

## Exploit

1. Extracted all protocol records from both files.
2. Computed `x = telemetry_ct XOR archive_ct` (first 55 bytes) =
   `telemetry_pt XOR archive_pt` (keystream cancels since nonce/key are identical).
3. Guessed `archive_pt` starts with the known flag prefix `CREST{`. XORing that into
   `x` gave `telemetry_pt[0:6] = "STATUS"` — a real word falling out of a blind
   guess, strong confirmation the crib was right.
4. Tried flag continuations against the same relation.
   `"nonce_reuse_breaks_everything"` revealed `telemetry_pt` was repeating
   `STATUS:READY....` (16-byte period) up to a point, then the guess diverged —
   pinpointing exactly where it was wrong.
5. Solved the diverging bytes against the known `STATUS:READY....` continuation,
   recovering `"confide..."` → the real word was `confidentiality_and_integrity`.
6. Final check: assume `telemetry_pt = ("STATUS:READY...."×4)[:55]`, XOR with `x` →
   clean, grammatical plaintext:

```
CREST{nonce_reuse_breaks_confidentiality_and_integrity}
```

## Takeaway

Reusing an AEAD nonce — even just by having two sessions' counters both start at
zero — destroys confidentiality (two-time pad) and, with GCM/ChaCha-Poly1305-style
schemes, integrity too. The noise events were there purely to bury the needle
(12-14 real records) in a 500k-line haystack and to seed fake flags so
pattern-matching alone wouldn't work.

## Solve scripts

- `work/extract.py` — pulls the `ct`/`nonce`/`tag` protocol records out of both
  `.cblog` files.
- `work/decode.py` — computes `telemetry_ct XOR archive_ct` and decodes the flag
  using the `STATUS:READY....` heartbeat crib.
