from PIL import Image
import os

def generate_header(image_path, output_path):
    # Create the assets directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found in current directory.")
        return

    # Load and resize to our Bobblehead specs
    img = Image.open(image_path).convert('RGB')
    
    # Crop to square and resize head to 32x48
    width, height = img.size
    square_size = min(width, height)
    img = img.crop((0, 0, square_size, square_size))
    img = img.resize((32, 48), Image.Resampling.LANCZOS)
    
    # Create a 32x64 canvas (black background)
    canvas = Image.new('RGB', (32, 64), (0, 0, 0))
    canvas.paste(img, (0, 0)) 
    
    # Simple "Tiny Body" block (Dark Grey)
    for x in range(8, 24):
        for y in range(48, 64):
            canvas.putpixel((x, y), (60, 60, 60))

    # Convert to 256 colors
    img_indexed = canvas.convert('P', palette=Image.ADAPTIVE, colors=255)
    pixels = list(img_indexed.getdata())
    raw_palette = img_indexed.getpalette()

    # Ensure palette is exactly 768 bytes (256 * 3)
    palette = raw_palette + [0] * (768 - len(raw_palette))

    # Write austin.h
    with open(output_path, 'w') as f:
        f.write("#ifndef AUSTIN_H\n#define AUSTIN_H\n\n")
        f.write(f"#define AUSTIN_WIDTH 32\n#define AUSTIN_HEIGHT 64\n\n")
        f.write("unsigned char austin_idle[] = {\n")
        for i, p in enumerate(pixels):
            f.write(f"{p}, " + ("\n" if (i + 1) % 16 == 0 else ""))
        f.write("\n};\n\n#endif")

    # Write palette.h
    palette_path = os.path.join(os.path.dirname(output_path), 'palette.h')
    with open(palette_path, 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
        f.write("unsigned char austin_palette[] = {\n")
        for i in range(256):
            r, g, b = palette[i*3], palette[i*3+1], palette[i*3+2]
            # Convert 8-bit (0-255) to VGA 6-bit (0-63)
            f.write(f"{r//4}, {g//4}, {b//4}, " + ("\n" if (i + 1) % 4 == 0 else ""))
        f.write("\n};\n\n#endif")

    print(f"Success! Created {output_path} and {palette_path}")

generate_header('austin.jpg', 'assets/austin.h')