"""
demos/rainbow.py — Demo 5: Rainbow Table Attack

Shows WHY unsalted hashes are catastrophically insecure for password
storage.  A "rainbow table" is a precomputed dictionary that maps hash
values back to their original plaintext passwords.  If the database
does not use a salt, the attacker skips brute-forcing entirely and
simply looks up the stolen hash — like checking a word in a dictionary.

The demo has two acts:
  1. ATTACK — The audience picks a common password, the program hashes
     it with plain SHA-256, and then instantly "cracks" it by looking
     up the hash in a small prebuilt rainbow table.
  2. DEFENSE — The same password is hashed twice with different random
     salts, producing completely different hashes.  The rainbow table
     lookup fails both times, showing that salt neutralizes the attack.

Narrative position
──────────────────
This is the FIFTH and final demo.  It ties together every earlier
lesson into a concrete attack-and-defense scenario:

    Demo 1–2: Hashes map inputs to outputs (and collisions are real).
    Demo 3:   Cryptographic hashes are unpredictable (avalanche).
    Demo 4:   Slow hashing makes brute-force expensive.
    Demo 5:   Without a salt, even slow hashing is not enough — an
              attacker can precompute everything in advance.

Key vocabulary introduced here:
  • Rainbow table — a precomputed lookup table that maps hash outputs
    back to their inputs.  Named after the original 2003 paper by
    Philippe Oechslin which used a "rainbow" of reduction functions.
    Modern tables can contain billions of entries and occupy terabytes.
  • Salt — a random value (typically 16+ bytes) generated uniquely for
    each password.  It is stored alongside the hash in the database
    (it does not need to be secret).  Salt makes rainbow tables useless
    because the attacker would need a SEPARATE table for every possible
    salt value — an impossibly large amount of storage.
  • Unsalted hash — a hash computed directly from the password with no
    salt.  Two users with the same password produce identical hashes,
    and all of them can be cracked with a single rainbow table lookup.
  • Pre-image attack — finding an input that produces a given hash
    output.  Rainbow tables are a practical pre-image attack against
    weak (unsalted) password storage.
"""

import hashlib
import os
import time
import binascii

from demos.ui import (
    header, setup_text, takeaway, label, info, good, bad,
    pause, prompt, draw_box,
    C_BOLD, C_CYAN, C_DIM, C_GREEN, C_RED, C_RESET,
    ARROW,
)

# ── Precomputed rainbow table ──────────────────────────────────────
# In real life these contain billions of entries (terabytes of data).
# Ours is tiny but demonstrates the concept perfectly.

COMMON_PASSWORDS = [
    "123456",    "password",  "12345678", "qwerty",   "abc123",
    "monkey",    "letmein",   "dragon",   "111111",   "baseball",
    "iloveyou",  "trustno1",  "sunshine",  "master",   "welcome",
    "shadow",    "ashley",    "football",  "jesus",    "michael",
    "ninja",     "mustang",   "password1", "hunter2",  "batman",
]

RAINBOW_TABLE = {}   # hash → plaintext


def _build_rainbow_table():
    """Populate the rainbow table with SHA-256 hashes of common passwords."""
    for pw in COMMON_PASSWORDS:
        h = hashlib.sha256(pw.encode()).hexdigest()
        RAINBOW_TABLE[h] = pw


