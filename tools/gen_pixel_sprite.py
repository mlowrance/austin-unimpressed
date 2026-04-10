from PIL import Image, ImageDraw
import os

def create_shared_palette_canvas():
    """Defines the game colors and creates the shared palette."""
    # We create a simple canvas with all our target colors
    p_img = Image.new('RGB', (16, 1), (0, 0, 0))
    p_draw = ImageDraw.Draw(p_img)
    
    # Define our specific hand-drawn color palette
    colors = [
        (0, 0, 0),       # 0: Transparency
        (230, 190, 160), # 1: Skin Base
        (200, 160, 130), # 2: Skin Shadow
        (80, 70, 60),    # 3: Hair/Goatee
        (120, 120, 120), # 4: Hair Highlight
        (0, 80, 200),    # 5: Blue Shirt
        (40, 40, 40),    # 6: Dark Pants
        (255, 255, 255), # 7: White (UI/Eyes)
        (10, 10, 10),    # 8: Near Black (Outlines)
    ]
    
    for i, c in enumerate(colors):
        p_draw.point((i, 0), fill=c)

    # Quantize to create the master 256-color adaptive palette
    # (Pillow will fill the remaining slots with an adaptive mix)
    quantized_p = p_img.quantize(colors=255)
    return quantized_p

def draw_austin_head(draw, center_x, center_y, style="normal"):
    """Hand-draws the stylized head based on geometric shapes."""
    # Base Head Shape (Dome/Oval)
    head_r = 14
    outline_col, skin_base, hair_col = (8, 1, 3) # Using our palette indices
    
    draw.ellipse([center_x - head_r, center_y - 18, center_x + head_r, center_y + 12], fill=skin_base, outline=outline_col)
    
    # Hairline/Dome (A simple arc)
    draw.arc([center_x - head_r, center_y - 20, center_x + head_r, center_y + 5], start=200, end=340, fill=hair_col, width=3)
    
    # The Goatee (A simple block/arc at the bottom)
    if style != "awooga":
        draw.chord([center_x - 10, center_y + 2, center_x + 10, center_y + 16], start=0, end=180, fill=hair_col, outline=outline_col)
    
    # The Mouth Expressions (The core of the game!)
    mouth_y = center_y + 8
    if style == "normal":
        # Slight smile
        draw.line([center_x - 4, mouth_y + 1, center_x, mouth_y + 3, center_x + 4, mouth_y + 1], fill=outline_col)
    elif style == "unimpressed":
        # The flat line mouth
        draw.line([center_x - 5, mouth_y + 1, center_x + 5, mouth_y + 1], fill=outline_col)
    elif style == "awooga":
        # Huge open mouth
        draw.ellipse([center_x - 6, mouth_y - 2, center_x + 6, mouth_y + 6], fill=outline_col)
        # Stretched goatee shape
        draw.chord([center_x - 12, center_y + 5, center_x + 12, center_y + 18], start=0, end=180, fill=hair_col)

    # The Eyes
    eye_y = center_y - 5
    if style == "awooga":
        # Stretched eyes
        draw.ellipse([center_x - 8, eye_y - 5, center_x - 2, eye_y + 5], fill=7, outline=outline_col) # White
        draw.ellipse([center_x + 2, eye_y - 5, center_x + 8, eye_y + 5], fill=7, outline=outline_col) # White
    else:
        # Standard eyes (Dots or small lines)
        draw.line([center_x - 6, eye_y, center_x - 4, eye_y], fill=outline_col)
        draw.line([center_x + 4, eye_y, center_x + 6, eye_y], fill=outline_col)

def draw_austin_body(draw, start_y):
    """Draws the tiny 'bobblehead' body (blue shirt and pants)."""
    # Simple block for the body (width 16px, centered)
    blue_shirt, dark_pants, outline = (5, 6, 8)
    
    # Shirt
    draw.rectangle([8, start_y, 24, start_y + 8], fill=blue_shirt, outline=outline)
    # Pants
    draw.rectangle([8, start_y + 8, 24, start_y + 15], fill=dark_pants, outline=outline)
    # Small feet placeholders
    draw.point((12, start_y + 15), fill=outline)
    draw.point((20, start_y + 15), fill=outline)

def generate_sprites():
    os.makedirs('assets', exist_ok=True)
    
    # Get the master quantized palette (P mode image)
    quantized_p = create_shared_palette_canvas()
    palette = quantized_p.getpalette()
    palette_padded = palette + [0] * (768 - len(palette))

    # 1. Export palette.h (6-bit VGA format)
    with open('assets/palette.h', 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\nunsigned char game_palette[] = {\n")
        for i in range(256):
            r, g, b = palette_padded[i*3]//4, palette_padded[i*3+1]//4, palette_padded[i*3+2]//4
            f.write(f"{r},{g},{b}, " + ("\n" if (i+1)%4==0 else ""))
        f.write("\n};\n\n#endif\n")

    # 2. Generate and export each sprite state (32x64)
    sprite_configs = [
        ("austin_normal", "normal"),
        ("austin_unimpressed", "unimpressed"),
        ("austin_awooga", "awooga")
    ]
    
    for name, style in sprite_configs:
        # Create a new 32x64 canvas in palette mode (P) using our shared palette
        sprite_img = Image.new('P', (32, 64), 0) # 0 is transparent black
        sprite_img.putpalette(palette)
        draw = ImageDraw.Draw(sprite_img)
        
        # Draw the parts using the geometry logic
        draw_austin_head(draw, 16, 24, style=style)
        draw_austin_body(draw, 48)
        
        # Export as header file
        pixels = list(sprite_img.getdata())
        with open(f'assets/{name}.h', 'w') as f:
            f.write(f"#ifndef {name.upper()}_H\n#define {name.upper()}_H\n")
            f.write(f"#define {name.upper()}_WIDTH  32\n")
            f.write(f"#define {name.upper()}_HEIGHT 64\n\n")
            f.write(f"unsigned char {name}[] = {{\n")
            for j, p in enumerate(pixels):
                f.write(f"{p}," + ("\n" if (j+1)%32==0 else ""))
            f.write("\n};\n\n#endif\n")

    print("Success! Created hand-drawn pixel-art sprite headers (Normal, Unimpressed, Awooga) and the game palette.")

if __name__ == "__main__":
    generate_sprites()