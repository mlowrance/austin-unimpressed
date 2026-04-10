from PIL import Image
import os
import sys

def convert_png_to_dos_header(png_path, sprite_name):
    """
    Converts a 64x128 PNG to a DOS C header file.
    Ensures absolute black (0,0,0) is index 0 for transparency.
    """
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)
    
    if not os.path.exists(png_path):
        print(f"Error: {png_path} not found.")
        return

    try:
        img = Image.open(png_path).convert('RGB')
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # --- THE DELUXE CHECK ---
    if img.size != (64, 128):
        print(f"Error: {png_path} must be exactly 64x128. Current: {img.size}")
        return

    # Convert to 256-color palette
    img_indexed = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    raw_palette = img_indexed.getpalette() # 768 entries
    
    # 1. Create palette.h (Shared game colors)
    palette_path = os.path.join(assets_dir, 'palette.h')
    if not os.path.exists(palette_path):
        with open(palette_path, 'w') as f:
            f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
            f.write("unsigned char game_palette[] = {\n")
            for i in range(256):
                # VGA 6-bit conversion (0-255 -> 0-63)
                r, g, b = raw_palette[i*3]//4, raw_palette[i*3+1]//4, raw_palette[i*3+2]//4
                f.write(f"  {r},{g},{b}," + ("\n" if (i+1)%4 == 0 else " "))
            f.write("\n};\n\n#endif\n")
        print(f"Created: {palette_path}")

    # 2. Create the Sprite Header (e.g., A_NORM.H)
    dos_filename = sprite_name.upper()[:8] + ".H"
    output_path = os.path.join(assets_dir, dos_filename)
    pixels = list(img_indexed.getdata())
    
    with open(output_path, 'w') as f:
        f.write(f"#ifndef {sprite_name}_H\n#define {sprite_name}_H\n\n")
        f.write(f"#define {sprite_name}_WIDTH  64\n")
        f.write(f"#define {sprite_name}_HEIGHT 128\n\n")
        f.write(f"unsigned char __far {sprite_name.lower()}[] = {{\n")
        for i, p in enumerate(pixels):
            f.write(f"{p}, " + ("\n" if (i + 1) % 64 == 0 else ""))
        f.write("\n};\n\n#endif\n")

    print(f"Success! Generated {output_path}")

if __name__ == "__main__":
    print("\n--- Austin Unimpressed: Sprite-to-C Converter ---")
    png_input = input("PNG filename (e.g., a_norm_dlx.png): ").strip()
    sprite_name = input("Sprite Variable Name (e.g., A_NORM): ").strip().upper()
    convert_png_to_dos_header(png_input, sprite_name)