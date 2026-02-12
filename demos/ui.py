"""
demos/ui.py — Shared visual formatting for the Hashing Concepts Lab.

Provides ANSI color constants, Unicode box-drawing helpers, and a small
library of output functions that enforce a consistent look across every
demo module.  Every function indents its output so the presenter's terminal
stays readable on a projector.

No external dependencies — only the Python standard library.
"""

import os
import sys
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ANSI COLOR CODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# These escape sequences work in every modern terminal emulator (macOS
# Terminal, iTerm, GNOME Terminal, Windows Terminal, VS Code integrated
# terminal, etc.).  They switch the foreground color or text style until
# C_RESET is printed.

C_PURPLE = "\033[95m"
C_BLUE   = "\033[94m"
C_CYAN   = "\033[96m"
C_GREEN  = "\033[92m"
C_YELLOW = "\033[93m"
C_RED    = "\033[91m"
C_BOLD   = "\033[1m"
C_DIM    = "\033[2m"
C_RESET  = "\033[0m"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  UNICODE BOX-DRAWING CHARACTERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Used to draw table borders, bucket visualizations, and comparison grids.
# These are standard Unicode codepoints and render correctly in any font
# that ships with a modern OS.

BOX_H  = "─"   # horizontal line
BOX_V  = "│"   # vertical line
BOX_TL = "┌"   # top-left corner
BOX_TR = "┐"   # top-right corner
BOX_BL = "└"   # bottom-left corner
BOX_BR = "┘"   # bottom-right corner
BOX_LT = "├"   # left tee (row separator)
BOX_RT = "┤"   # right tee (row separator)
ARROW  = "→"   # right arrow


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SCREEN / NAVIGATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def clear():
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def pause(label="continue"):
    """
    Print a dim prompt and block until the presenter presses Enter.

    These pause points are the primary pacing mechanism for live
    presentations.  The presenter can talk, answer questions, or point
    at the screen before advancing.
    """
    input(f"\n  {C_DIM}↵  Press Enter to {label}...{C_RESET}")


