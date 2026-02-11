"""
demos/avalanche.py — Demo 3: The Avalanche Effect

Shows that a GOOD cryptographic hash is wildly sensitive to input
changes.  Flipping a single character in the input should flip roughly
half of the bits in the output.  This property is called the Avalanche
Effect and is one of the core requirements of any secure hash function.

The audience enters two similar strings (or uses the defaults) and the
program displays their SHA-256 hashes side-by-side in three views:

    1. Raw hex — with a character-level diff line.
    2. Binary  — with a bit-level diff line (first 64 of 256 bits).
    3. Summary — percentage of bits that flipped vs. the ideal 50 %.

Narrative position
──────────────────
This is the THIRD demo.  It transitions from "hash as bucket tool"
(Demos 1–2) to "hash as security tool" (Demos 4–5):

    Demo 1–2: Hashes organize data efficiently.
    Demo 3:   Hashes also HIDE information — you cannot reverse-
              engineer the input from the output.

Key vocabulary introduced here:
  • Avalanche Effect — the property that a tiny input change causes
    a huge output change.  Named after an actual avalanche: a small
    trigger produces an enormous result.
  • SHA-256 — Secure Hash Algorithm, 256-bit output.  Part of the
    SHA-2 family designed by the NSA and published by NIST.  Used in
    TLS certificates, Git commits, Bitcoin mining, and more.
  • Bit — a single binary digit, 0 or 1.  The most basic unit of
    information in computing.
"""

import hashlib

from demos.ui import (
    header, setup_text, takeaway, label, info,
    pause, prompt,
    C_BOLD, C_CYAN, C_DIM, C_RED, C_GREEN, C_RESET,
)


def _hex_to_bin(hex_str):
    """Convert a hex digest string to a binary string of 0s and 1s."""
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)


