Truncated Trust -- leaked PRNG data
====================================

Our internal service uses a home-rolled PRNG (a linear congruential
generator) to derive per-session keys:

    state[i+1] = (a * state[i] + c) mod m

- m, a, and c are all PUBLIC (this PRNG's parameters were never
  secret -- see data.json "modulus" / "multiplier_a" / "increment_c").
- state[0]: secret random seed. This, and every subsequent internal
  state, is what actually needs protecting.

Due to a logging bug, 8 consecutive outputs were leaked to a debug
log -- but only the TOP 24 bits of each 64-bit
state, i.e. state[i] >> 40. The low 40 bits of every leaked state
(most of each 64-bit value) are NOT in the log. See "leaked_outputs"
in data.json (index 0..7, in order).

The flag was encrypted using state[8] (the very next state after the
8 leaked ones, which was never output anywhere) as a key, via:

    key_bytes = state[8].to_bytes(8, "big")
    keystream = SHA256(key_bytes || counter) || SHA256(key_bytes || counter+1) || ...
    ciphertext = flag_bytes XOR keystream[:len(flag_bytes)]

The ciphertext (hex) is in data.json as "flag_ciphertext_hex".

Recover a, c, and the hidden low bits of the leaked states from the
truncated outputs alone, predict state[8], and decrypt the flag.
