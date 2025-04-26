#!/usr/bin/env python3
import argparse
import csv
import os
import sys

def parse_columns_options(r_option, c_option, total_columns):
    """
    Determines which columns (1-indexed) to consider for the duplicate check.

    Parameters:
      r_option (str or None): The value for -r. It can be a single number or a hyphen-delimited
                              list of column numbers (e.g. "3" or "3-5-8").
      c_option (int or None): The value for -c (i.e. the count of columns to consider).
      total_columns (int): Total number of columns available (from the CSV's header).

    Returns:
      A list of column numbers (1-indexed) to check.

    Behavior:
      - If r_option is provided:
         * If c_option is also provided, only the first number in r_option is used as the starting
           column and the count from c_option defines the consecutive columns.
         * If c_option is not provided, then r_option is parsed as a list (e.g. "3-5-8" becomes [3, 5, 8]).
      - If r_option is not provided but c_option is, then start from column 1 and use the first c_option
        columns.
      - If neither is provided, then all columns (1 through total_columns) are used.
    """
    columns = []
    if r_option:
        parts = r_option.split('-')
        try:
            if c_option is not None:
                # With both -r and -c provided: use the first number from -r as the starting column.
                start = int(parts[0])
                columns = list(range(start, start + c_option))
            else:
                # Only -r provided: treat the option as a list of columns.
                columns = [int(x) for x in parts]
        except ValueError:
            sys.exit("Error: Invalid column number detected in -r option. Please ensure all parts are integers.")
    else:
        if c_option is not None:
            # Without -r but with -c: default starting column is 1.
            start = 1
            columns = list(range(start, start + c_option))
        else:
            # If neither -r nor -c is provided, use all available columns.
            columns = list(range(1, total_columns + 1))
    
    # Ensure selected columns are within the available range.
    valid_columns = [col for col in columns if 1 <= col <= total_columns]
    if not valid_columns:
        sys.exit("Error: No valid columns specified for duplicate checking based on the CSV size.")
    return valid_columns

def list_headers(csvfile):
    """
    Reads and prints the header row of the CSV file with 1-indexed positions.
    """
    try:
        with open(csvfile, newline='') as csv_in:
            reader = csv.reader(csv_in)
            headers = next(reader)
    except StopIteration:
        sys.exit("Error: The CSV file is empty.")
    except Exception as e:
        sys.exit(f"Error reading CSV file: {e}")
    
    print("Column index : Header")
    for idx, header in enumerate(headers, start=1):
        print(f"{idx}: {header}")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate rows from a CSV based on specified column(s) values. "
                    "Also, log duplicate pairs’ column1 values in a two-column file 'deduplicate_list', "
                    "or list headers with the -q option."
    )
    parser.add_argument("csvfile", help="Input CSV file path.")
    parser.add_argument("-c", type=int, help="Count of columns to check (if not given, all columns are used unless -r specifies a subset).")
    parser.add_argument("-r", type=str, help="Column specifier. When used with -c, the first value is the starting column. "
                                              "When used alone, provide a hyphen-separated list (e.g., 3-5-8) of columns to check.")
    parser.add_argument("-q", action="store_true", help="List the column headers with indexes. If provided, all other options are ignored.")
    args = parser.parse_args()

    input_file = args.csvfile
    if not os.path.isfile(input_file):
        sys.exit("Error: Input file does not exist.")

    # If -q is provided, list headers and ignore other options.
    if args.q:
        list_headers(input_file)

    # Read all rows from the CSV.
    with open(input_file, newline='') as csv_in:
        reader = csv.reader(csv_in)
        rows = list(reader)
    
    if not rows:
        sys.exit("Error: The CSV file is empty.")

    # Determine total number of columns from the first row (header).
    total_columns = len(rows[0])

    # Determine which columns to use for checking duplicates.
    # Columns are treated as 1-indexed for user input.
    cols_to_use = parse_columns_options(args.r, args.c, total_columns)
    # Convert them to 0-indexed positions.
    col_indices = [col - 1 for col in cols_to_use]

    # Use a dictionary to track seen keys. We store the first occurrence's column1 value.
    seen_keys = {}
    deduped_rows = []

    # Open deduplicate_list for writing duplicate pairs (each row has two columns).
    with open("deduplicate_list", "w", newline='') as dup_file:
        dup_writer = csv.writer(dup_file)
        # Uncomment the following line if you want to write headers in the duplicate file.
        # dup_writer.writerow(["Original_Row_Column1", "Duplicate_Row_Column1"])
        
        for row in rows:
            # Build the key from the specified columns.
            key = tuple(row[i] if i < len(row) else "" for i in col_indices)
            if key in seen_keys:
                # Key already seen, so this row is a duplicate.
                original_value = seen_keys[key]  # The column1 value of the accepted row.
                duplicate_value = row[0] if len(row) > 0 else ""
                dup_writer.writerow([original_value, duplicate_value])
            else:
                # First time this key is seen: record its column1 value and keep the row.
                seen_keys[key] = row[0] if len(row) > 0 else ""
                deduped_rows.append(row)
    
    # Create output filename by appending "_deduped" before the extension.
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_deduped{ext}"

    with open(output_file, "w", newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(deduped_rows)
    
    print(f"Deduplicated CSV file written to {output_file}")
    print("Duplicate pairs (column1 values) have been written to 'deduplicate_list'.")

if __name__ == "__main__":
    main()
