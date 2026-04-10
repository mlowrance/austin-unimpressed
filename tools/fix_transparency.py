from PIL import Image

def process_sprite(image_path, name):
    img = Image.open(image_path).convert('RGBA')
    # Create a new image with a distinct background color (e.g., magenta)
    # to differentiate it from the sprite's content.
    new_img = Image.new('RGBA', img.size, (255, 0, 255, 255))
    new_img.paste(img, (0, 0), img)
    
    # Quantize to 256 colors including transparency
    quantized = new_img.quantize(colors=255)
    # The background should be index 0 (which will be transparent)
    
    # Extract palette and sprite data...
    # (Implementation details for palette extraction and saving)
    print(f"Generated {name}.h")

if __name__ == "__main__":
    process_sprite('a_norm_dlx.png', 'A_NORM')
