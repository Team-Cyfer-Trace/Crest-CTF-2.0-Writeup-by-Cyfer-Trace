> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:09 p.m.
>
> **Official challenge:** White Pixel · **Category:** Web · **Difficulty:** Medium · **Points:** 200 · **Solves:** 74
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# White Pixel — Writeup

## Challenge

The challenge presents a completely white page:

```text
http://2.31.70.16:5500/
```

The flag format is `crest{...}`.

## Page Inspection

Inspecting the page source shows that it contains only a white background and
an image:

```html
<img id="v" src="/q.png" alt="">
```

The image is only 60×84 pixels and appears blank because its pixels are almost
white.

## Extracting the Hidden Image

The image uses two very similar colors:

```text
(255, 255, 255)  # normal white
(255, 255, 254)  # slightly different white
```

Treating pixels with blue value `254` as set pixels and pixels with blue value
`255` as unset pixels reveals a block-letter pattern:

```text
################################################
################################################
################################################
############                    ################
############                    ################
############                    ################
################################################
################################################
################################################
############
############
############
############
```

After ignoring the padding and interpreting the pattern as a bitmap, it forms
the letter `P`.

## Flag

```text
crest{p}
```
