# Contributing

This repository is a team CTF writeup archive. The structure is intentionally boring so that future solve notes can be dropped in without reorganising anything.

## Repository rules

1. **One challenge per folder.** Do not put two challenges in the same directory.
2. **Category folders are fixed.** Use the existing names: `crypto`, `forensic`, `misc`, `multi`, `network`, `osint`, `rev`, `stegno`, `web`.
3. **Never claim a teammate's solve.** Publish a teammate's writeup only with explicit attribution to the named author and handle. If the author is unknown, do not publish it.
4. **Preserve the author's technical content.** Formatting, file links, and a short archive header may be added; do not silently rewrite the solve or change its claims.
5. **Preserve attachments.** Do not edit, re-encode, or replace a challenge file. If you need a derived file, put it in `solve/` and explain how it was produced.
6. **Every solver must run from a clean checkout.** Read challenge data from `../attachments/`; do not hard-code absolute paths.
7. **Flags are exact.** Copy the accepted value, including the challenge's own prefix (`CREST{...}`, `ctf7{...}`, or lowercase `crest{...}`). Do not normalise it.

## Adding a challenge

Create this structure:

```text
<category>/
└── Challenge-Name/
    ├── README.md              # brief, author, flag, file index, run instructions
    ├── writeup.md             # full solve, with an attribution header
    ├── source-writeup.docx    # optional: original author-formatted file
    ├── attachments/           # exact files provided by the challenge
    └── solve/                 # tested solver + requirements (if needed)
```

Use **Title-Case-Hyphenated** folder names. Keep spaces out of paths so GitHub links and command-line examples stay simple.

### `README.md` template

````markdown
# Challenge Name

![Event](https://img.shields.io/badge/CREST_CTF_2.0-CTF7-101518?style=flat-square)
![Category](https://img.shields.io/badge/Category-Category_Name-8A4B08?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Difficulty-7A5A12?style=flat-square)
![Points](https://img.shields.io/badge/Points-000-2F5D3A?style=flat-square)
![Solves](https://img.shields.io/badge/Solves-000-1F5F73?style=flat-square)

> **Solved and written by** Author Name (`handle`) · **Team** Cyfer Trace · **Submitted** DD Month YYYY
> **Challenge author:** Event-credited author · **Created:** DD Month YYYY

## Challenge description

The official brief, copied accurately.

**Flag format:** `CREST{...}`

**Attachments:** [`file`](attachments/file)

## Flag

```text
CREST{...}
```

## Writeup

Read the full solve: **[writeup.md](writeup.md)**

The key insight in one line.

## Files

| File | What it is |
| --- | --- |
| `README.md` | This brief, metadata, file index and run instructions. |
| `writeup.md` | Full solve writeup by the named author. |
| `attachments/file` | Official challenge file. |
| `solve/solve.py` | What the solver does. |

## Notes

- Dependencies, caveats, and anything a reader should know before running.

## Run the solver

```bash
cd solve
python solve.py
```

---

[← Back to Category](../README.md) · [All writeups](../../README.md)
````

### `writeup.md` requirements

Every writeup starts with an attribution block:

```markdown
> **Solved and written by** Author Name (`handle`) · **Team** Cyfer Trace · **Submitted** DD Month YYYY
>
> **Official challenge:** Name · **Category:** Category · **Difficulty:** Difficulty · **Points:** N · **Solves:** N
>
> This writeup was contributed by the named teammate. It is not personal work by Ishant Choudhary.
```

A good writeup then answers these questions in order:

1. **What is the challenge?** A one-paragraph restatement, not a copy of the brief.
2. **What is the data?** File shapes, fields, and which parts are noise.
3. **What is the trick?** The vulnerability, encoding, metadata field, graph property, or VM behaviour.
4. **How do you execute it?** Commands and code a reader can follow.
5. **How do you know it is correct?** Exact flag, forward verification, hash, or a second independent check.
6. **What is reusable?** Two or three lessons, not a summary of the steps.

Include a `## Flag` section and a `## Reproduce` section where useful. Link the full solver instead of pasting hundreds of lines.

## Updating the category README

Every new challenge must update its category's `README.md` in the same commit:

1. Add a row to **Published writeups** with the author, difficulty, points, solves, and a link.
2. Update the **Published writeups** count in the header, splitting personal and teammate work.
3. Update the **Team result** line if the team total changed.
4. Add one short bullet to **Notes** explaining the trick.
5. If a challenge was previously listed under **Team clears without a published writeup**, move it out.

Do not list a team solve as a personal writeup. The distinction is the point of the category READMEs.

## Attachments and provenance

- Include the file exactly as downloaded. For a ZIP bundle, keep the original ZIP and, if useful, an extracted copy under `attachments/docs/`.
- Record where the file came from (challenge name, platform, original filename).
- If a file is too large for the repository, add an `attachments/README.md` with the official link and size instead of committing it.
- If you add `SHA256SUMS`, generate it from the files in place and do not edit the attachments afterwards.
- Do not commit secrets, credentials, personal data, or anything from a live environment.

## Solver style

- Python 3.10+.
- Prefer the standard library. Add a `requirements.txt` only when a dependency is genuinely needed.
- Use `pathlib` and resolve paths relative to `__file__`.
- Print the intermediate values a reader needs to follow the solve, then a final `[+] FLAG: ...` line.
- Keep output deterministic.
- Do not make network requests in a solver.

## Validation checklist

Before committing:

```bash
# 1. Run the solver from its own directory
cd category/Challenge-Name/solve
python solve.py

# 2. Run it from the repository root as well
cd ../../..
python category/Challenge-Name/solve/solve.py

# 3. Check every relative link in the Markdown
#    (or use the repository's link checker)

# 4. Confirm the flag in README.md, writeup.md, and solver output match
```

Also check:

- [ ] The category README links to the new challenge and names its author.
- [ ] The challenge README links to `writeup.md`, every attachment, and `solve/`.
- [ ] `writeup.md` names the author and says it is not the repository owner's personal work.
- [ ] No absolute Windows paths (`C:\...`) appear in a solver or README.
- [ ] No `__pycache__`, `.venv`, or editor files are staged.
- [ ] The flag is not presented as a live target.

## Commit messages

Use a short, scoped message:

```text
crypto: add Close Enough writeup
osint: add Papertrail attachments and solver
docs: attribute teammate writeups and update indexes
```

## Attribution

By contributing, you confirm that you wrote the writeup or have permission to publish it, and that challenge files are included only for study and reproducibility. See [`NOTICE.md`](NOTICE.md) and [`CONTRIBUTORS.md`](CONTRIBUTORS.md).
