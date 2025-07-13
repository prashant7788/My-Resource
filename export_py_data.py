#!/usr/bin/env python3
"""
Python Data Exporter

This script scans a directory for Python (.py) files and extracts information
about their contents (functions, classes, imports, etc.) and exports the data
to a CSV file with columns: name, type, and query.
"""

import ast
import csv
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


class PythonFileAnalyzer:
    """Analyzes Python files and extracts metadata."""
    
    def __init__(self):
        self.data = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Analyze a single Python file and extract metadata.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of dictionaries containing name, type, and query information
        """
        file_data = []
        processed_functions = set()  # Track to avoid duplicates
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file using AST
            tree = ast.parse(content, filename=file_path)
            
            # Extract module-level information
            module_name = Path(file_path).stem
            module_docstring = ast.get_docstring(tree) or "No description"
            
            file_data.append({
                'name': module_name,
                'type': 'module',
                'query': module_docstring.strip(),
                'file_path': file_path
            })
            
            # Process top-level nodes first to avoid duplicates
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    # Extract function information
                    func_name = node.name
                    func_docstring = ast.get_docstring(node) or "No description"
                    
                    # Get function signature
                    args = [arg.arg for arg in node.args.args]
                    signature = f"{func_name}({', '.join(args)})"
                    
                    if signature not in processed_functions:
                        file_data.append({
                            'name': signature,
                            'type': 'function',
                            'query': func_docstring.strip(),
                            'file_path': file_path
                        })
                        processed_functions.add(signature)
                
                elif isinstance(node, ast.ClassDef):
                    # Extract class information
                    class_name = node.name
                    class_docstring = ast.get_docstring(node) or "No description"
                    
                    file_data.append({
                        'name': class_name,
                        'type': 'class',
                        'query': class_docstring.strip(),
                        'file_path': file_path
                    })
                    
                    # Extract methods from the class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_name = item.name
                            method_docstring = ast.get_docstring(item) or "No description"
                            
                            # Get method signature
                            args = [arg.arg for arg in item.args.args]
                            method_signature = f"{class_name}.{method_name}({', '.join(args)})"
                            
                            file_data.append({
                                'name': method_signature,
                                'type': 'method',
                                'query': method_docstring.strip(),
                                'file_path': file_path
                            })
                
                elif isinstance(node, ast.Import):
                    # Extract import statements
                    for alias in node.names:
                        import_name = alias.name
                        file_data.append({
                            'name': import_name,
                            'type': 'import',
                            'query': f"import {import_name}",
                            'file_path': file_path
                        })
                
                elif isinstance(node, ast.ImportFrom):
                    # Extract from-import statements
                    module = node.module or ''
                    for alias in node.names:
                        import_name = alias.name
                        query = f"from {module} import {import_name}" if module else f"from . import {import_name}"
                        file_data.append({
                            'name': f"{module}.{import_name}" if module else import_name,
                            'type': 'import_from',
                            'query': query,
                            'file_path': file_path
                        })
        
        except UnicodeDecodeError as e:
            # Handle encoding issues
            file_data.append({
                'name': Path(file_path).stem,
                'type': 'error',
                'query': f"File encoding error: {str(e)}",
                'file_path': file_path
            })
        except SyntaxError as e:
            # Handle syntax errors in Python files
            file_data.append({
                'name': Path(file_path).stem,
                'type': 'error',
                'query': f"Syntax error: {str(e)}",
                'file_path': file_path
            })
        except Exception as e:
            # Handle other parsing errors
            file_data.append({
                'name': Path(file_path).stem,
                'type': 'error',
                'query': f"Failed to parse file: {str(e)}",
                'file_path': file_path
            })
        
        return file_data
    
    def scan_directory(self, directory: str) -> List[Dict[str, str]]:
        """
        Scan a directory for Python files and analyze them.
        
        Args:
            directory: Path to the directory to scan
            
        Returns:
            List of dictionaries containing extracted data
        """
        all_data = []
        
        # Find all Python files in the directory and subdirectories
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    print(f"Analyzing: {file_path}")
                    file_data = self.analyze_file(file_path)
                    all_data.extend(file_data)
        
        return all_data
    
    def export_to_csv(self, data: List[Dict[str, str]], output_file: str):
        """
        Export the extracted data to a CSV file.
        
        Args:
            data: List of dictionaries containing the data
            output_file: Path to the output CSV file
        """
        if not data:
            print("No data to export.")
            return
        
        # Define CSV headers
        headers = ['name', 'type', 'query']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            for row in data:
                # Only write the required columns to CSV
                csv_row = {
                    'name': row['name'],
                    'type': row['type'],
                    'query': row['query']
                }
                writer.writerow(csv_row)
        
        print(f"Data exported to: {output_file}")
        print(f"Total entries: {len(data)}")


def main():
    """Main function to handle command-line arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description="Export data from Python files in a directory to CSV format"
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan for Python files (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        default='python_data_export.csv',
        help='Output CSV file name (default: python_data_export.csv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)
    
    print(f"Scanning directory: {os.path.abspath(args.directory)}")
    print(f"Output file: {args.output}")
    print("-" * 50)
    
    # Create analyzer and process files
    analyzer = PythonFileAnalyzer()
    data = analyzer.scan_directory(args.directory)
    
    if data:
        analyzer.export_to_csv(data, args.output)
        
        if args.verbose:
            print("\nExtracted data summary:")
            type_counts = {}
            for item in data:
                item_type = item['type']
                type_counts[item_type] = type_counts.get(item_type, 0) + 1
            
            for item_type, count in sorted(type_counts.items()):
                print(f"  {item_type}: {count}")
    else:
        print("No Python files found or no data extracted.")


if __name__ == '__main__':
    main()