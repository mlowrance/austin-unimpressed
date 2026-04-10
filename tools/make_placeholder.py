from PIL import Image, ImageDraw
import os

def create_placeholder_sprite():
    # Create a perfect 64x128 canvas with a black background
    img = Image.new('RGB', (64, 128), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a blocky, structural "Austin"
    # Hair (Grey)
    draw.rectangle([16, 16, 48, 28], fill=(128, 128, 128))
    # Face (Peach)
    draw.rectangle([16, 28, 48, 56], fill=(255, 204, 153))
    # Goatee (Dark Grey)
    draw.rectangle([26, 48, 38, 56], fill=(100, 100, 100))
    # Shirt (Blue)
    draw.rectangle([12, 56, 52, 96], fill=(0, 102, 204))
    # Pants (Dark Grey)
    draw.rectangle([20, 96, 44, 124], fill=(40, 40, 50))
    # Boots (Brown)
    draw.rectangle([16, 124, 48, 128], fill=(139, 69, 19))

    # Save it exactly where we need it
    output_path = 'a_norm_dlx.png'
    img.save(output_path)
    print(f"Success! Guaranteed 64x128 placeholder saved as {output_path}")

if __name__ == "__main__":
    create_placeholder_sprite()