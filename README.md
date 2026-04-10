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
├── assets/         # Sprite headers and palette data
├── tools/          # Scripts for asset conversion and sprite processing
├── plans/          # Development roadmap and planning notes
├── .github/        # GitHub metadata and project guidance
├── bin/            # Compiled `.EXE` output (git ignored)
├── Makefile        # Build and run targets
├── DEVELOPMENT.md  # Build/environment instructions
├── GEMINI.md       # AI agent and project guidance
├── README.md       # Project overview and docs
└── .gitignore      # Build artifact exclusion