def run():
    """Entry point — called from the main menu."""

    header("Demo 3 — The Avalanche Effect")
    setup_text("""
        So far we have used a simple toy hash that just adds letters
        together.  That works for sorting items into buckets, but an
        attacker could easily reverse it or predict the output.

        A CRYPTOGRAPHIC hash function is designed to be:
          • Unpredictable — you cannot guess the output, even if the
            input changes by only one character.
          • Irreversible  — given the output, you CANNOT work backward
            to recover the input (this is called the ONE-WAY property).
          • Pattern-free  — the output looks like total randomness,
            so attackers have nothing to exploit.

        SHA-256 ("Secure Hash Algorithm, 256-bit") is a widely used
        cryptographic hash.  One of its key properties is the
        AVALANCHE EFFECT:

            Changing even a SINGLE character in the input should flip
            roughly HALF of the bits in the output.

        Why half?  If the output were truly random, each bit would have
        a 50/50 chance of flipping.  So the ideal average is 50%.
        If significantly FEWER bits change, it means patterns remain —
        and an attacker could use those patterns.
        If 100% of bits always flipped, that itself would be a pattern!

        Let’s see it in action.  Enter two similar strings and we will
        compare their SHA-256 hashes character by character AND bit by
        bit.
    """)
    pause("start the demo")

    # ── Collect input ───────────────────────────────────────────────
    default_a, default_b = "password", "passwore"
    in_a = prompt(f"String 1  (Enter for '{default_a}')") or default_a
    in_b = prompt(f"String 2  (Enter for '{default_b}')") or default_b

    h_a = hashlib.sha256(in_a.encode()).hexdigest()
    h_b = hashlib.sha256(in_b.encode()).hexdigest()
    b_a = _hex_to_bin(h_a)
    b_b = _hex_to_bin(h_b)

    # ── Part 1: Input comparison ────────────────────────────────────
    label("Inputs")
    max_len = max(len(in_a), len(in_b))
    padded_a = in_a.ljust(max_len)
    padded_b = in_b.ljust(max_len)

    diff_markers = ""
    for ca, cb in zip(padded_a, padded_b):
        if ca == cb:
            diff_markers += f"{C_DIM}·{C_RESET}"
        else:
            diff_markers += f"{C_RED}{C_BOLD}^{C_RESET}"

    print(f'    A: "{C_BOLD}{in_a}{C_RESET}"')
    print(f'    B: "{C_BOLD}{in_b}{C_RESET}"')
    print(f"       {diff_markers}")

    char_diffs = sum(1 for a, b in zip(padded_a, padded_b) if a != b)
    char_diffs += abs(len(in_a) - len(in_b))

    info(f"The two inputs differ by {char_diffs} character(s).")
    info("The '^' markers show exactly which character(s) changed.")

    pause("see the resulting hashes")

    # ── Part 2: Hex comparison ──────────────────────────────────────
    label("SHA-256 Output — Hexadecimal  (64 characters)")
    info(
        "Hexadecimal (or ‘hex’) is a way of writing numbers using 16"
    )
    info(
        "symbols: 0–9 plus A–F.  It is more compact than binary (0s and"
    )
    info(
        "1s) and easier to read.  Each hex character represents 4 bits."
    )
    info(
        "SHA-256 outputs 64 hex characters × 4 bits = 256 bits total."
    )
    print()

    hex_diff = ""
    hex_diffs = 0
    for ca, cb in zip(h_a, h_b):
        if ca == cb:
            hex_diff += f"{C_DIM}·{C_RESET}"
        else:
            hex_diff += f"{C_RED}^{C_RESET}"
            hex_diffs += 1

    print(f"    A: {C_CYAN}{h_a}{C_RESET}")
    print(f"    B: {C_CYAN}{h_b}{C_RESET}")
    print(f"       {hex_diff}")
    print()
    info(f"{hex_diffs} of 64 hex characters are different ({hex_diffs / 64 * 100:.0f}%).")
    info(
        "The '·' dots mark positions that stayed the same."
    )
    info(
        "The '^' carets mark positions that changed."
    )

    pause("see the binary (bit-level) view")

    # ── Part 3: Binary comparison (first 64 of 256 bits) ───────────
    SHOW_BITS = 64
    label(f"Binary View — first {SHOW_BITS} of 256 bits")
    info(
        "Bits are the actual 0s and 1s the computer stores."
    )
    info(
        "We show the first 64 bits, grouped into bytes (8 bits each)."
    )
    print()

    bit_diffs_total = sum(1 for a, b in zip(b_a, b_b) if a != b)

    colored_a = ""
    colored_b = ""
    bit_diff_line = ""

    for i in range(SHOW_BITS):
        if b_a[i] == b_b[i]:
            colored_a    += f"{C_DIM}{b_a[i]}{C_RESET}"
            colored_b    += f"{C_DIM}{b_b[i]}{C_RESET}"
            bit_diff_line += f"{C_DIM}·{C_RESET}"
        else:
            colored_a    += f"{C_CYAN}{C_BOLD}{b_a[i]}{C_RESET}"
            colored_b    += f"{C_RED}{C_BOLD}{b_b[i]}{C_RESET}"
            bit_diff_line += f"{C_RED}^{C_RESET}"

        # Insert a space every 8 bits for readability
        if (i + 1) % 8 == 0 and i < SHOW_BITS - 1:
            colored_a    += " "
            colored_b    += " "
            bit_diff_line += " "

    print(f"    A: {colored_a}")
    print(f"    B: {colored_b}")
    print(f"       {bit_diff_line}")
    print()
    pct = bit_diffs_total / 256 * 100
    info(f"{bit_diffs_total} of 256 total bits flipped ({pct:.0f}%).")
    info(f"The ideal is 50% (128 bits) — the hallmark of total randomness.")
    if pct > 40:
        info(f"This result is strong: SHA-256 is behaving like a good scrambler.")

    # ── Takeaway ────────────────────────────────────────────────────
    takeaway(f"""
        Changing just {char_diffs} character(s) in the input flipped
        {bit_diffs_total} out of 256 bits — that is {pct:.0f}% of the output.

        This is the Avalanche Effect.  It is what makes a cryptographic
        hash function different from our simple toy hash:
          • It is ONE-WAY — you cannot figure out the original input by
            looking at the hash, just as you cannot un-bake a cake to
            get the raw eggs back.
          • It is UNPREDICTABLE — two nearly-identical inputs produce
            wildly different hashes.
          • There is NO SHORTCUT — the only way to find the input that
            matches a given hash is to try every possibility.

        These properties are what allow hashing to protect passwords
        (Demo 4) and defend against pre-built attack tables (Demo 5).
    """)
    pause("return to menu")
