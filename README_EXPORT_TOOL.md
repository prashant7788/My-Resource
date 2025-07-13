# Python Data Exporter

This script scans a directory for Python (.py) files and extracts information about their contents (functions, classes, imports, etc.) and exports the data to a CSV file with columns: name, type, and query.

## Usage

### Basic Usage
```bash
# Scan current directory and export to default CSV file
python export_py_data.py

# Scan a specific directory
python export_py_data.py /path/to/directory

# Specify output file
python export_py_data.py /path/to/directory -o output.csv

# Enable verbose output
python export_py_data.py /path/to/directory --verbose
```

### Command Line Options
- `directory`: Directory to scan for Python files (default: current directory)
- `-o, --output`: Output CSV file name (default: python_data_export.csv)
- `--verbose`: Enable verbose output showing extraction summary

## Output Format

The script generates a CSV file with the following columns:
- **name**: The name of the element (module, function, class, method, or import)
- **type**: The type of element (module, function, class, method, import, import_from, error)
- **query**: Description or docstring of the element

### Types Extracted
- **module**: Python file/module with its docstring
- **function**: Top-level functions with their signatures and docstrings
- **class**: Class definitions with their docstrings
- **method**: Class methods with their signatures and docstrings
- **import**: Import statements (e.g., `import os`)
- **import_from**: From-import statements (e.g., `from typing import List`)
- **error**: Files that couldn't be parsed with error details

## Examples

### Example 1: Analyzing a project directory
```bash
python export_py_data.py my_project/ -o project_analysis.csv --verbose
```

### Example 2: Quick analysis of sample scripts
```bash
python export_py_data.py sample_scripts/
```

## Requirements
- Python 3.6 or higher
- Standard library modules: ast, csv, os, sys, argparse, pathlib, typing

## Error Handling
The script gracefully handles:
- Files with encoding issues
- Python files with syntax errors
- Files that cannot be parsed for other reasons
- Missing directories

Error entries are included in the output with type "error" and details in the query column.