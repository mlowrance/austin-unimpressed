# Austin Unimpressed (DOS)

An interactive "walking simulator" for vintage DOS hardware.

## The Premise
Austin is on a quest for retirement. To get there, he must walk through a series of corporate and life hurdles, remaining completely unimpressed by everything he encounters.

## Technical Specs
- **Platform:** MS-DOS
- **Graphics:** VGA Mode 13h (320x200, 256 colors)
- **Language:** C (Open Watcom v2)
- **Architecture:** 16-bit Real Mode (Targeting 386/486 hardware)

## Controls
- **Space Bar:** Start Game / Continue
- **Right Arrow:** Walk toward retirement


## Source Structure

.
├── src/            # C source files (*.c)
├── include/        # Header files (*.h)
├── assets/         # Sprite data converted to C headers
├── tools/          # Scripts for asset conversion
├── bin/            # Compiled .EXE output (git ignored)
├── PLAN.md         # Task tracking for Gemini CLI
├── DEVELOPMENT.md  # Build and environment instructions
└── .gitignore      # Build artifact exclusion