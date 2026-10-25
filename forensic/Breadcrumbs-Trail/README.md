# Breadcrumbs Trail

![Event](https://img.shields.io/badge/Event-CREST_CTF_2.0-101518?style=flat-square) ![Category](https://img.shields.io/badge/Category-Forensics-B4441F?style=flat-square) ![Difficulty](https://img.shields.io/badge/Difficulty-Hard-8A4B08?style=flat-square)
![Points](https://img.shields.io/badge/Points-550-2F5D3A?style=flat-square) ![Solves](https://img.shields.io/badge/Solves-218-1F5F73?style=flat-square)

> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:15 a.m.
> **Challenge author:** Tanmay M · **Created:** 22 Oct, 2026

## Challenge description

A Linux application server returned to service after a suspicious overnight maintenance window. You have been provided with authentication, shell-history, audit, syslog, service-state, and recovery artifacts.
Investigate the evidence, correlate events across sources, identify the privilege boundary and local account transition, and recover the final flag from the matching recovery manifest.
Expect extended logs with routine activity mixed into the incident records. Flag-shaped strings may appear in metadata or annotations; do not assume that a string is the answer without validating the evidence chain. No Docker, network access, or elevated privileges are required. Flag format: CREST{...}
Attachments (evidence/): home_deploy_bash_history, srv_app_deploy_notes.txt, usr_local_bin_rotate_worker_state, var_lib_app_worker_history_20260918021406.state, var_lib_app_worker_recovery_manifest.conf, var_log_audit_execve.log, var_log_auth.log, var_log_journal_app_worker_export.log, var_log_syslog.log, var_tmp_stage_state.txt

**Flag format:** `CREST{...}`

**Attachments:** [`home_deploy_bash_history`](attachments/home_deploy_bash_history) · [`srv_app_deploy_notes.txt`](attachments/srv_app_deploy_notes.txt) · [`usr_local_bin_rotate_worker_state`](attachments/usr_local_bin_rotate_worker_state) · [`var_lib_app_worker_history_20260918021406.state`](attachments/var_lib_app_worker_history_20260918021406.state) · [`var_lib_app_worker_recovery_manifest.conf`](attachments/var_lib_app_worker_recovery_manifest.conf) · [`var_log_audit_execve.log`](attachments/var_log_audit_execve.log) · [`var_log_auth.log`](attachments/var_log_auth.log) · [`var_log_journal_app_worker_export.log`](attachments/var_log_journal_app_worker_export.log) · [`var_log_syslog.log`](attachments/var_log_syslog.log) · [`var_tmp_stage_state.txt`](attachments/var_tmp_stage_state.txt)

## Flag

```text
CREST{Breadcrumbs2026Trail9X}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

Correlate shell history, service state, auth/audit/syslog, and a recovery manifest to find the one valid flag among many decoys.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/home_deploy_bash_history` | Official challenge file. |
| `attachments/srv_app_deploy_notes.txt` | Official challenge file. |
| `attachments/usr_local_bin_rotate_worker_state` | Official challenge file. |
| `attachments/var_lib_app_worker_history_20260918021406.state` | Official challenge file. |
| `attachments/var_lib_app_worker_recovery_manifest.conf` | Official challenge file. |
| `attachments/var_log_audit_execve.log` | Official challenge file. |
| `attachments/var_log_auth.log` | Official challenge file. |
| `attachments/var_log_journal_app_worker_export.log` | Official challenge file. |
| `attachments/var_log_syslog.log` | Official challenge file. |
| `attachments/var_tmp_stage_state.txt` | Official challenge file. |
| `attachments/SHA256SUMS` | SHA-256 checksums for the archived challenge files. |
| `solve/solve.py` | Tested decoder for the Base64 recovery fragment. |

## Notes

- All ten official evidence files are archived here, including `var_lib_app_worker_history_20260918021406.state`, which the author's working copy did not have.
- The manifest contains several flag-shaped decoys; the solver validates the `encoding=base64` field and decodes the matching fragment.
- The challenge is entirely offline and does not require Docker or elevated privileges.

## Run the solver

Then run it:

```bash
cd solve
python solve.py
```

Expected final line:

```text
[+] FLAG: CREST{Breadcrumbs2026Trail9X}
```

---

[← Back to Forensics](../README.md) · [All writeups](../../README.md)
