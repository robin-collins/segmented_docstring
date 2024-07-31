"""
splitter.py

This module provides functionality to split Python source files into separate
files containing bare code and docstrings.
"""

import ast
import os
from pathlib import Path
from typing import Dict, Any

from colored_custom_logger import CustomLogger

logger = CustomLogger.get_logger("splitter")

class SplitterError(Exception):
    """Base exception for splitter-related errors."""
    pass

class FileReadError(SplitterError):
    """Raised when there's an error reading the input file."""
    pass

class FileSaveError(SplitterError):
    """Raised when there's an error saving the output files."""
    pass

class ParseError(SplitterError):
    """Raised when there's an error parsing the Python source."""
    pass

def split_file(input_file_path: str, output_directory: str, barecode_extension: str, docstring_extension: str) -> None:
    """
    Split a Python file into separate files for bare code and docstrings.

    Args:
        input_file_path (str): Path to the input Python file.
        output_directory (str): Directory to save the output files.
        barecode_extension (str): File extension for the bare code file.
        docstring_extension (str): File extension for the docstring file.

    Raises:
        FileReadError: If there's an error reading the input file.
        ParseError: If there's an error parsing the Python source.
        FileSaveError: If there's an error saving the output files.
    """
    logger.info("Splitting file: %s", input_file_path)

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            source = file.read()
    except IOError as e:
        logger.error("Error reading input file: %s", e)
        raise FileReadError(f"Error reading input file: {e}") from e

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        logger.error("Error parsing Python source: %s", e)
        raise ParseError(f"Error parsing Python source: {e}") from e
    
    barecode_lines = []
    docstring_lines = []
    
    class DocstringVisitor(ast.NodeVisitor):
        def visit_Module(self, node):
            self._process_node(node, 0)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            self._process_node(node, node.col_offset)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            self._process_node(node, node.col_offset)
            self.generic_visit(node)

        def _process_node(self, node, indent):
            docstring = ast.get_docstring(node)
            if docstring:
                lines = docstring.split('\n')
                docstring_lines.extend([' ' * indent + '"""' + lines[0] + '"""'] + 
                                       [' ' * indent + line for line in lines[1:]])
                docstring_lines.append('')
            else:
                placeholder = f'"""<placeholder> Add docstring for {node.__class__.__name__}"""'
                docstring_lines.append(' ' * indent + placeholder)
                docstring_lines.append('')

    visitor = DocstringVisitor()
    visitor.visit(tree)

    lines = source.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            continue
        if stripped and not stripped.startswith('#'):
            barecode_lines.append(line)
        elif stripped.startswith('#') or not stripped:
            barecode_lines.append(line)

    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    barecode_path = os.path.join(output_directory, f"{base_name}{barecode_extension}")
    docstring_path = os.path.join(output_directory, f"{base_name}{docstring_extension}")

    try:
        with open(barecode_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(barecode_lines))
        logger.info("Bare code saved to: %s", barecode_path)

        # Remove extra indentation for placeholder docstrings
        cleaned_docstring_lines = []
        for line in docstring_lines:
            if line.strip().startswith('"""<placeholder>'):
                cleaned_docstring_lines.append(line.lstrip())
            else:
                cleaned_docstring_lines.append(line)

        with open(docstring_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_docstring_lines))
        logger.info("Docstrings saved to: %s", docstring_path)
    except IOError as e:
        logger.error("Error saving output files: %s", e)
        raise FileSaveError(f"Error saving output files: {e}") from e

    logger.info("File split successfully")

__version__ = "0.1.9"
