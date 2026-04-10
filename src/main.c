#include <stdio.h>
#include <conio.h>
#include "vga.h"

int main(void) {
    /* 4x4 test sprite (color 0 is transparent) */
    unsigned char test_sprite[] = {
        0, 15, 15, 0,
        15, 10, 10, 15,
        15, 10, 10, 15,
        0, 15, 15, 0
    };

    printf("Initializing VGA Mode 13h with double buffering...\n");
    printf("Press any key to start.\n");
    getch();

    if (!init_vga_buffer()) {
        printf("Failed to allocate back buffer!\n");
        return 1;
    }

    set_video_mode(MODE_VGA_13H);

    /* Draw to the back buffer */
    clear_vga_buffer(0); /* Black background */

    /* Draw a few pixels */
    put_pixel(160, 100, 15); /* White pixel in the center */
    put_pixel(0, 0, 10);      /* Green pixel at top-left */
    put_pixel(319, 199, 12);  /* Red pixel at bottom-right */

    /* Draw the test sprite */
    draw_sprite(160, 110, 4, 4, test_sprite);

    /* Copy back buffer to video memory */
    flip_vga_buffer();

    /* Wait for a key press */
    getch();

    exit_video_mode();
    free_vga_buffer();

    printf("Returned to text mode. Exiting.\n");

    return 0;
}
