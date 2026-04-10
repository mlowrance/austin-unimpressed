#ifndef VGA_H
#define VGA_H

#include <i86.h>

/* VGA Mode 13h constants */
#define VGA_WIDTH 320
#define VGA_HEIGHT 200
#define VGA_SCREEN_SIZE (VGA_WIDTH * VGA_HEIGHT)
#define VGA_VIDEO_MEMORY MK_FP(0xA000, 0)

/* Video modes */
#define MODE_TEXT 0x03
#define MODE_VGA_13H 0x13

void set_video_mode(unsigned char mode);
void exit_video_mode(void);
void put_pixel(int x, int y, unsigned char color);

#endif
