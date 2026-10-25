> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 10:40 a.m.
>
> **Official challenge:** Query Shadow · **Category:** Web · **Difficulty:** Hard · **Points:** 400 · **Solves:** 232
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Shadow Directory

## Challenge Description

Shadow Directory is an internal staff directory that lets users register,
choose a display name, and view colleagues who share that display name.

The goal is to recover the flag in the format `crest{...}`.

## Discovery

After registering an account and setting a normal display name such as
`Falcon`, the **Colleagues** page displayed all users with that display name.

The display name is stored on the account and later used by the colleagues
lookup. This suggested testing whether the stored value was safely handled when
the lookup query was built.

## Exploitation

I set my display name to the following SQL injection payload:

```text
x' UNION SELECT name, value FROM secrets --
```

The profile accepted and stored the payload. When I then opened the
**Colleagues** page, the stored display name was evaluated as part of the
database query. The injected `UNION SELECT` returned rows from the `secrets`
table.

The page displayed the following result:

```text
Username: vault_token
Display name: crest{sec0nd_0rder_1nj3ct10n_sh4d0w}
```

## Flag

```text
crest{sec0nd_0rder_1nj3ct10n_sh4d0w}
```

## Vulnerability

This is a second-order SQL injection. The malicious input is stored first and
executed later when the colleagues query uses the saved display name. The
application should use parameterized queries for both storing and retrieving
display names, and should validate input according to the intended display-name
format.
