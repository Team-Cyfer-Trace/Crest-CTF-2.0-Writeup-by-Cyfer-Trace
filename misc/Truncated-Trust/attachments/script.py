import hashlib
import itertools
import json
from pathlib import Path

from z3 import BitVec, BitVecVal, Extract, Solver, sat

# Load challenge data.
data = json.loads(Path("data.json").read_text())

M = data["modulus"]
A = data["multiplier_a"]
C = data["increment_c"]
OUTPUTS = data["leaked_outputs"]
CIPHERTEXT = bytes.fromhex(data["flag_ciphertext_hex"])

BITS = 64
HIDDEN_BITS = data["hidden_bits"]

# Model consecutive 64-bit states.
states = [BitVec(f"s{i}", BITS) for i in range(len(OUTPUTS) + 1)]

solver = Solver()

# Apply the LCG recurrence. Bit-vector arithmetic wraps
# automatically modulo 2^64.
a = BitVecVal(A, BITS)
c = BitVecVal(C, BITS)

for i in range(len(states) - 1):
    solver.add(states[i + 1] == a * states[i] + c)

# Constrain the leaked upper 24 bits of each state.
for i, output in enumerate(OUTPUTS):
    solver.add(
        Extract(63, HIDDEN_BITS, states[i]) == output
    )

print("[*] Solving for the hidden states...")

if solver.check() != sat:
    raise RuntimeError("No satisfying state sequence found.")

model = solver.model()

recovered = [
    model.eval(state, model_completion=True).as_long()
    for state in states
]

print("[+] Recovered states:")
for i, state in enumerate(recovered):
    print(f"    state[{i}] = 0x{state:016x}")

# Verify the recurrence and leaked outputs.
for i in range(len(OUTPUTS)):
    assert recovered[i + 1] == (
        A * recovered[i] + C
    ) % M

    assert recovered[i] >> HIDDEN_BITS == OUTPUTS[i]

key = recovered[8].to_bytes(8, "big")

print(f"\n[+] state[8] = 0x{recovered[8]:016x}")
print(f"[+] Key bytes = {key.hex()}")


def decrypt(counter_width, endian, start):
    """Try a counter encoding for the documented SHA-256 stream."""
    stream = bytearray()
    counter = start

    while len(stream) < len(CIPHERTEXT):
        counter_bytes = counter.to_bytes(
            counter_width, endian
        )

        block = hashlib.sha256(key + counter_bytes).digest()
        stream.extend(block)
        counter += 1

    return bytes(
        x ^ y
        for x, y in zip(CIPHERTEXT, stream)
    )


print("\n[*] Testing common counter encodings...")

found = False

for width, endian, start in itertools.product(
    (1, 2, 4, 8),
    ("big", "little"),
    (0, 1),
):
    plaintext = decrypt(width, endian, start)

    if plaintext.startswith(b"ctf7{"):
        print("\n[+] FLAG:", plaintext.decode(errors="replace"))
        print(
            f"[+] Counter encoding: "
            f"{width}-byte {endian}-endian, starting at {start}"
        )
        found = True
        break

if not found:
    print(
        "[-] No flag found with the tested counter encodings. "
        "Check the challenge's original encryption implementation "
        "for the exact counter serialization."
    )