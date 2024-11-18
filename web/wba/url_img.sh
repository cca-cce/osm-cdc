#!/bin/bash

# Define the input TSV file
input_file="urls.tsv"

# Iterate over each line of the TSV file
while IFS= read -r url; do
    # Sanitize the URL to create the output filename
    sanitized_filename=$(echo "$url" | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed 's/-$//').png

    # Check if the file exists
    if [ -f "$sanitized_filename" ]; then
        echo "- [$url]($url) ([image]($sanitized_filename))"
    else
        echo "- [$url]($url) (missing)"
    fi
done < "$input_file"

