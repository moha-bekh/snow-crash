#!/usr/bin/env python3

cipher = "cdiiddwpgswtgt"

for shift in range(26):
    decoded = "".join(
        chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
        for ch in cipher
    )
    print(f"{shift:02d}: {decoded}")