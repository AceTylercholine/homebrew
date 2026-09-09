import os
import glob
from PIL import Image

def batch_rotate_clockwise(directory_path):
    search_pattern = os.path.join(directory_path, '*.[jJ][pP]*[gG]')
    image_files = glob.glob(search_pattern)

    for file_path in image_files:
        try:
            # Open and read the image
            with Image.open(file_path) as img:
                rotated_img = img.transpose(Image.Transpose.ROTATE_270)
            
            # The 'with' block ends here, closing the original file lock.
            # Now it is safe to overwrite the file on Windows.
            rotated_img.save(file_path, quality=95)
            print(f"Rotated and saved: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Failed to process {os.path.basename(file_path)}: {e}")

if __name__ == '__main__':
    batch_rotate_clockwise(".")