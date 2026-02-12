# Hashing Concepts Lab

An interactive, presenter-driven teaching tool for live cybersecurity demonstrations. Every demo follows a consistent three-part pattern — **setup → visual demonstration → takeaway** — designed so the presenter can narrate each concept in real time while the audience discovers behaviors through interaction.

## Quick Start

```bash
python3 hashing_lab.py
```

No external libraries needed — Python 3.6+ standard library only.

## Project Structure

```
hashing-demo/
├── hashing_lab.py           # Entry point — banner + main menu
└── demos/
    ├── __init__.py
    ├── ui.py                # Shared colors, box-drawing, formatting
    ├── toy_hash.py          # Demo 1: Toy hash mapping
    ├── collisions.py        # Demo 2: Collision challenge
    ├── avalanche.py         # Demo 3: Avalanche effect
    ├── password.py          # Demo 4: Fast vs. slow password hashing
    └── rainbow.py           # Demo 5: Rainbow table attack & salt defense
```

Each demo is a self-contained module with a single `run()` function.  Adding a new demo is as simple as creating a file with `run()` and registering it in `hashing_lab.py`.

## Demo Modules

Each module builds on the previous one, forming a coherent narrative arc.

| # | Module | Concept | Key Vocabulary |
|---|--------|---------|----------------|
| 1 | **Toy Hash Mapping** | How text maps to numbered buckets via ASCII sum + modulo | Hash function, Bucket, Collision |
| 2 | **Collision Challenge** | Why collisions are mathematically inevitable | Pigeonhole Principle, Collision resistance |
| 3 | **Avalanche Effect** | One character change flips ~50% of output bits (hex + binary diff) | Avalanche Effect, SHA-256, Bit |
| 4 | **Password Hashing** | Feel the speed difference: fast SHA-256 vs. slow PBKDF2 in real time | Brute-force, PBKDF2, Key stretching, Salt |
| 5 | **Rainbow Table Attack** | Crack an unsalted hash instantly, then see salt defeat the attack | Rainbow table, Salt, Pre-image attack |

## Presenter Tips

- **Terminal setup**: Use a large font (18pt+) on a dark background for projector visibility.
- **Pacing**: Every demo pauses with "Press Enter to..." prompts — use these moments to elaborate verbally, ask questions, or take audience input.
- **Audience interaction**: Ask the room for words/passwords to type in. Discovery beats lecture.
- **Recommended order**: 1 → 2 → 3 → 4 → 5 (each demo references concepts from the one before).
- **Modifying live**: Each demo module is small and self-contained with clear function names — easy to open and edit on a projector if you want to show the code.
