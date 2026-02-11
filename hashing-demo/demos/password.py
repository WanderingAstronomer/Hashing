"""
demos/password.py — Demo 4: Password Hashing (Fast vs. Slow)

Demonstrates WHY passwords must be stored with intentionally slow hash
functions rather than fast ones like SHA-256.

The audience hashes the same password twice — once with SHA-256 (near-
instant) and once with PBKDF2 at 600,000 iterations (perceptibly slow).
A live progress bar makes the delay visible and visceral.  A side-by-
side comparison table summarizes the tradeoff.

Narrative position
──────────────────
This is the FOURTH demo.  It applies the theory from Demos 1–3 to a
real-world security problem:

    Demo 1–2: Hashes organize data.
    Demo 3:   Cryptographic hashes hide information.
    Demo 4:   The SPEED of a hash matters for password security.
    Demo 5:   What happens when you ignore Demo 4's lesson.

Key vocabulary introduced here:
  • Brute-force attack — trying every possible password until you
    find the right one.  Speed is the attacker's best friend.
  • PBKDF2 (Password-Based Key Derivation Function 2) — a standard
    algorithm that runs a fast hash (like SHA-256) thousands of times
    in a loop, making each guess expensive.  Defined in RFC 8018.
  • Iterations — the number of times PBKDF2 re-hashes internally.
    More iterations = slower = safer.  OWASP recommends ≥600,000
    for PBKDF2-HMAC-SHA256 as of 2023.
  • Salt — a random value mixed into the password before hashing.
    Ensures that even identical passwords produce different hashes.
    (Salt is explored further in Demo 5.)
  • Key stretching — the general technique of making a hash function
    artificially slow.  PBKDF2, bcrypt, scrypt, and Argon2 are all
    key-stretching algorithms.
"""

import hashlib
import os
import time
import binascii

from demos.ui import (
    header, setup_text, takeaway, label, info, bad,
    pause, prompt, draw_box, progress_bar,
    C_BOLD, C_CYAN, C_DIM, C_GREEN, C_RED, C_RESET,
)