def prompt(text):
    """
    Ask the user / audience for input and return their response.

    The yellow color draws attention on a projector and makes it obvious
    that the program is waiting for someone to type.
    """
    return input(f"  {C_YELLOW}▸ {text}: {C_RESET}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STRUCTURED OUTPUT — the three-part teaching pattern
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def header(title):
    """
    Clear the screen and print a prominent module header.

    Called once at the top of every demo (and again when the screen
    redraws, e.g. after adding a new bucket entry).
    """
    clear()
    width = max(len(title) + 6, 48)
    print(f"\n{C_PURPLE}{C_BOLD}  {'━' * width}")
    print(f"  ┃  {title.upper()}")
    print(f"  {'━' * width}{C_RESET}\n")


def setup_text(text):
    """
    Print the "What we are about to see" explanation block.

    This is the FIRST part of the three-part teaching pattern.  It sets
    the audience's expectation before anything executes.  Keep the
    language plain — no jargon unless you define it in the same sentence.
    """
    print(f"  {C_CYAN}{C_BOLD}▸ What we are about to see{C_RESET}")
    for line in text.strip().split("\n"):
        print(f"    {C_CYAN}{line.strip()}{C_RESET}")
    print()


def takeaway(text):
    """
    Print the "What this means" conclusion block.

    This is the THIRD part of the three-part teaching pattern.  It
    reinforces the lesson after the audience has observed the behavior.
    """
    print(f"\n  {C_GREEN}{C_BOLD}✓ What this means{C_RESET}")
    for line in text.strip().split("\n"):
        print(f"    {C_GREEN}{line.strip()}{C_RESET}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  INLINE TEXT HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def label(text):
    """Print a bold step heading inside a demo (e.g. 'Step 2 — Modulo')."""
    print(f"\n  {C_BOLD}{text}{C_RESET}")


def info(text):
    """Print a dim supporting detail line."""
    print(f"    {C_DIM}{text}{C_RESET}")


def warn(text):
    """Print a yellow caution / attention line."""
    print(f"    {C_YELLOW}{text}{C_RESET}")


def good(text):
    """Print a green positive-outcome line."""
    print(f"    {C_GREEN}{text}{C_RESET}")


def bad(text):
    """Print a red negative-outcome / danger line."""
    print(f"    {C_RED}{text}{C_RESET}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BOX-DRAWING UTILITIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def strip_ansi(text):
    """
    Return the visible length of *text* after removing ANSI escape codes.

    We need this so that .ljust() / .rjust() pad correctly even when the
    string contains color sequences (which are invisible but count toward
    len()).
    """
    import re
    return re.sub(r"\033\[[0-9;]*m", "", text)


def draw_box(content_lines, width=None, color=C_CYAN):
    """
    Draw a Unicode single-line box around a list of already-formatted
    strings.

    Each line is padded to fill the box width.  If *width* is None, the
    box auto-sizes to the widest visible line.

    Example output:

        ┌──────────────────────────────────────┐
        │  FAST (SHA-256)       SLOW (PBKDF2)  │
        │  < 0.001 s            0.42 s         │
        └──────────────────────────────────────┘
    """
    if width is None:
        width = max(len(strip_ansi(line)) for line in content_lines) + 2

    print(f"    {color}{BOX_TL}{BOX_H * width}{BOX_TR}{C_RESET}")
    for line in content_lines:
        visible_len = len(strip_ansi(line))
        padding = width - visible_len
        print(f"    {color}{BOX_V}{C_RESET}{line}{' ' * padding}{color}{BOX_V}{C_RESET}")
    print(f"    {color}{BOX_BL}{BOX_H * width}{BOX_BR}{C_RESET}")


def draw_buckets(buckets, highlight_idx=None):
    """
    Render a bucket array as a Unicode table.

    Each row shows a bucket index on the left and its contents (or
    "empty") on the right.  Rows are separated by horizontal rules.

        ┌─────┬────────────────────────────────────────────┐
        │  0  │ Cat, Act                                   │
        ├─────┼────────────────────────────────────────────┤
        │  1  │ empty                                      │
        └─────┴────────────────────────────────────────────┘

    If *highlight_idx* is set, that row's index number is colored green
    (placement) or red (collision).
    """
    num = len(buckets)
    idx_w = 5          # width of the index column (including padding)
    content_w = 44     # width of the content column

    # Top border
    print(f"    {C_CYAN}{BOX_TL}{BOX_H * idx_w}┬{BOX_H * content_w}{BOX_TR}{C_RESET}")

    for i in range(num):
        # Index cell — pick color based on highlight state
        if i == highlight_idx and buckets[i]:
            idx_color = C_RED      # collision
        elif i == highlight_idx:
            idx_color = C_GREEN    # clean placement
        else:
            idx_color = C_CYAN     # default

        idx_str = f"{idx_color}{C_BOLD}{i:^{idx_w}}{C_RESET}"

        # Content cell
        if buckets[i]:
            items_str = ", ".join(buckets[i])
        else:
            items_str = f"{C_DIM}empty{C_RESET}"

        # Pad content to fill the column (account for invisible ANSI)
        visible_len = len(strip_ansi(items_str))
        pad = content_w - visible_len - 1  # -1 for leading space
        content_cell = f" {items_str}{' ' * max(pad, 0)}"

        print(f"    {C_CYAN}{BOX_V}{C_RESET}{idx_str}{C_CYAN}{BOX_V}{C_RESET}{content_cell}{C_CYAN}{BOX_V}{C_RESET}")

        # Row separator (not after the last row)
        if i < num - 1:
            print(f"    {C_CYAN}{BOX_LT}{BOX_H * idx_w}┼{BOX_H * content_w}{BOX_RT}{C_RESET}")

    # Bottom border
    print(f"    {C_CYAN}{BOX_BL}{BOX_H * idx_w}┴{BOX_H * content_w}{BOX_BR}{C_RESET}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PROGRESS BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def progress_bar(label_text, seconds, color=C_GREEN):
    """
    Display a live-filling progress bar over *seconds* duration.

    Used in the password-hashing demo to make the audience FEEL how
    long the slow hash takes.  The bar redraws on the same line using
    a carriage return.
    """
    width = 30
    start = time.time()
    while True:
        elapsed = time.time() - start
        pct = min(elapsed / seconds, 1.0)
        filled = int(width * pct)
        bar = "█" * filled + "░" * (width - filled)
        sys.stdout.write(
            f"\r    {color}{label_text} [{bar}] {pct * 100:3.0f}%{C_RESET}"
        )
        sys.stdout.flush()
        if pct >= 1.0:
            break
        time.sleep(0.05)
    print()  # move to next line after bar completes


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SHARED HASH HELPER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def toy_hash(text, num_buckets):
    """
    A trivially simple "hash function" used in Demos 1 and 2.

    Algorithm: sum every character's ASCII code, then take the remainder
    when dividing by num_buckets.

        toy_hash("Cat", 8)
        → (67 + 97 + 116) = 280
        → 280 % 8 = 0
    """
    return sum(ord(c) for c in text) % num_buckets
