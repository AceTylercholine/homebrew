import os
import glob
from PIL import Image

def batch_rotate_clockwise(directory_path):
    search_pattern = os.path.join(directory_path, '*.[jJ][pP]*[gG]')
    image_files = glob.glob(search_pattern)

    for file_path in image_files:
        try:
            with Image.open(file_path) as img:
                # Transpose rewrites the pixel grid and resizes the canvas for 90-degree rotations
                rotated_img = img.transpose(Image.Transpose.ROTATE_270)
                
                # Overwriting without passing the exif parameter explicitly strips the EXIF tags
                rotated_img.save(file_path, quality=95)
                print(f"Rotated and saved: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Failed to process {os.path.basename(file_path)}: {e}")

if __name__ == '__main__':
    batch_rotate_clockwise(".")
