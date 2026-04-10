import os

def save_header(name, width, height, data, folder="assets"):
    path = os.path.join(folder, name.lower() + ".h")
    guard = name.upper() + "_H"
    with open(path, "w") as f:
        f.write(f"#ifndef {guard}\n#define {guard}\n\n")
        f.write(f"#define {name.upper()}_WIDTH {width}\n")
        f.write(f"#define {name.upper()}_HEIGHT {height}\n\n")
        f.write(f"unsigned char {name.lower()}[] = {{\n")
        for i, val in enumerate(data):
            f.write(f"{val},")
            if (i + 1) % width == 0:
                f.write("\n")
        f.write("};\n\n#endif\n")

# 1. Simple Palette (Standard VGA-ish)
palette = [0] * (256 * 3)
palette[0:3] = [0, 0, 0] # 0: Black
palette[3:6] = [0, 0, 40] # 1: Blue
palette[21:24] = [40, 40, 40] # 7: Grey
palette[30:33] = [0, 60, 0] # 10: Green
palette[36:39] = [60, 0, 0] # 12: Red
palette[42:45] = [60, 60, 0] # 14: Yellow
palette[45:48] = [60, 60, 60] # 15: White

with open("assets/palette.h", "w") as f:
    f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
    f.write("unsigned char austin_palette[] = {\n")
    for i in range(0, 256 * 3, 3):
        f.write(f"{palette[i]},{palette[i+1]},{palette[i+2]}, ")
        if (i//3 + 1) % 8 == 0: f.write("\n")
    f.write("\n};\n\n#endif\n")

def gen_box(w, h, border_color, fill_color=0, pattern=None):
    img = [0] * (w * h)
    for x in range(w):
        img[x] = border_color
        img[(h-1)*w + x] = border_color
    for y in range(h):
        img[y*w] = border_color
        img[y*w + (w-1)] = border_color
    
    if fill_color:
        for y in range(1, h-1):
            for x in range(1, w-1):
                img[y*w + x] = fill_color

    if pattern == "strips":
        for y in range(5, h-5, 4):
            for x in range(5, w-5): img[y*w + x] = 14 # Yellow strips
    elif pattern == "pr":
        for y in range(5, h-5):
            img[y*w + w//2] = 15 # Vertical line
            if y % 10 < 5:
                for x in range(w//2, w-5): img[y*w + x] = 15
    elif pattern == "money":
        for y in range(h//4, 3*h//4):
            for x in range(w//4, 3*w//4): img[y*w + x] = 10 # Green $
            
    return img

# Austin States
save_header("AUSTIN_N", 32, 64, gen_box(32, 64, 15, 14))
save_header("AUSTIN_UNIMPRESSED", 32, 64, gen_box(32, 64, 15, 12))
save_header("AUSTIN_AWOOGA", 32, 64, gen_box(32, 64, 15, 10))

# Retirement Bar
save_header("RETIREMENT_BAR", 100, 20, gen_box(100, 20, 15))

# NEW: Bosses and End Game Assets
save_header("BOSS_CHICKEN", 48, 48, gen_box(48, 48, 12, 0, "strips"))
save_header("BOSS_PR", 48, 48, gen_box(48, 48, 1, 0, "pr"))
save_header("MONEY", 32, 32, gen_box(32, 32, 10, 0, "money"))
save_header("HOUSE", 64, 64, gen_box(64, 64, 7, 0)) # Simple grey house
