"""
demos/toy_hash.py — Demo 1: Toy Hash Mapping

Teaches the fundamental idea behind every hash function: turning
arbitrary text into a small, fixed-size number.

The audience types words and watches them land in numbered "buckets"
drawn with Unicode box art.  Collisions emerge naturally when two
different words map to the same bucket — the program highlights them
in red and explains what happened.

Narrative position
──────────────────
This is the FIRST demo in the lab.  It establishes the mental model
that all later demos build on:

    input  →  deterministic math  →  fixed-size number (the hash)

Key vocabulary introduced here:
  • Hash function — a repeatable formula that converts any input to a
    fixed-size output.
  • Bucket — a storage slot identified by the hash value.
  • Collision — when two different inputs produce the same hash.
"""

from demos.ui import (
    header, setup_text, takeaway, label, info, good, bad,
    pause, prompt, draw_buckets, toy_hash,
    C_BOLD, C_CYAN, C_GREEN, C_RED, C_RESET,
)

NUM_BUCKETS = 8


def run():
    """Entry point — called from the main menu."""
    buckets = [[] for _ in range(NUM_BUCKETS)]

    # ── Setup: explain what is about to happen ──────────────────────
    header("Demo 1 — Toy Hash Mapping")
    setup_text("""
        A hash function is a formula that takes ANY input — a word, a
        file, an entire novel — and converts it into a fixed-size
        number.  The same input ALWAYS produces the same number.

        Why is this useful?  Imagine a library with millions of books.
        Instead of searching every shelf, the librarian uses a formula
        to calculate exactly which shelf a book belongs on.  That is
        what a hash function does — it turns data into an address.

        Our toy formula works like this:
          1. Convert each letter to its ASCII number.
             ASCII is a universal numbering system for characters —
             every computer in the world agrees that 'A' = 65,
             'B' = 66, 'a' = 97, 'b' = 98, and so on.
          2. Add all the numbers together.
          3. Divide by the number of slots and keep only the
             remainder (the “modulo” operation).

        We call each slot a BUCKET — a numbered storage container
        where we place items based on their hash value.
        Type words and watch which bucket they land in!
    """)
    pause("start the demo")

    # ── Interactive loop ────────────────────────────────────────────
    while True:
        header("Demo 1 — Toy Hash Mapping")
        draw_buckets(buckets)

        print()
        word = prompt("Type a word to hash  (q = back to menu)")
        if word.lower() == "q" or word == "":
            break

        # Step 1 — ASCII conversion
        label("Step 1 — Convert each letter to its ASCII number")
        info(
            "ASCII is a universal lookup table that assigns a number"
        )
        info(
            "to every character.  'A' = 65, 'a' = 97, '0' = 48, etc."
        )
        parts = []
        total = 0
        for ch in word:
            v = ord(ch)
            total += v
            parts.append(f"'{ch}'={v}")
        print(f"    {' + '.join(parts)}")
        print(f"    Sum = {C_BOLD}{total}{C_RESET}")

        # Step 2 — Modulo
        idx = total % NUM_BUCKETS
        label(f"Step 2 — Modulo  (fit into {NUM_BUCKETS} buckets)")
        info(
            "The modulo operator (%) divides and keeps only the remainder."
        )
        info(
            f"It guarantees the result is always between 0 and {NUM_BUCKETS - 1}."
        )
        print(f"    {total} % {NUM_BUCKETS} = {C_BOLD}{C_CYAN}{idx}{C_RESET}")

        # Step 3 — Place the word
        collision = len(buckets[idx]) > 0
        if collision:
            label("Result — Collision!")
            bad(
                f"Bucket {idx} already contains: {buckets[idx]}"
            )
            info(
                f"'{word}' maps to the SAME bucket.  This is called a COLLISION."
            )
            info(
                "Both words will share the bucket.  Collisions are not errors —"
            )
            info(
                "they are a normal consequence of squeezing infinite inputs"
            )
            info(
                "into a limited number of slots.  We will explore this in Demo 2."
            )
        else:
            label("Result")
            good(f"Bucket {idx} is empty — placing '{word}' there now.")

        buckets[idx].append(word)
        pause("hash another word")

    # ── Takeaway ────────────────────────────────────────────────────
    takeaway("""
        A hash function always gives the same output for the same input.
        That makes it perfect for organizing and finding data quickly —
        just like our librarian calculating exactly which shelf to check
        instead of searching every book in the building.

        When two DIFFERENT inputs produce the same output, we call that a
        COLLISION.  Collisions are unavoidable because we are squeezing
        infinite possible inputs into a limited number of buckets.

        In the real world, this same idea powers everything from the way
        your computer quickly finds files, to how websites verify that a
        download was not corrupted.  The next demos will show how hashing
        also plays a critical role in security.
    """)
    pause("return to menu")
