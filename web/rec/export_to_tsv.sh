#!/bin/bash

# Define the database and tables
DATABASE="tracking.db"
TABLES=("mouse_positions" "click_positions" "scroll_positions")

# Loop through each table and export to TSV
for TABLE in "${TABLES[@]}"; do
    OUTPUT_FILE="${TABLE}.tsv"
    sqlite3 -header -separator $'\t' "$DATABASE" "SELECT * FROM $TABLE;" > "$OUTPUT_FILE"
    echo "Exported $TABLE to $OUTPUT_FILE"
done
