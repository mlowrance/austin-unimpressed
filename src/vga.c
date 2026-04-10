#include "vga.h"

/* Pointer to the start of video memory */
unsigned char __far *video_mem = (unsigned char __far *)VGA_VIDEO_MEMORY;

void set_video_mode(unsigned char mode) {
    union REGPACK regs;
    regs.w.ax = mode;
    intr(0x10, &regs);
}

void exit_video_mode(void) {
    set_video_mode(MODE_TEXT);
}

void put_pixel(int x, int y, unsigned char color) {
    if (x >= 0 && x < VGA_WIDTH && y >= 0 && y < VGA_HEIGHT) {
        video_mem[y * VGA_WIDTH + x] = color;
    }
}
