# Austin Unimpressed - Development Plan

This document serves as the roadmap for the Gemini CLI and development team.

## Phase 1: Boilerplate & VGA Initialization
- [ ] **Task 1.1:** Create `src/main.c` with a basic DOS entry point.
- [ ] **Task 1.2:** Implement `set_video_mode(unsigned char mode)` to switch to `0x13` (VGA 320x200).
- [ ] **Task 1.3:** Implement `exit_video_mode()` to return to text mode (0x03) on program exit.
- [ ] **Task 1.4:** Create a `put_pixel(int x, int y, unsigned char color)` function.

## Phase 2: Double Buffering & Graphics Engine
- [ ] **Task 2.1:** Allocate a 64,000-byte buffer (`unsigned char *screen_buffer`) for double buffering.
- [ ] **Task 2.2:** Implement a `flip_buffer()` function using `memcpy` to copy the buffer to video memory at `0xA0000`.
- [ ] **Task 2.3:** Implement a basic sprite drawing function that supports transparency (skip drawing for color 0).
- [ ] **Task 2.4:** Implement a `clear_buffer()` function to reset the frame.

## Phase 3: State Machine & Input
- [ ] **Task 3.1:** Setup a game loop with a state machine: `STATE_TITLE`, `STATE_WALKING`, `STATE_UNIMPRESSED`, `STATE_END`.
- [ ] **Task 3.2:** Implement non-blocking keyboard input for Space Bar (continue) and Right Arrow (walk).
- [ ] **Task 3.3:** Create a basic timer or delay function to control frame rate on real hardware.

## Phase 4: Gameplay & UI
- [ ] **Task 4.1:** Define an `Actor` struct to track Austin's X/Y position and current animation frame.
- [ ] **Task 4.2:** Implement the "Retirement Bar" UI at the top of the screen (fills in $1/3$ increments).
- [ ] **Task 4.3:** Set Boss Encounter triggers at specific X-coordinates.
- [ ] **Task 4.4:** Implement the "Speech Bubble" logic for the "Unimpressed" state.

## Phase 5: Asset Integration & End Game
- [ ] **Task 5.1:** Integrate header-based sprite data for Austin (Normal, Unimpressed, and Awooga states).
- [ ] **Task 5.2:** Integrate Boss sprites (Chicken Strips, Massive PR, TBD).
- [ ] **Task 5.3:** Code the "End Game" sequence: Retirement money appears -> House falls from sky -> Game Over.