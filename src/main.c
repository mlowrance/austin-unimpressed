#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include "vga.h"

/* Assets */
#include "assets/palette.h"
#include "assets/AUSTIN_N.H"
#include "assets/austin_unimpressed.h"
#include "assets/austin_awooga.h"
#include "assets/retirement_bar.h"

typedef enum {
    STATE_TITLE,
    STATE_WALKING,
    STATE_UNIMPRESSED,
    STATE_END
} GameState;

typedef struct {
    int x, y;
    int width, height;
    unsigned char *sprite;
} Actor;

/* Non-blocking key codes */
#define KEY_ESC   27
#define KEY_SPACE 32
#define KEY_RIGHT 77

/* Game constants */
#define RETIREMENT_GOAL 3
#define BOSS_X_TRIGGER 200

int main(void) {
    GameState current_state = STATE_TITLE;
    int running = 1;
    int retirement_count = 0;
    
    Actor austin;
    austin.x = 20;
    austin.y = 100;
    austin.width = AUSTIN_N_WIDTH;
    austin.height = AUSTIN_N_HEIGHT;
    austin.sprite = austin_n;

    printf("Austin Unimpressed - Phase 4\n");
    printf("SPACE: Start/Continue, RIGHT: Walk, ESC: Quit\n");
    getch();

    if (!init_vga_buffer()) {
        printf("Buffer failed!\n");
        return 1;
    }

    set_video_mode(MODE_VGA_13H);
    set_palette(austin_palette);

    while (running) {
        /* 1. Input */
        if (kbhit()) {
            int key = getch();
            if (key == 0) { /* Extended key */
                key = getch();
                if (key == KEY_RIGHT && current_state == STATE_WALKING) {
                    austin.x += 5;
                }
            } else if (key == KEY_ESC) {
                running = 0;
            } else if (key == KEY_SPACE) {
                if (current_state == STATE_TITLE) {
                    current_state = STATE_WALKING;
                } else if (current_state == STATE_UNIMPRESSED) {
                    current_state = STATE_WALKING;
                    retirement_count++;
                    austin.x = 20;
                    if (retirement_count >= RETIREMENT_GOAL) {
                        current_state = STATE_END;
                    }
                }
            }
        }

        /* 2. Logic */
        if (current_state == STATE_WALKING) {
            if (austin.x >= BOSS_X_TRIGGER) {
                current_state = STATE_UNIMPRESSED;
            }
        }

        /* 3. Rendering */
        clear_vga_buffer(0);

        /* Always draw UI if not in Title/End */
        if (current_state == STATE_WALKING || current_state == STATE_UNIMPRESSED) {
            /* Draw retirement bar background */
            draw_sprite(110, 10, RETIREMENT_BAR_WIDTH, RETIREMENT_BAR_HEIGHT, retirement_bar);
            
            /* Fill retirement bar based on progress */
            {
                int i;
                int fill_w = (retirement_count * (RETIREMENT_BAR_WIDTH - 2)) / RETIREMENT_GOAL;
                for (i = 0; i < fill_w; i++) {
                    int iy;
                    for (iy = 0; iy < 10; iy++) {
                        put_pixel(111 + i, 15 + iy, 10); /* Green fill inside bar */
                    }
                }
            }
        }

        switch (current_state) {
            case STATE_TITLE:
                /* Draw normal austin as title placeholder */
                draw_sprite(144, 68, AUSTIN_N_WIDTH, AUSTIN_N_HEIGHT, austin_n);
                break;

            case STATE_WALKING:
                draw_sprite(austin.x, austin.y, austin.width, austin.height, austin.sprite);
                break;

            case STATE_UNIMPRESSED:
                /* Switch to unimpressed sprite */
                draw_sprite(austin.x, austin.y, AUSTIN_UNIMPRESSED_WIDTH, AUSTIN_UNIMPRESSED_HEIGHT, austin_unimpressed);
                break;

            case STATE_END:
                /* Draw Awooga for end state */
                draw_sprite(144, 68, AUSTIN_AWOOGA_WIDTH, AUSTIN_AWOOGA_HEIGHT, austin_awooga);
                break;
        }

        wait_for_vsync();
        flip_vga_buffer();
    }

    exit_video_mode();
    free_vga_buffer();
    return 0;
}
