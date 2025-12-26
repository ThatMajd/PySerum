#!/bin/bash

# Check if argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_preset.SerumPreset>"
    exit 1
fi

# Convert to absolute paths immediately
INPUT_FILE="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
FILENAME=$(basename -- "$INPUT_FILE")
BASENAME="${FILENAME%.*}"
DIRNAME=$(dirname "$INPUT_FILE")
OUTPUT_FILE="${DIRNAME}/${BASENAME}.json"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1
fi

# Get the absolute path to the packager directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGER_DIR="${SCRIPT_DIR}/serum-preset-packager"

# Run the unpack command
echo "Unpacking '$INPUT_FILE' to '$OUTPUT_FILE'..."
cd "$PACKAGER_DIR" || exit
python3 cli.py unpack "$INPUT_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Done!"
else
    echo "Failed to unpack preset."
    exit 1
fi
