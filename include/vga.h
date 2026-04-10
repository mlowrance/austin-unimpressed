#ifndef VGA_H
#define VGA_H

#include <i86.h>
#include <string.h>
#include <stdlib.h>

/* VGA Mode 13h constants */
#define VGA_WIDTH 320
#define VGA_HEIGHT 200
#define VGA_SCREEN_SIZE (VGA_WIDTH * VGA_HEIGHT)
#define VGA_VIDEO_MEMORY MK_FP(0xA000, 0)

/* Video modes */
#define MODE_TEXT 0x03
#define MODE_VGA_13H 0x13

/* Buffer management */
int init_vga_buffer(void);
void free_vga_buffer(void);
void clear_vga_buffer(unsigned char color);
void flip_vga_buffer(void);
void wait_for_vsync(void);

/* Drawing functions */
void set_video_mode(unsigned char mode);
void exit_video_mode(void);
void set_palette(const unsigned char *palette_data);
void put_pixel(int x, int y, unsigned char color);
void draw_sprite(int x, int y, int width, int height, const unsigned char *sprite_data);

#endif