def run():
    """Entry point — called from the main menu."""

    _build_rainbow_table()

    header("Demo 5 — Rainbow Table Attack")
    setup_text("""
        Imagine an attacker has stolen a database of password hashes.
        Instead of guessing passwords one at a time, the attacker
        uses a RAINBOW TABLE — a giant precomputed dictionary that
        maps known hash values back to their original passwords.

        How it works:
          1. BEFORE the breach, the attacker hashes millions of common
             passwords and stores them in a lookup table:
                 hash("password") → "password"
                 hash("dragon")   → "dragon"
                 hash("123456")   → "123456"
                 … billions more …

          2. AFTER stealing a database, the attacker simply looks up
             each victim's hash in the table.  If it matches, the
             password is instantly revealed — no computation needed.

        This attack works ONLY when the database stores plain, unsalted
        hashes.  We will first see the attack succeed, then see how
        adding a SALT defeats it completely.
    """)
    pause("see the rainbow table")

    # ━━ Act 1: Show the Precomputed Table ━━━━━━━━━━━━━━━━━━━━━━━━━
    label("The Attacker's Rainbow Table  (showing 10 of 25 entries)")
    info("Each row is a password and its SHA-256 hash, computed in advance.")
    print()

    rows = []
    for pw in COMMON_PASSWORDS[:10]:
        h = hashlib.sha256(pw.encode()).hexdigest()
        rows.append(f"  {pw:<14} {ARROW}  {C_DIM}{h[:32]}…{C_RESET}")
    draw_box(rows, color=C_RED)
    print()
    info("Real rainbow tables contain BILLIONS of entries and can occupy")
    info("terabytes of disk space.  They are freely downloadable online.")

    pause("simulate the attack")

    # ━━ Act 2: Attack Phase ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    label("Attack Simulation")
    info("Pretend a company stored their passwords as plain SHA-256 hashes.")
    info("The attacker has stolen the hash database.")
    print()
    victim_pw = prompt("Pick a victim password  (Enter for 'dragon')") or "dragon"
    victim_hash = hashlib.sha256(victim_pw.encode()).hexdigest()

    print(f"\n    Stolen hash : {C_CYAN}{victim_hash}{C_RESET}")
    print(f"    Searching rainbow table", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    time.sleep(0.3)

    result = RAINBOW_TABLE.get(victim_hash)
    if result:
        print(f"\n\n    {C_RED}{C_BOLD}CRACKED!{C_RESET}")
        print(f"    The password is: {C_RED}{C_BOLD}{result}{C_RESET}")
        print()
        bad("The lookup was instant — no brute-forcing required.")
        bad("Every user with this password is compromised in one step.")
    else:
        print(f"\n\n    {C_GREEN}Not found in this 25-entry demo table.{C_RESET}")
        info("A real table with billions of entries might still crack it.")

    pause("see how SALT defeats this attack")

    # ━━ Act 3: Defense — Salted Hashes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    label("Defense — Adding a Salt")
    info("A SALT is a random string generated uniquely for each user.")
    info("Before hashing, the salt is mixed into the password:")
    info("")
    info("    hash( salt + password )  →  stored hash")
    info("")
    info("The salt is stored in the clear alongside the hash — it does")
    info("NOT need to be secret.  Why?  Because the salt's job is NOT to")
    info("hide anything.  Its job is to make every hash UNIQUE.  Even if")
    info("the attacker can see the salt, they would have to build an")
    info("entirely new rainbow table just for that specific salt value.")
    info("With a different random salt per user, no single precomputed")
    info("table works against anyone.")
    print()

    salt_a = os.urandom(12)
    salt_b = os.urandom(12)
    salted_a = hashlib.sha256(salt_a + victim_pw.encode()).hexdigest()
    salted_b = hashlib.sha256(salt_b + victim_pw.encode()).hexdigest()

    print(f"    Same password : {C_BOLD}{victim_pw}{C_RESET}")
    print()
    print(f"    User A  salt  : {C_DIM}{binascii.hexlify(salt_a).decode()}{C_RESET}")
    print(f"    User A  hash  : {C_GREEN}{salted_a}{C_RESET}")
    print()
    print(f"    User B  salt  : {C_DIM}{binascii.hexlify(salt_b).decode()}{C_RESET}")
    print(f"    User B  hash  : {C_GREEN}{salted_b}{C_RESET}")

    pause("attempt the rainbow lookup on salted hashes")

    print(f"    Rainbow lookup for User A hash", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f" {C_GREEN}{C_BOLD}NOT FOUND ✓{C_RESET}")

    print(f"    Rainbow lookup for User B hash", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f" {C_GREEN}{C_BOLD}NOT FOUND ✓{C_RESET}")

    print()
    info("The rainbow table was built for UNSALTED hashes.")
    info("With a salt mixed in, the resulting hash is completely different")
    info("from anything in the table — the lookup fails every time.")

    # ── Takeaway ────────────────────────────────────────────────────
    takeaway("""
        Without a salt, identical passwords produce identical hashes.
        An attacker can crack them all at once with a single table
        lookup — no computation required.

        A random salt makes every hash unique:
          • The attacker would need a separate rainbow table for every
            possible salt value.
          • A 12-byte salt has 2⁹⁶ possible values.  Here is the math:
            12 bytes × 8 bits per byte = 96 bits, and each bit doubles
            the possibilities (2 × 2 × 2… ninety-six times = 2⁹⁶).
            That is a number with 29 digits — building a table for
            each one is physically impossible.

        Remember the key question: "If the attacker can see the salt,
        why can't they just use it?"  They CAN use it — but only to
        check ONE guess at a time, which brings us right back to the
        slow brute-force attack from Demo 4.  The salt's power is that
        it destroys the attacker's ability to reuse precomputed work.

        This is why every modern password storage system — bcrypt,
        scrypt, Argon2, PBKDF2 — generates a unique salt automatically.
        If a system stores unsalted hashes, it is fundamentally broken.

        Combined with the slow hashing from Demo 4, salt + key stretching
        is the industry-standard defense for password storage.
    """)
    pause("return to menu")
