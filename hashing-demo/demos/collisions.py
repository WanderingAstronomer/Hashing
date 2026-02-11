"""
demos/collisions.py — Demo 2: Collision Challenge

An interactive game that turns a theoretical concept into a hands-on
discovery: collisions are INEVITABLE when you map infinite inputs into
a finite number of buckets.

The audience is challenged to intentionally cause a collision using
only 5 buckets.  With that few slots, the Pigeonhole Principle
guarantees a collision by the 6th entry at the latest — but it usually
happens much sooner, which surprises people.

Narrative position
──────────────────
This is the SECOND demo.  It deepens the understanding from Demo 1:

    Demo 1 said: "Collisions can happen."
    Demo 2 says: "Collisions MUST happen, and here is why."

Key vocabulary introduced here:
  • Pigeonhole Principle — if you have more items than containers,
    at least one container must hold more than one item.
  • Collision resistance — the property of a hash function that makes
    collisions hard to *find*, even though they exist in theory.
    Cryptographic hash functions like SHA-256 have 2²⁵⁶ possible
    outputs, making intentional collisions effectively impossible.
"""

from demos.ui import (
    header, setup_text, takeaway, label, info, good, bad,
    pause, prompt, draw_buckets, toy_hash,
    C_BOLD, C_DIM, C_RESET,
)

NUM_BUCKETS = 5  # deliberately small to make collisions very likely


def run():
    """Entry point — called from the main menu."""

    header("Demo 2 — Collision Challenge")
    setup_text("""
        In Demo 1 we saw that collisions CAN happen.
        Now we will prove that collisions MUST happen.

        This is because of the Pigeonhole Principle — a simple but
        powerful idea from mathematics:

            "If you have more pigeons than pigeonholes,
             at least one hole must contain more than one pigeon."

        We have only 5 buckets this time.  Your challenge is to
        cause a collision — type words until two of them land in
        the same bucket.

        Hint: with 5 buckets, a collision is GUARANTEED by word #6.
        Why?  Once you have entered 5 words, every bucket could be
        occupied.  The 6th word MUST land in an already-occupied
        bucket because there is simply nowhere new for it to go!
        In practice it usually happens even sooner.
    """)
    pause("start the challenge")

    buckets = [[] for _ in range(NUM_BUCKETS)]
    attempts = 0
    found = False

    while not found:
        header("Demo 2 — Collision Challenge")
        print(f"    {C_DIM}Buckets: {NUM_BUCKETS}   │   Words entered: {attempts}{C_RESET}\n")
        draw_buckets(buckets)

        print()
        word = prompt("Enter a word  (q = back to menu)")
        if word.lower() == "q" or word == "":
            break

        idx = toy_hash(word, NUM_BUCKETS)
        attempts += 1

        ascii_sum = sum(ord(c) for c in word)
        print(
            f"\n    hash('{word}') = {ascii_sum} mod {NUM_BUCKETS} "
            f"= {C_BOLD}{idx}{C_RESET}"
        )

        if buckets[idx]:
            # ── Collision detected ──
            found = True
            bad(
                f"COLLISION in bucket {idx}!  "
                f"'{word}' crashed into {buckets[idx]}"
            )
            buckets[idx].append(word)
            print()
            draw_buckets(buckets, highlight_idx=idx)

            takeaway(f"""
                It took {attempts} word(s) to produce a collision in {NUM_BUCKETS} buckets.

                Why was it so fast?
                The Pigeonhole Principle guarantees that after {NUM_BUCKETS + 1} entries, at
                least two MUST share a bucket — there are simply not enough
                slots for everyone to have their own.

                In fact, randomness makes collisions appear even sooner than
                you might expect.  This is related to the "Birthday Paradox":
                in a group of just 23 people, there is a 50% chance that two
                of them share the same birthday.  The same math applies to
                hash functions — as you add inputs, the chance of two outputs
                matching grows surprisingly fast.

                Our toy hash only has {NUM_BUCKETS} buckets, so collisions are trivial.
                Real-world hash functions use enormous output spaces to make
                collisions practically impossible to find.  For example,
                SHA-256 ("Secure Hash Algorithm, 256-bit") — which we will
                explore in Demo 3 — has 2²⁵⁶ possible outputs.  That is more
                combinations than there are atoms in the observable universe.

                Even though collisions still EXIST in theory, nobody has ever
                found two inputs with the same SHA-256 result.  We call that
                property COLLISION RESISTANCE.
            """)
            pause("return to menu")
        else:
            good(f"No collision yet. '{word}' placed in bucket {idx}.")
            buckets[idx].append(word)
            pause("try again")
