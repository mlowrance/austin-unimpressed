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
# Format: R, G, B (0-63)
palette = [0] * (256 * 3)
# 0: Black
palette[0:3] = [0, 0, 0]
# 1: Blue
palette[3:6] = [0, 0, 40]
# 7: Grey
palette[21:24] = [40, 40, 40]
# 10: Green
palette[30:33] = [0, 60, 0]
# 12: Red
palette[36:39] = [60, 0, 0]
# 14: Yellow
palette[42:45] = [60, 60, 0]
# 15: White
palette[45:48] = [60, 60, 60]

with open("assets/palette.h", "w") as f:
    f.write("#ifndef PALETTE_H\n#define PALETTE_H\n\n")
    f.write("unsigned char austin_palette[] = {\n")
    for i in range(0, 256 * 3, 3):
        f.write(f"{palette[i]},{palette[i+1]},{palette[i+2]}, ")
        if (i//3 + 1) % 8 == 0: f.write("\n")
    f.write("\n};\n\n#endif\n")

def gen_box(w, h, color, face_color=None, expression=None):
    img = [0] * (w * h)
    # Border
    for x in range(w):
        img[x] = 15
        img[(h-1)*w + x] = 15
    for y in range(h):
        img[y*w] = 15
        img[y*w + (w-1)] = 15
    
    # Face Area
    if face_color:
        for y in range(5, 25):
            for x in range(5, w-5):
                img[y*w + x] = face_color
                
    # Expression
    if expression == "normal":
        img[15*w + 10] = 0; img[15*w + 20] = 0 # Eyes
        for x in range(12, 20): img[20*w + x] = 0 # Smile
    elif expression == "unimpressed":
        img[15*w + 10] = 0; img[15*w + 20] = 0 # Eyes
        for x in range(10, 22): img[18*w + x] = 0 # Flat line
    elif expression == "awooga":
        # Big Eyes
        for y in range(10, 18):
            for x in range(8, 14): img[y*w + x] = 15
            for x in range(18, 24): img[y*w + x] = 15
        # Big Mouth
        for y in range(22, 30):
            for x in range(10, 22): img[y*w + x] = 12
            
    return img

# Generate Austin States
save_header("AUSTIN_N", 32, 64, gen_box(32, 64, 1, 14, "normal"))
save_header("AUSTIN_UNIMPRESSED", 32, 64, gen_box(32, 64, 1, 12, "unimpressed"))
save_header("AUSTIN_AWOOGA", 32, 64, gen_box(32, 64, 1, 10, "awooga"))

# Retirement Bar
bar = [0] * (100 * 20)
for x in range(100):
    bar[x] = 15; bar[19*100 + x] = 15
for y in range(20):
    bar[y*100] = 15; bar[y*100 + 99] = 15
save_header("RETIREMENT_BAR", 100, 20, bar)
