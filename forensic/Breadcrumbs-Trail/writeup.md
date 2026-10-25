> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:15 a.m.
>
> **Official challenge:** Breadcrumbs Trail · **Category:** Forensics · **Difficulty:** Hard · **Points:** 550 · **Solves:** 218
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Breadcrumbs Trail — Writeup

**Category:** Digital Forensics
**Flag:** `CREST{Breadcrumbs2026Trail9X}`

## Challenge

A Linux application server returned to service after a suspicious overnight maintenance window. The evidence is a set of logs, shell history, service-state files and a recovery manifest. The task is to correlate them, find the privilege boundary and the local account transition, and recover the flag from the matching recovery manifest. Many `CREST{...}` strings are planted as decoys.

## Evidence

| File | Role |
|---|---|
| `home_deploy_bash_history` | Commands run by `deploy` |
| `usr_local_bin_rotate_worker_state` | State of the `rotate-worker` utility |
| `var_tmp_stage_state.txt` | Transient stage state |
| `srv_app_deploy_notes.txt` | Deploy handoff notes and timeline |
| `var_lib_app_worker_recovery_manifest.conf` | Recovery manifest (holds the flag) |
| `var_log_auth.log`, `var_log_audit_execve.log`, `var_log_syslog.log`, `var_log_journal_app_worker_export.log` | System logs |
| `var_lib_app_worker_history_20260918021406.state` | Not in the local folder; not reviewed |

## Analysis

1. **Timeline** (`srv_app_deploy_notes.txt`): the change window opened 2026-09-18 01:45 UTC, `deploy` requested a `rotate-worker` recovery, a worker session appeared from loopback, and recovery archive `9c7d4e21` reported checkpoint `7f31c2a9`.
2. **Privilege boundary** (`home_deploy_bash_history`): `deploy` ran `sudo /usr/local/bin/rotate-worker --recover`. The `rotate-worker` state file confirms `requested_by=deploy`, `effective_uid=0`, `runner=/var/tmp/.stage/.ws`, `recover_mode=compat`.
3. **Staging**: `deploy` created `.stage` (mode 700), copied `last-good.state` to `.stage/.state`, and ran `./.stage/.ws --quiet --state .stage/.state`. `var_tmp_stage_state.txt` shows `owner=deploy`, `last_transition=worker-context`, `archive_id=9c7d4e21` and `checkpoint=7f31c2a9`.
4. **Account transition**: the last command is `ssh worker@127.0.0.1 -p 22`, a hop from `deploy` to the local `worker` account over loopback.
5. **Matching manifest**: `var_lib_app_worker_recovery_manifest.conf` has `id=9c7d4e21` and `checkpoint=7f31c2a9`, matching the stage state and the notes. It was created at 02:14:07Z, which matches the history file name `...20260918021406`.

## Decoys

The files contain plain-text flag-shaped strings in comments and `note=` / `annotation=` fields. They sit on unrelated routine lines or carry IDs that don't tie to the chain, so they are not the answer. Examples:

- `CREST{TokenRefreshed47A}`
- `CREST{WorkerResumed60B}`
- `CREST{LogRotationOK73C}`
- `CREST{DeployRollback85O}`
- `CREST{BlueQuartz46L}`
- `CREST{AuditTrailClean59M}`
- `CREST{CacheRecovered66U}`

## Solution

The manifest's `fragment` field is Base64, as `encoding=base64` indicates:

```
Q1JFU1R7QnJlYWRjcnVtYnMyMDI2VHJhaWw5WH0=
```

```powershell
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("Q1JFU1R7QnJlYWRjcnVtYnMyMDI2VHJhaWw5WH0="))
```

Output:

```
CREST{Breadcrumbs2026Trail9X}
```

## Caveat

I did not review the auth, audit, syslog or journal logs, and the `worker_history` state file was not available. The chain above rests on the shell history, the state files, the notes and the manifest, which agree on the archive ID and checkpoint.
