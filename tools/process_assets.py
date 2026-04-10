from PIL import Image, ImageDraw
import os

def generate_all_assets():
    os.makedirs('assets', exist_ok=True)
    
    try:
        img_smile = Image.open('austin.jpg').convert('RGB')
        img_unimpressed = Image.open('unnamed.jpg').convert('RGB')
    except FileNotFoundError as e:
        print(f"Error: Could not find your image files. Make sure 'austin.jpg' and 'unnamed.jpg' are in this folder. {e}")
        return

    img_smile = img_smile.resize((32, 48), Image.Resampling.LANCZOS)
    img_unimpressed = img_unimpressed.resize((32, 48), Image.Resampling.LANCZOS)

    master = Image.new('RGB', (256, 128), (0, 0, 0))
    master.paste(img_smile, (0, 0))
    master.paste(img_unimpressed, (32, 0))
    
    shocked = img_unimpressed.resize((32, 60)).crop((0, 0, 32, 48))
    master.paste(shocked, (64, 0))

    draw = ImageDraw.Draw(master)
    draw.text((100, 10), "AUSTIN", fill=(0, 120, 255)) 
    draw.text((100, 25), "UNIMPRESSED", fill=(200, 200, 200)) 
    draw.rectangle([100, 50, 200, 60], outline=(255, 255, 255))
    draw.rectangle([101, 51, 150, 59], fill=(255, 100, 0))

    quantized = master.quantize(colors=255)
    raw_palette = quantized.getpalette() # This might be less than 768 entries
    
    # --- FIX: Padding the palette to exactly 768 bytes (256 * 3) ---
    palette = raw_palette + [0] * (768 - len(raw_palette))
    
    with open('assets/palette.h', 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\nunsigned char game_palette[] = {\n")
        for i in range(256):
            r, g, b = palette[i*3]//4, palette[i*3+1]//4, palette[i*3+2]//4
            f.write(f"{r},{g},{b}, " + ("\n" if (i+1)%4==0 else ""))
        f.write("\n};\n\n#endif\n")

    def save_sprite(name, x, y, w, h):
        sprite = quantized.crop((x, y, x + w, y + h))
        pixels = list(sprite.getdata())
        with open(f'assets/{name}.h', 'w') as f:
            f.write(f"#ifndef {name.upper()}_H\n#define {name.upper()}_H\n\n")
            f.write(f"#define {name.upper()}_WIDTH {w}\n#define {name.upper()}_HEIGHT {h}\n\n")
            f.write(f"unsigned char {name}[] = {{\n")
            for j, p in enumerate(pixels):
                f.write(f"{p}," + ("\n" if (j+1)%w==0 else ""))
            f.write("\n};\n\n#endif\n")

    save_sprite("austin_normal", 0, 0, 32, 64)
    save_sprite("austin_unimpressed", 32, 0, 32, 64)
    save_sprite("austin_awooga", 64, 0, 32, 64)
    save_sprite("title_logo", 100, 5, 120, 40)
    save_sprite("retirement_bar", 100, 50, 100, 20)

    print("Success! Created Palette and all game assets.")

if __name__ == "__main__":
    generate_all_assets()