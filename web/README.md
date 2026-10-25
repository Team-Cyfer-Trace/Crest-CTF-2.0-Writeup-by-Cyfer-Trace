# Web

Application logic, identity flows, access control, and the small assumptions that turn a feature into a vulnerability.

**Team result:** 4 of 4 cleared · **Published writeups:** 4 (0 personal, 4 teammate)

## Published writeups

| Challenge | Author | Difficulty | Points | Solves | Writeup |
| --- | --- | --- | ---: | ---: | --- |
| [Well Known](Well-Known/) | Hrishikesh (`hrishikesh`) | Easy | 200 | 196 | [read](Well-Known/writeup.md) |
| [White Pixel](White-Pixel/) | Hrishikesh (`hrishikesh`) | Medium | 200 | 74 | [read](White-Pixel/writeup.md) |
| [Session Drift](Session-Drift/) | Hrishikesh (`hrishikesh`) | Medium | 300 | 174 | [read](Session-Drift/writeup.md) |
| [Query Shadow](Query-Shadow/) | Hrishikesh (`hrishikesh`) | Hard | 400 | 232 | [read](Query-Shadow/writeup.md) |

All challenges in this category were cleared by the team.

## Notes

- `Query Shadow` stores a display name and later splices it into an XPath query; a UNION-style payload reaches the flag node.
- `Session Drift` uses a Flask-style client-side session cookie with a weak signing key.
- `Well Known` hides the flag in `/.well-known/security.txt`.
- `White Pixel` is a near-blank page; a 60×84 image uses two almost-identical whites to spell the flag.

---

[← All categories](../README.md) · [All writeups](../README.md)
