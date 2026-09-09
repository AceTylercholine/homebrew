import sys
import os
from PIL import Image

def combine_pages(img1_path, img2_path):
    try:
        base_name, ext = os.path.splitext(img1_path)
        output_path = f"{base_name}(2){ext}"

        with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
            total_width = img1.width + img2.width
            max_height = max(img1.height, img2.height)

            combined_img = Image.new('RGB', (total_width, max_height))
            
            # Paste the left image at coordinates (0, 0)
            combined_img.paste(img1, (0, 0))
            # Paste the right image starting at the right edge of the left image
            combined_img.paste(img2, (img1.width, 0))

            combined_img.save(output_path, quality=95)
            print(f"Combined into: {output_path}")
    except Exception as e:
        print(f"Failed to combine images: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        combine_pages(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python combine.py <left_image.jpg> <right_image.jpg>")