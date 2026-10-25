# Hived Off CRW1

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Forensics-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Expert-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-700-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-107-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 11:30 a.m.
> **Challenge author:** Tanmay M · **Created:** 23 Oct, 2026

## Challenge description

An incident started with a phishing lure: a "quarterly invoice" attachment with a macro. It was quarantined before it fired, but the config it carried is the thread that unravels the whole intrusion.The attachment is an OLE2 compound document with an obfuscated VBA AutoOpen macro; deobfuscate it to recover a token and the endpoint it beacons to. That endpoint is a legacy RSA "credential unwrap" service that still speaks PKCS#1 v1.5 and leaks whether a decryption is padding-conforming — a Bleichenbacher oracle that gives up an admin credential with no private key (after AUTH, it takes ciphertexts as DECRYPT <hex>;). That credential logs you into a corporate directory admin portal whose search splices your input straight into an XPath query over its XML user store.This is a three-stage chain -- Forensics then Crypto then Web -- where each stage's output unlocks the next. Deobfuscate the macro, run Bleichenbacher, then inject XPath to pull the flag node. Access:Stage 1: http://2.31.70.16:16240/Stage 2: nc 2.31.70.16 16241Stage 3: http://2.31.70.16:16242/

**Flag format:** `ctf7{...}`

**Attachments:** [`quarterly_invoice.doc`](attachments/quarterly_invoice.doc)

**Targets (offline after the event):** `http://2.31.70.16:16240/` · `nc 2.31.70.16 16241` · `http://2.31.70.16:16242/`

## Flag

```text
ctf7{vba_macro_bleichenbacher_xpath_pivot}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Deobfuscate an OLE2 VBA macro, use a PKCS#1 v1.5 padding oracle, then inject XPath into a directory admin portal.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/quarterly_invoice.doc` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |

## Notes

- `quarterly_invoice.doc` is the stage-1 OLE2 document.
- The flag uses lowercase `ctf7{...}`.
- The full kill chain is Forensics → Crypto → Web.

## Run the solver

No end-to-end solver is archived; stages 2 and 3 are remote services that are offline after the event. The writeup contains the VBA deobfuscation, Bleichenbacher attack, and XPath payload.

---

[← Back to Forensics](../README.md) · [All writeups](../../README.md)