def run():
    """Entry point — called from the main menu."""

    header("Demo 4 — Password Hashing: Fast vs. Slow")
    setup_text("""
        First, the most important question: WHY hash passwords at all?
        Why not just store them directly in a database?

        Because databases get stolen.  Every year, hackers break into
        companies and download their entire user tables.  If passwords
        are stored in plain text, the attacker instantly has every
        user’s password — and since most people reuse passwords, the
        damage spreads far beyond that one site.

        Hashing is the defense: instead of storing the password itself,
        the server stores the HASH of the password.  When you log in,
        the server hashes what you typed and compares it to the stored
        hash.  Even if an attacker steals the database, they only get
        hashes — and as we learned in Demo 3, a hash is ONE-WAY, so
        they cannot simply reverse it.

        But there is a catch.  Fast hash functions like SHA-256 can
        process billions of guesses per second on a GPU (Graphics
        Processing Unit — the powerful chip that renders video games,
        which attackers repurpose for cracking passwords).  If each
        guess takes a billionth of a second, even a strong 8-character
        password can be cracked in minutes.

        Password hash functions solve this by being intentionally SLOW.
        They run the underlying hash thousands of times in a loop so
        that each single guess becomes expensive.  This technique is
        called KEY STRETCHING.

        We will hash the same password with both approaches and
        FEEL the difference in real time.
    """)
    pause("start the demo")

    pwd = prompt("Enter a password to hash  (Enter for 'hunter2')") or "hunter2"

    # ━━ Round 1: Fast Hash ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    label("Round 1 — Fast Hash  (SHA-256)")
    info("SHA-256 computes a unique 256-bit \"fingerprint\" in a single pass.")
    info("Think of it like a fingerprint: it uniquely identifies the input,")
    info("but you cannot reconstruct a person from their fingerprint alone.")
    info("SHA-256 was designed for speed — ideal for files, NOT passwords.")
    pause("compute the fast hash")

    start = time.time()
    h_fast = hashlib.sha256(pwd.encode()).hexdigest()
    elapsed_fast = time.time() - start

    print(f"    Password : {C_BOLD}{pwd}{C_RESET}")
    print(f"    Hash     : {C_CYAN}{h_fast}{C_RESET}")
    print(f"    Time     : {C_RED}{C_BOLD}< 0.001 seconds  ⚡{C_RESET}")
    print()
    bad("At this speed, an attacker with a modern GPU could try")
    bad("roughly 10 BILLION SHA-256 hashes per second.")
    info(
        "(A GPU is a Graphics Processing Unit — the chip in your"
    )
    info(
        "computer that renders video games.  Attackers repurpose its"
    )
    info(
        "massive parallel processing power for cracking passwords.)"
    )
    info(
        "At 10 billion guesses/sec, every possible 6-character password"
    )
    info(
        "(letters + digits) could be exhausted in under one second."
    )

    pause("see the slow hash")

    # ━━ Round 2: Slow Hash ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    iterations = 600_000
    label(f"Round 2 — Slow Hash  (PBKDF2  ×{iterations:,} iterations)")
    info("PBKDF2 = Password-Based Key Derivation Function 2.")
    info(
        f"It takes SHA-256 and runs it {iterations:,} times in a loop,"
    )
    info(
        "feeding each output back in as the next input."
    )
    info(
        "This means a SINGLE password guess costs 600,000× more work."
    )
    info("")
    info(
        "It also mixes in a random SALT — a unique value generated for"
    )
    info(
        "each user — so that the same password never produces the same hash."
    )
    pause("compute the slow hash  (watch the progress bar)")

    salt = os.urandom(16)

    start = time.time()
    h_slow = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, iterations)
    elapsed_slow = time.time() - start

    # Replay the wall-clock delay as a visible progress bar
    progress_bar("Hashing", elapsed_slow, C_GREEN)

    h_slow_hex = binascii.hexlify(h_slow).decode()
    salt_hex = binascii.hexlify(salt).decode()

    print(f"    Password : {C_BOLD}{pwd}{C_RESET}")
    print(f"    Salt     : {C_DIM}{salt_hex}{C_RESET}")
    print(f"    Hash     : {C_GREEN}{h_slow_hex}{C_RESET}")
    print(f"    Time     : {C_GREEN}{C_BOLD}{elapsed_slow:.2f} seconds  🐢{C_RESET}")

    # ━━ Comparison Table ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    label("Side-by-Side Comparison")
    ratio = elapsed_slow / max(elapsed_fast, 1e-7)

    col1 = 14   # label column
    col2 = 22   # fast column
    col3 = 22   # slow column

    rows = [
        f"  {'':>{col1}}{'FAST (SHA-256)':>{col2}}  {'SLOW (PBKDF2)':>{col3}}  ",
        f"  {'Speed':>{col1}}{'< 0.001 s':>{col2}}  {f'{elapsed_slow:.2f} s':>{col3}}  ",
        f"  {'Iterations':>{col1}}{'1':>{col2}}  {f'{iterations:,}':>{col3}}  ",
        f"  {'Has Salt':>{col1}}{'No':>{col2}}  {'Yes':>{col3}}  ",
        f"  {'Attacker cost':>{col1}}{'Trivial':>{col2}}  {'Enormous':>{col3}}  ",
        f"  {'Good for':>{col1}}{'Files / data':>{col2}}  {'Passwords':>{col3}}  ",
    ]
    draw_box(rows)

    # ── Takeaway ────────────────────────────────────────────────────
    years = elapsed_slow * 1e9 / 3.154e7   # 1 billion guesses at this rate
    takeaway(f"""
        The slow hash took {elapsed_slow:.2f} seconds — roughly {ratio:,.0f}× slower
        than a single SHA-256.

        Why does that matter?  Arithmetic:
          • If one guess takes {elapsed_slow:.2f}s, then one BILLION guesses
            would take approximately {years:,.0f} years.
          • Meanwhile, one billion SHA-256 guesses take about 0.1 seconds
            on a modern GPU.

        This deliberate slowness is the ENTIRE defense.  It does not
        make passwords impossible to crack, but it makes the cost so
        high that attackers move on to easier targets.

        Production-grade alternatives to PBKDF2 include bcrypt, scrypt,
        and Argon2.  These go even further: they also require lots of
        MEMORY to compute each guess, so attackers cannot simply buy
        more GPUs to speed things up.  This is called
        "memory-hardness" — it is like adding a toll booth AND a
        traffic jam to the attacker’s highway.
    """)
    pause("return to menu")
