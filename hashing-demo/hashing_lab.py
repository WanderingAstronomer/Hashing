#!/usr/bin/env python3
"""
hashing_lab.py — Interactive Hashing Concepts Lab
Cybersecurity SIG

Entry point and main menu for the lab.  Each demo lives in its own
module under the `demos/` package.  Run this file to start:

    python3 hashing_lab.py

No external dependencies — standard library only.
"""

import time

from demos.ui import (
    clear, pause, prompt, warn,
    C_BOLD, C_CYAN, C_DIM, C_GREEN, C_RESET,
)
from demos import toy_hash, collisions, avalanche, password, rainbow

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def banner():
    """Print the lab title banner."""
    print(f"{C_CYAN}{C_BOLD}")
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║                                               ║")
    print("  ║        HASHING  CONCEPTS  LAB                 ║")
    print("  ║        Interactive Teaching Demo               ║")
    print("  ║                                               ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print(f"{C_RESET}")
    print(f"  {C_DIM}Cybersecurity SIG  —  Guided Discovery Mode{C_RESET}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DEMO REGISTRY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Each entry is (title, one-line description, callable).
# Adding a new demo is as simple as creating a module with a run()
# function and adding a line here.

DEMOS = [
    (
        "Toy Hash Mapping",
        "See how text maps to numbered buckets — and discover collisions",
        toy_hash.run,
    ),
    (
        "Collision Challenge",
        "Try to force two words into the same bucket — and learn why it always works",
        collisions.run,
    ),
    (
        "Avalanche Effect",
        "Change one character and watch the entire output scramble",
        avalanche.run,
    ),
    (
        "Password Hashing",
        "See why websites don't store your actual password",
        password.run,
    ),
    (
        "Rainbow Table Attack",
        "Crack a stolen password instantly — then learn the defense",
        rainbow.run,
    ),
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN MENU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main_menu():
    while True:
        clear()
        banner()

        # Narrative arc hint
        print(
            f"  {C_DIM}Each demo builds on the last.  "
            f"Recommended order: 1 → 5{C_RESET}\n"
        )

        for i, (title, subtitle, _) in enumerate(DEMOS, 1):
            print(f"    {C_BOLD}{i}{C_RESET}.  {C_CYAN}{title}{C_RESET}")
            print(f"        {C_DIM}{subtitle}{C_RESET}")

        print(f"\n    {C_BOLD}Q{C_RESET}.  Quit\n")

        choice = prompt("Select a demo")

        if choice.lower() == "q":
            clear()
            print(f"\n  {C_GREEN}{C_BOLD}Thanks for attending! 🔐{C_RESET}\n")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(DEMOS):
            _, _, run_fn = DEMOS[int(choice) - 1]
            run_fn()
        else:
            warn("Please enter a number 1–5 or Q.")
            time.sleep(1)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {C_DIM}Interrupted. Goodbye!{C_RESET}\n")
