from PIL import Image
import os
import sys

def convert_png_to_dos_header(png_path, sprite_name):
    """
    Converts a standardized 32x64 PNG (Index 0 = transparent)
    to a C header file (e.g., A_UNIMP.H).
    """
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)
    
    # Check if the file exists
    if not os.path.exists(png_path):
        print(f"Error: {png_path} not found. Please provide a valid PNG.")
        return

    # Load and force the image into the standardized 256-color palette
    try:
        img = Image.open(png_path).convert('P', colors=256)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # 1. Enforce the Standard Resolution (32x64)
    if img.size != (32, 64):
        print(f"Error: {png_path} must be exactly 32x64 pixels. Current size: {img.size}.")
        return

    # 2. Export palette.h (from the first converted sprite)
    # We will generate one palette.h and ensure ALL sprites use it.
    palette_path = os.path.join(assets_dir, 'palette.h')
    if not os.path.exists(palette_path):
        print(f"Generating base game palette from {sprite_name}...")
        raw_palette = img.getpalette() # 768 entries (256 * 3)
        
        with open(palette_path, 'w') as f:
            f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
            f.write("unsigned char game_palette[] = {\n")
            for i in range(256):
                # VGA 6-bit conversion (0-63)
                r = raw_palette[i*3] // 4
                g = raw_palette[i*3+1] // 4
                b = raw_palette[i*3+2] // 4
                f.write(f"  {r},{g},{b}," + (" // Color Index {}\n".format(i) if (i + 1) % 4 == 0 else " "))
            f.write("\n};\n\n#endif\n")
        print(f"Success! Base palette created at {palette_path}.")

    # 3. Export Sprite Data to Header
    # We use a strict 8.3 filename (e.g., A_UNIMP.H) to avoid DOS issues later.
    dos_filename = sprite_name.upper()[:8] + ".H"
    sprite_header_name = sprite_name.upper()[:8]
    
    output_path = os.path.join(assets_dir, dos_filename)
    pixels = list(img.getdata())
    
    with open(output_path, 'w') as f:
        f.write(f"#ifndef {sprite_header_name}_H\n#define {sprite_header_name}_H\n\n")
        f.write(f"#define {sprite_header_name}_WIDTH  32\n")
        f.write(f"#define {sprite_header_name}_HEIGHT 64\n\n")
        
        # We specify the array is located in the FAR memory segment
        # (Needed for larger memory models in Watcom)
        f.write(f"unsigned char __far {sprite_header_name.lower()}[] = {{\n")
        for i, p in enumerate(pixels):
            f.write(f"{p}, " + ("\n" if (i + 1) % 32 == 0 else ""))
        f.write("\n};\n\n#endif\n")

    print(f"Success! {png_path} converted to {output_path}.")
    print("This sprite is now locked to the master game palette.")

# --- The Interactive Prompt ---
if __name__ == "__main__":
    print("\n--- Austin Unimpressed: Unified Asset Converter (32x64 PNG) ---")
    
    # Prompt for the PNG file
    png_input = input("Enter the path to the 32x64 PNG master file (e.g., a_unimp.png): ").strip()
    
    if not png_input:
        print("Error: A file path is required.")
        sys.exit(1)

    # Prompt for the short, DOS-friendly name
    sprite_input = input("Enter a DOS-friendly name (max 8 chars, e.g., A_UNIMP): ").strip().upper()
    
    if not sprite_input:
        print("Error: A sprite name is required.")
        sys.exit(1)
        
    convert_png_to_dos_header(png_input, sprite_input)