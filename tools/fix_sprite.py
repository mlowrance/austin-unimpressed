from PIL import Image
import os

def fix_my_sprite():
    input_file = 'austin_normal.jpeg' # Make sure your saved AI image is named this
    output_file = 'a_norm.png'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    # Load the image
    img = Image.open(input_file).convert('RGB')
    
    # Find the 'Bounding Box' of all non-black pixels
    # This automatically ignores the black space around him
    bg = Image.new('RGB', img.size, (0, 0, 0))
    diff = ImageChops.difference(img, bg) if 'ImageChops' in globals() else None
    
    # Simpler version if ImageChops isn't imported: 
    # Get the area of the image that isn't black
    bbox = img.getbbox()
    
    if not bbox:
        print("Error: The image seems to be entirely black!")
        return

    # Crop exactly to his body
    austin_only = img.crop(bbox)
    
    # Now resize to our 32x64 DOS spec
    # NEAREST keeps those chunky pixels looking like art instead of a blur
    final_sprite = austin_only.resize((32, 64), Image.Resampling.NEAREST)
    
    final_sprite.save(output_file)
    print(f"Success! Austin is now fully contained in {output_file} (32x64).")

if __name__ == "__main__":
    from PIL import ImageChops # Needed for the bounding box logic
    fix_my_sprite()