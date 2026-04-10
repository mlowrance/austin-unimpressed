#include "vga.h"
#include <dos.h>
#include <malloc.h>

/* Pointer to the start of video memory */
unsigned char __far *video_mem = (unsigned char __far *)VGA_VIDEO_MEMORY;

/* Back buffer for double buffering - using far pointer for safety */
unsigned char __far *back_buffer = NULL;

void set_video_mode(unsigned char mode) {
    union REGPACK regs;
    regs.w.ax = mode;
    intr(0x10, &regs);
}

void exit_video_mode(void) {
    set_video_mode(MODE_TEXT);
}

int init_vga_buffer(void) {
    back_buffer = (unsigned char __far *)_fmalloc(VGA_SCREEN_SIZE);
    if (back_buffer == NULL) {
        return 0;
    }
    _fmemset(back_buffer, 0, VGA_SCREEN_SIZE);
    return 1;
}

void free_vga_buffer(void) {
    if (back_buffer != NULL) {
        _ffree(back_buffer);
        back_buffer = NULL;
    }
}

void clear_vga_buffer(unsigned char color) {
    if (back_buffer != NULL) {
        _fmemset(back_buffer, color, VGA_SCREEN_SIZE);
    }
}

void flip_vga_buffer(void) {
    if (back_buffer != NULL) {
        _fmemcpy(video_mem, back_buffer, VGA_SCREEN_SIZE);
    }
}

void put_pixel(int x, int y, unsigned char color) {
    if (back_buffer != NULL && x >= 0 && x < VGA_WIDTH && y >= 0 && y < VGA_HEIGHT) {
        back_buffer[y * (long)VGA_WIDTH + x] = color;
    }
}

void draw_sprite(int x, int y, int width, int height, const unsigned char *sprite_data) {
    int sx, sy;
    if (back_buffer == NULL) return;

    for (sy = 0; sy < height; sy++) {
        int screen_y = y + sy;
        if (screen_y < 0 || screen_y >= VGA_HEIGHT) continue;

        for (sx = 0; sx < width; sx++) {
            int screen_x = x + sx;
            if (screen_x < 0 || screen_x >= VGA_WIDTH) continue;

            {
                unsigned char color = sprite_data[sy * width + sx];
                if (color != 0) {
                    back_buffer[screen_y * (long)VGA_WIDTH + screen_x] = color;
                }
            }
        }
    }
}
