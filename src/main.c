#include <stdio.h>
#include <conio.h>
#include "vga.h"

int main(void) {
    printf("Initializing VGA Mode 13h...\n");
    printf("Press any key to start.\n");
    getch();

    set_video_mode(MODE_VGA_13H);

    /* Draw a simple test pattern: a few pixels */
    put_pixel(160, 100, 15); /* White pixel in the center */
    put_pixel(0, 0, 10);      /* Green pixel at top-left */
    put_pixel(319, 199, 12);  /* Red pixel at bottom-right */

    /* Wait for a key press before exiting */
    getch();

    exit_video_mode();
    printf("Returned to text mode. Exiting.\n");

    return 0;
}
