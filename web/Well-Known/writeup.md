> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:02 p.m.
>
> **Official challenge:** Well Known · **Category:** Web · **Difficulty:** Easy · **Points:** 200 · **Solves:** 196
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Well Known - Writeup

## Challenge Information

- **Category:** Web Exploitation
- **Target:** `http://2.31.70.16:5400/`
- **Flag format:** `crest{...}`

## Enumeration

The homepage presents a Crest Security marketing site. Its footer contains the clue:

> Researchers: see our published disclosure metadata.

The page also mentions that Crest publishes standard machine-readable security metadata. This points to the conventional `/.well-known/` directory, specifically the `security.txt` file used for security disclosure information.

Requesting the following endpoint:

```text
http://2.31.70.16:5400/.well-known/security.txt
```

returns a valid security policy file. Alongside the disclosure contacts and policy information, it contains an internal comment:

```text
# Internal disclosure canary (do not remove): crest{w3ll_kn0wn_s3cur1ty_txt}
```

## Flag

```text
crest{w3ll_kn0wn_s3cur1ty_txt}
```
