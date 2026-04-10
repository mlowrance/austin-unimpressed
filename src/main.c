#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include "vga.h"

/* Assets */
#include "assets/palette.h"
#include "assets/A_NORM.H"
#include "assets/austin_unimpressed.h"
#include "assets/austin_awooga.h"
#include "assets/retirement_bar.h"
#include "assets/boss_chicken.h"
#include "assets/boss_pr.h"
#include "assets/money.h"
#include "assets/house.h"

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
    austin.y = 50; /* Adjusted for taller sprite */
    austin.width = A_NORM_WIDTH;
    austin.height = A_NORM_HEIGHT;
    austin.sprite = a_norm;

    printf("Austin Unimpressed - Phase 5 Final Prototype\n");
    printf("SPACE: Start/Continue, RIGHT: Walk, ESC: Quit\n");
    getch();

    if (!init_vga_buffer()) {
        printf("Buffer failed!\n");
        return 1;
    }

    set_video_mode(MODE_VGA_13H);
    set_palette(austin_palette);

    while (running) {
        if (kbhit()) {
            int key = getch();
            if (key == 0) {
                key = getch();
                if (key == KEY_RIGHT && current_state == STATE_WALKING) {
                    austin.x += 8;
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
                } else if (current_state == STATE_END) {
                    running = 0; /* Quit after winning */
                }
            }
        }

        if (current_state == STATE_WALKING) {
            if (austin.x >= BOSS_X_TRIGGER) {
                current_state = STATE_UNIMPRESSED;
            }
        }

        clear_vga_buffer(0);

        /* UI Rendering */
        if (current_state == STATE_WALKING || current_state == STATE_UNIMPRESSED) {
            draw_sprite(110, 5, RETIREMENT_BAR_WIDTH, RETIREMENT_BAR_HEIGHT, retirement_bar);
            {
                int i;
                int fill_w = (retirement_count * (RETIREMENT_BAR_WIDTH - 2)) / RETIREMENT_GOAL;
                for (i = 0; i < fill_w; i++) {
                    int iy;
                    for (iy = 0; iy < 10; iy++) {
                        put_pixel(111 + i, 10 + iy, 10);
                    }
                }
            }
        }

        switch (current_state) {
            case STATE_TITLE:
                draw_sprite(128, 40, A_NORM_WIDTH, A_NORM_HEIGHT, a_norm);
                /* Draw some "Logo" pixels */
                put_pixel(160, 20, 14); put_pixel(161, 20, 14);
                break;

            case STATE_WALKING:
                /* Draw Ground */
                {
                    int gx;
                    for (gx = 0; gx < 320; gx++) put_pixel(gx, 164, 7);
                }
                draw_sprite(austin.x, austin.y, austin.width, austin.height, austin.sprite);
                break;

            case STATE_UNIMPRESSED:
                /* Draw Boss based on progress */
                if (retirement_count == 0) {
                    draw_sprite(220, 100, BOSS_CHICKEN_WIDTH, BOSS_CHICKEN_HEIGHT, boss_chicken);
                } else {
                    draw_sprite(220, 100, BOSS_PR_WIDTH, BOSS_PR_HEIGHT, boss_pr);
                }
                
                draw_sprite(austin.x, austin.y, AUSTIN_UNIMPRESSED_WIDTH, AUSTIN_UNIMPRESSED_HEIGHT, austin_unimpressed);
                
                /* Simple Speech Bubble Placeholder */
                {
                    int bx, by;
                    for (by = 80; by < 95; by++) {
                        for (bx = 20; bx < 100; bx++) put_pixel(bx, by, 15);
                    }
                }
                break;

            case STATE_END:
                /* Win sequence: Money and House */
                draw_sprite(100, 130, MONEY_WIDTH, MONEY_HEIGHT, money);
                draw_sprite(180, 130, MONEY_WIDTH, MONEY_HEIGHT, money);
                draw_sprite(128, 40, HOUSE_WIDTH, HOUSE_HEIGHT, house);
                draw_sprite(144, 100, AUSTIN_AWOOGA_WIDTH, AUSTIN_AWOOGA_HEIGHT, austin_awooga);
                break;
        }

        wait_for_vsync();
        flip_vga_buffer();
    }

    exit_video_mode();
    free_vga_buffer();
    return 0;
}
