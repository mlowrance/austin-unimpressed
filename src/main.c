#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include "vga.h"

typedef enum {
    STATE_TITLE,
    STATE_WALKING,
    STATE_UNIMPRESSED,
    STATE_END
} GameState;

/* Non-blocking key codes */
#define KEY_ESC   27
#define KEY_SPACE 32
#define KEY_RIGHT 77

/* Helper to draw a solid block */
void draw_rect(int x, int y, int w, int h, unsigned char color) {
    int ix, iy;
    for (iy = 0; iy < h; iy++) {
        for (ix = 0; ix < w; ix++) {
            put_pixel(x + ix, y + iy, color);
        }
    }
}

int main(void) {
    GameState current_state = STATE_TITLE;
    int running = 1;
    int austin_x = 20;
    int austin_y = 100;

    unsigned char test_sprite[] = {
        0, 15, 15, 0,
        15, 10, 10, 15,
        15, 10, 10, 15,
        0, 15, 15, 0
    };

    printf("Austin Unimpressed - Debug Build\n");
    printf("SPACE: Start/Continue, RIGHT: Walk, ESC: Quit\n");
    printf("Initializing...\n");
    getch();

    if (!init_vga_buffer()) {
        printf("Buffer failed!\n");
        return 1;
    }

    set_video_mode(MODE_VGA_13H);

    while (running) {
        if (kbhit()) {
            int key = getch();
            if (key == 0) { /* Extended key prefix */
                key = getch();
                if (key == KEY_RIGHT && current_state == STATE_WALKING) {
                    austin_x += 10;
                }
            } else if (key == KEY_ESC) {
                running = 0;
            } else if (key == KEY_SPACE) {
                if (current_state == STATE_TITLE) {
                    current_state = STATE_WALKING;
                } else if (current_state == STATE_UNIMPRESSED) {
                    current_state = STATE_WALKING;
                    austin_x = 20; /* Reset position */
                }
            }
        }

        if (current_state == STATE_WALKING) {
            if (austin_x > 280) {
                current_state = STATE_UNIMPRESSED;
            }
        }

        /* Clear to a dark blue background to show the buffer is active */
        clear_vga_buffer(1); 

        switch (current_state) {
            case STATE_TITLE:
                /* Big Yellow Box for Title */
                draw_rect(110, 80, 100, 40, 14);
                break;

            case STATE_WALKING:
                /* Draw a "ground" line */
                draw_rect(0, 120, 320, 2, 7);
                draw_sprite(austin_x, austin_y, 4, 4, test_sprite);
                break;

            case STATE_UNIMPRESSED:
                /* Big Red Box for Unimpressed */
                draw_rect(110, 80, 100, 40, 12);
                break;

            case STATE_END:
                break;
        }

        wait_for_vsync();
        flip_vga_buffer();
    }

    exit_video_mode();
    free_vga_buffer();
    return 0;
}
