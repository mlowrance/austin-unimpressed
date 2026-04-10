from PIL import Image
import os

def rip_assets(mockup_path):
    os.makedirs('assets', exist_ok=True)
    
    if not os.path.exists(mockup_path):
        print(f"Error: {mockup_path} not found!")
        return

    # Load the mockup
    img = Image.open(mockup_path).convert('RGB')
    
    # 1. Define the crop areas (Left, Top, Right, Bottom)
    # These coordinates are calibrated to the mockup I sent you.
    # Austin is roughly in the center-top (Normal), middle (Unimpressed), and bottom (Awooga).
    crops = {
        "austin_normal":      (400, 20, 600, 280),   # Panel 1
        "austin_unimpressed": (400, 480, 600, 740),  # Panel 3
        "austin_awooga":      (380, 830, 620, 1100), # Panel 4
    }

    # 2. Process into a shared 256-color palette
    quantized_master = img.quantize(colors=255)
    palette = quantized_master.getpalette()
    palette_padded = palette + [0] * (768 - len(palette))

    # 3. Export palette.h (VGA 6-bit)
    with open('assets/palette.h', 'w') as f:
        f.write("#ifndef PALETTE_H\n#define PALETTE_H\nunsigned char game_palette[] = {\n")
        for i in range(256):
            r, g, b = palette_padded[i*3]//4, palette_padded[i*3+1]//4, palette_padded[i*3+2]//4
            f.write(f"{r},{g},{b}, " + ("\n" if (i+1)%4==0 else ""))
        f.write("\n};\n#endif\n")

    # 4. Extract and Save Sprites
    for name, coords in crops.items():
        # Crop and resize to our 16-bit DOS spec (32x64)
        sprite = quantized_master.crop(coords).resize((32, 64), Image.Resampling.NEAREST)
        
        # Save a debug image so you can see if the crop was successful!
        sprite.convert('RGB').save(f'assets/{name}_preview.png')
        
        pixels = list(sprite.getdata())
        with open(f'assets/{name}.h', 'w') as f:
            f.write(f"#ifndef {name.upper()}_H\n#define {name.upper()}_H\n")
            f.write(f"unsigned char {name}[] = {{\n")
            for j, p in enumerate(pixels):
                f.write(f"{p}," + ("\n" if (j+1)%32==0 else ""))