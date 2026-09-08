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

# Enable nullglob so the array is empty if no files match
shopt -s nullglob
files=("$SRC_DIR"/*.h264)
total=${#files[@]}
shopt -u nullglob # Turn it back off to maintain standard bash behavior

if [ "$total" -eq 0 ]; then
    echo "No .h264 files found."
else
    echo "Found $total file(s). Starting transfer..."
    count=0

    for file in "${files[@]}"; do
        filename=$(basename "$file")
        date_str=$(echo "$filename" | cut -d'_' -f3)

        if [[ "$date_str" =~ ^[0-9]{8}$ ]]; then
            yyyy_mm="${date_str:0:6}"
            target_dir="$TARGET_BASE/$yyyy_mm/$date_str"

            mkdir -p "$target_dir"

            echo -e "\nMoving file $((count+1)) of $total: $filename"
            
            # Use rsync to show real-time transfer progress, then delete the source
            sudo rsync -ah --progress --remove-source-files "$file" "$target_dir/"
            
            # Verify the transfer was successful before altering ownership
            if [ $? -eq 0 ]; then
                sudo chown pi:pi "$target_dir/$filename"
                ((count++))
            else
                echo "Error: Transfer failed for $filename. File retained at source."
            fi
        else
            echo -e "\nWarning: $filename skipped (invalid date format)."
        fi
    done
fi

echo -e "\nProcess complete. Moved $count .h264 files."
read -p "Press Enter to close..."
