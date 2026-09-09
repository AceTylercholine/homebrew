import os
import shutil
import zipfile
import argparse
import glob

def epub_to_cbz(epub_path):
    """
    Converts an EPUB file to CBZ by extracting images and re-archiving them.
    """
    if not os.path.isfile(epub_path):
        print(f"Error: File {epub_path} not found.")
        return

    filename = os.path.basename(epub_path)
    base_name = os.path.splitext(filename)[0]
    target_cbz = os.path.splitext(epub_path)[0] + ".cbz"

    # Skip if CBZ already exists to prevent redundant processing
    if os.path.exists(target_cbz):
        print(f"Skipping: {target_cbz} already exists.")
        return

    # Temp directory for extraction
    temp_dir = f"temp_{base_name}"
    # Clean up previous failed runs if they exist
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    try:
        print(f"Processing: {filename}")
        
        with zipfile.ZipFile(epub_path, 'r') as z:
            z.extractall(temp_dir)

        image_files = []
        valid_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in valid_exts:
                    full_path = os.path.join(root, file)
                    # Filter out tiny metadata icons (< 10KB)
                    if os.path.getsize(full_path) > 10240:
                        image_files.append(full_path)

        if not image_files:
            print(f"Warning: No significant images found in {filename}.")
            return

        image_files.sort()
        
        with zipfile.ZipFile(target_cbz, 'w') as cbz:
            for img_path in image_files:
                cbz.write(img_path, arcname=os.path.basename(img_path))
        
        print(f"Success: Created {target_cbz}")

    except zipfile.BadZipFile:
        print(f"Error: {filename} is not a valid ZIP/EPUB file.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert EPUB comics to CBZ.")
    parser.add_argument(
        "files", 
        nargs='*',  # Changed from '+' to '*' to allow zero arguments
        help="EPUB files to convert. If empty, scans current directory."
    )
    args = parser.parse_args()

    # Logic: Use arguments if provided, otherwise scan current dir
    if args.files:
        file_list = args.files
    else:
        file_list = glob.glob("*.epub")
        if not file_list:
            print("No EPUB files found in the current directory.")

    for f in file_list:
        epub_to_cbz(f)