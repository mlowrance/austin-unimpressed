from PIL import Image
import os

def extract_palette(image_path, output_h):
    img = Image.open(image_path)
    if img.mode != 'P':
        print(f"Error: {image_path} is not an indexed (Palette) image. Converting...")
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    
    raw_palette = img.getpalette()
    # Padding to 768 bytes (256 * 3)
    palette = raw_palette + [0] * (768 - len(raw_palette))
    
    with open(output_h, 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
        f.write("unsigned char austin_palette[] = {\n")
        for i in range(256):
            # VGA palette uses 6 bits per channel (0-63)
            r, g, b = palette[i*3]//4, palette[i*3+1]//4, palette[i*3+2]//4
            f.write(f"{r},{g},{b}, ")
            if (i + 1) % 8 == 0:
                f.write("\n")
        f.write("\n};\n\n#endif\n")
    print(f"Successfully extracted palette to {output_h}")

if __name__ == "__main__":
    extract_palette('a_norm_dlx.png', 'assets/palette.h')
