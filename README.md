# CSV Deduplicator Extension

A VSCode extension to deduplicate CSV files using the `csvdeduplicator.py` script.

## Features
- **Deduplicate CSV**: Remove duplicate rows based on user-specified columns.
- **List Headers**: Display column indices and headers for the active CSV file.

## Requirements
- Python 3 installed and available on PATH.

## Usage
1. Open a CSV file in VSCode.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Run `CSV Deduplicator: Deduplicate CSV` to remove duplicates.
   - You will be prompted to enter a column specifier (`-r`) or press Enter to skip.
   - Then prompted to enter a count of columns (`-c`) or press Enter to skip.
   - The extension will run the script and open the deduplicated file alongside the duplicate list.
4. Run `CSV Deduplicator: List Headers` to view header indices.

## Contributing
1. Clone the repository.
2. Run `npm install`.
3. Press `F5` to launch a development host.

## Release Notes
See [CHANGELOG.md](CHANGELOG.md) for more details.
