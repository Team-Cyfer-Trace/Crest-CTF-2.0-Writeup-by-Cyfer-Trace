> **Solved and written by** Bryan (`RadixCobra19`) · **Team** Cyfer Trace · **Submitted** Oct. 23, 2026, 3:18 p.m.
>
> **Official challenge:** NP In Disguise · **Category:** Miscellaneous · **Difficulty:** Hard · **Points:** 600 · **Solves:** 96
>
> This writeup was contributed by the named teammate for the Cyfer Trace archive. It is not personal work by Ishant Choudhary. Light formatting and file links were added here; the technical content is the author's.

---

# NP In Disguise — CTF Writeup

## 1. Challenge Overview

**Category:** Reverse Engineering / Cryptography / SAT  
**Flag format:** `ctf7{...}`

The challenge provides three components:

- `program(1).esolang` — the NP-lang program containing Boolean constraints and encrypted data.
- `SPEC.md` — the specification of the custom programming language.
- `interpreter.py` — the reference interpreter that checks a candidate assignment and decrypts the payload if all constraints pass.

The objective is to find an assignment of binary values to the program's variables that satisfies every constraint and allows the interpreter to reveal the flag.

## 2. Understanding NP-lang

The program declares 70 Boolean variables:

```text
VARS 70
```

Each variable, from `x0` to `x69`, must be assigned either `0` or `1`.

The main instruction used in the program is `CLAUSE`, which represents a three-literal Boolean OR expression.

For example:

```text
CLAUSE x18 x10 !x64
```

This clause succeeds if at least one of the following is true:

- `x18 = 1`
- `x10 = 1`
- `x64 = 0`

A positive literal such as `x18` is true when its variable equals `1`. A negated literal such as `!x64` is true when its variable equals `0`.

If all three literals are false, the interpreter rejects the assignment immediately.

The program contains **750 clauses**, so the objective is to find a 70-bit assignment satisfying all of them.

## 3. Recognizing the SAT Problem

Each `CLAUSE` instruction is equivalent to a clause in a Boolean satisfiability problem, specifically a 3-SAT instance.

For example:

```text
CLAUSE x18 x10 !x64
CLAUSE x9 x69 !x52
CLAUSE x55 x64 x35
```

These can be represented as:

- `(x18 OR x10 OR NOT x64)`
- `(x9 OR x69 OR NOT x52)`
- `(x55 OR x64 OR x35)`

The complete program defines a conjunction of all 750 clauses. A valid assignment must make every clause true.

Trying random bitstrings would be inefficient because a candidate that violates even one clause is rejected. Instead, the problem can be treated as a SAT-solving task, using a solver or a suitable constraint-solving script to find a satisfying assignment.

## 4. Obtaining a Valid Assignment

The interpreter accepts the complete assignment as a command-line argument rather than exploring the possible branches itself.

The assignment must contain exactly 70 binary digits, ordered as follows:

```text
bit 0  -> x0
bit 1  -> x1
...
bit 69 -> x69
```

The recovered satisfying assignment is:

```text
0100001110101011011101101101011011011001001010101000100010010000011101
```

This assignment satisfies all 750 clauses in the provided program, allowing execution to reach `HALT_OK`.

## 5. Understanding the Payload Encryption

The program stores the encrypted payload as hexadecimal data in a `DATA` instruction. The reference interpreter retrieves the data under the name `payload`.

When `HALT_OK` is reached, the interpreter derives a cryptographic key from the assignment.

First, the 70 bits are split into groups of eight. The final group contains six bits and is padded with two zeros on the right.

The resulting bytes are hashed using SHA-256:

```text
key = SHA256(packed_assignment)
```

The interpreter then decrypts the payload by XORing each ciphertext byte with the corresponding repeating key byte:

```text
plaintext[i] = ciphertext[i] XOR key[i % 32]
```

Here, `key` is the 32-byte SHA-256 digest. This means that satisfying the Boolean constraints is the key to recovering the correct decryption key.

## 6. Running the Interpreter

Place the interpreter and the `.esolang` program in the same directory, then run:

```bash
python3 interpreter.py "program(1).esolang" 0100001110101011011101101101011011011001001010101000100010010000011101
```

The interpreter checks the assignment against the clauses. If they all pass, it reaches `HALT_OK`, computes the SHA-256 key, decrypts the payload, and prints the plaintext.

## 7. Result and Verification

The assignment was checked against the provided program:

- Number of variables: **70**
- Number of clauses: **750**
- Unsatisfied clauses: **0**
- Final instruction reached: `HALT_OK`
- Decrypted payload: text matching the required flag format

## 8. Final Flag

```text
ctf7{s4t_1s_h4rd_but_n0t_f0r_us}
```

## 9. Conclusion

This challenge combines Boolean satisfiability and symmetric decryption. The custom NP-lang syntax disguises a 3-SAT instance, while the interpreter uses the successful assignment to derive a SHA-256 key. Once a satisfying assignment is found, the encrypted payload can be decrypted using a repeating-key XOR operation.

The key insight is that the assignment is not merely a collection of guesses: it must satisfy every Boolean constraint, and the exact same bit sequence is used to derive the decryption key.
