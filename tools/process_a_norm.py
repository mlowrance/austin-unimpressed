from PIL import Image

def process_sprite(image_path, name):
    # Open as RGBA to keep transparency
    img = Image.open(image_path).convert('RGBA')
    
    # Quantize to 255 colors + 1 for transparent background
    # 0 will be the transparent index
    quantized = img.quantize(colors=255, method=Image.FASTOCTREE)
    
    # Ensure index 0 is transparent (background)
    # The quantize method often puts the most common color (background) at index 0.
    
    raw_palette = quantized.getpalette()
    palette = raw_palette + [0] * (768 - len(raw_palette))
    
    # Set index 0 to a distinct color for the game background (Grey = 7)
    # VGA palette index 7 is light grey (42, 42, 42)
    # The quantize might have moved the background, let's force index 0 to be our clear color
    palette[0:3] = [42, 42, 42] 
    
    # Save Palette
    with open('assets/palette.h', 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\nunsigned char austin_palette[768] = {\n")
        for i in range(256):
            r, g, b = palette[i*3]//4, palette[i*3+1]//4, palette[i*3+2]//4
            f.write(f"{r},{g},{b}, ")
            if (i + 1) % 8 == 0: f.write("\n")
        f.write("\n};\n\n#endif\n")

    # Save Sprite
    w, h = quantized.size
    pixels = list(quantized.getdata())
    with open(f'assets/{name}.h', 'w') as f:
        f.write(f"#ifndef {name.upper()}_H\n#define {name.upper()}_H\n\n")
        f.write(f"#define {name.upper()}_WIDTH {w}\n#define {name.upper()}_HEIGHT {h}\n\n")
        f.write(f"unsigned char __far {name.lower()}[] = {{\n")
        for j, p in enumerate(pixels):
            # If the pixel was transparent in the original, force it to 0
            # For this simple approach, we assume the background is index 0
            f.write(f"{p}," + ("\n" if (j+1)%w==0 else ""))
        f.write("\n};\n\n#endif\n")
    print(f"Generated {name}.h and palette.h. Background forced to grey.")

if __name__ == "__main__":
    process_sprite('a_norm_dlx.png', 'A_NORM')
