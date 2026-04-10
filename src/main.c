#include <stdio.h>
#include <conio.h>
#include "vga.h"

#include "assets/palette.h"
#include "assets/AUSTIN_N.H"
#include "assets/austin_unimpressed.h"
#include "assets/austin_awooga.h"

int main(void) {
    printf("Displaying new Austin sprites for verification...\n");
    printf("Press any key to start.\n");
    getch();

    if (!init_vga_buffer()) {
        printf("Buffer failed!\n");
        return 1;
    }

    set_video_mode(MODE_VGA_13H);
    set_palette(austin_palette);

    clear_vga_buffer(0);

    /* Draw Normal Austin (Left) - using new AUSTIN_N.H */
    draw_sprite(40, 68, AUSTIN_N_WIDTH, AUSTIN_N_HEIGHT, austin_n);

    /* Draw Unimpressed Austin (Middle) */
    draw_sprite(144, 68, AUSTIN_UNIMPRESSED_WIDTH, AUSTIN_UNIMPRESSED_HEIGHT, austin_unimpressed);

    /* Draw Awooga Austin (Right) */
    draw_sprite(248, 68, AUSTIN_AWOOGA_WIDTH, AUSTIN_AWOOGA_HEIGHT, austin_awooga);

    flip_vga_buffer();

    getch();

    exit_video_mode();
    free_vga_buffer();

    return 0;
}
