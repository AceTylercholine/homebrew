#!/bin/bash

# Define source and base target directories
SRC_DIR="/var/www/html/media"
MOUNT_POINT="/home/pi/storage_new"
TARGET_BASE="$MOUNT_POINT/Soziale_Neurobiologie/MXBI/2.Data/RawData"

echo "Starting media cleanup..."
# Verify the network drive is actually mounted
if ! mountpoint -q "$MOUNT_POINT"; then
	echo "Error: Network drive is not mounted at $MOUNT_POINT."
	echo "Please mount the drive and try again."
	read -p "Press Enter to close..."
	exit 1
fi

# Delete all .jpg files
echo "Deleting .jpg files from $SRC_DIR..."
sudo find "$SRC_DIR" -maxdepth 1 -name "*.jpg" -type f -delete
echo ".jpg files deleted."

echo "Scanning for .h264 files..."

count=0
# Iterate through all .h264 files
for file in "$SRC_DIR"/*.h264; do
    # Exit loop gracefully if no .h264 files are found
    [ -e "$file" ] || { echo "No .h264 files found."; break; }

    filename=$(basename "$file")

    # Extract the 8-digit date (YYYYMMDD) from the filename 
    date_str=$(echo "$filename" | cut -d'_' -f3)

    # Validate that the extracted string is exactly 8 digits
    if [[ "$date_str" =~ ^[0-9]{8}$ ]]; then
        # Extract the year and month (YYYYMM)
        yyyy_mm="${date_str:0:6}"
        
        # Define the full target directory path
        target_dir="$TARGET_BASE/$yyyy_mm/$date_str"

        # Create the target directory structure
        mkdir -p "$target_dir"

        # Move the video file and fix ownership
        sudo mv "$file" "$target_dir/"
        sudo chown pi:pi "$target_dir/$filename"
        
        ((count++))
        echo "Moved [$count]: $filename"
    else
        echo "Warning: $filename skipped (invalid date format)."
    fi
done

echo "Process complete. Moved $count .h264 files."
read -p "Press Enter to close..."
