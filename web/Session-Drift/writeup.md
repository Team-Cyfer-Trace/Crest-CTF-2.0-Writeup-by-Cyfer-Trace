> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:35 a.m.
>
> **Official challenge:** Session Drift · **Category:** Web · **Difficulty:** Medium · **Points:** 300 · **Solves:** 174
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Session Drift - CTF7 Write-up

## Challenge Information

- **Challenge:** Session Drift
- **Category:** Web Exploitation
- **Target:** `http://2.31.70.16:5100/`
- **Flag:** `crest{s3ss10n_dr1ft_s3cr3t_reuse}`

## Description

The application is a Crest staff portal. A demo account is provided, but administrative reports are restricted to users with the `admin` role.

Provided credentials:

```text
Username: alice
Password: password123
```

## Enumeration

The web service was running on port `5100`. The home page showed links to the login page and described the role-based access control.

After logging in as `alice`, the dashboard showed:

```text
Username: alice
Session role: user
Admin reports: locked
```

The application used a Flask-style client-side session cookie. Decoding the cookie revealed data equivalent to:

```json
{
  "username": "alice",
  "role": "user"
}
```

Because the session is client-side signed, the signing secret would be needed to modify the role safely.

## Finding the Secret Key

The `robots.txt` file contained an interesting entry:

```text
User-agent: *
Disallow: /static/backup/
```

The backup directory was then checked for configuration files. The following file was accessible:

```text
/static/backup/config.py.bak
```

Its contents disclosed the Flask secret key:

```python
# Crest Internal - staging config (DO NOT COMMIT)
# NOTE: secret reused from the dev box; rotate before prod (SEC-241)
SECRET_KEY = "sup3r-s3cr3t-dev-key-2023"
DEBUG = False
```

## Forging the Session

The original session contained the `user` role. Using the leaked key, a new Flask session was generated with the role changed to `admin`:

```json
{
  "username": "alice",
  "role": "admin"
}
```

The forged cookie was sent to:

```text
/dashboard
```

The server accepted the signature and displayed the administrative report.

## Result

The dashboard revealed the flag:

```text
crest{s3ss10n_dr1ft_s3cr3t_reuse}
```

## Root Cause

The challenge combines two issues:

1. A backup configuration file is exposed under a web-accessible static path.
2. The Flask `SECRET_KEY` is reused and is used to sign client-side session data containing the authorization role.

An attacker who obtains the key can modify the session and escalate from the `user` role to the `admin` role.

## Mitigations

- Remove backup and configuration files from publicly served directories.
- Rotate the exposed secret key immediately.
- Use strong, unique production secrets stored outside the source tree.
- Do not store authorization decisions solely in client-controlled session data.
- Enforce authorization using server-side user records or a server-side session store.
- Add deployment checks to prevent `.bak`, `.env`, and configuration files from being published.
