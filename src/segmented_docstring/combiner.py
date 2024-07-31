"""
combiner.py

This module provides functionality for combining bare code and docstring files
back into a single Python source file.

Version: 1.1.0
"""

import ast
from pathlib import Path
from typing import Dict, Any
from colored_custom_logger import CustomLogger

logger = CustomLogger.get_logger("combiner")

class CombinerError(Exception):
    """Base exception for combiner-related errors."""
    pass

class FileReadError(CombinerError):
    """Raised when there's an error reading input files."""
    pass

class FileSaveError(CombinerError):
    """Raised when there's an error saving the output file."""
    pass

class DocstringMismatchError(CombinerError):
    """Raised when there's a mismatch between bare code and docstrings."""
    pass

def combine_files(barecode_file_path: str, docstring_file_path: str, output_file_path: str) -> None:
    """
    Combine bare code and docstring files into a single Python source file.

    This function reads the bare code and docstring files, merges the docstrings
    back into the bare code while preserving the original structure and formatting,
    and writes the combined content to the output file.

    Args:
        barecode_file_path (str): Path to the file containing the bare code.
        docstring_file_path (str): Path to the file containing the docstrings.
        output_file_path (str): Path to write the combined output file.

    Raises:
        FileReadError: If there's an error reading the input files.
        FileSaveError: If there's an error saving the output file.
        DocstringMismatchError: If there's a mismatch between bare code and docstrings.
    """
    logger.info("Combining files: %s and %s", barecode_file_path, docstring_file_path)

    try:
        with open(barecode_file_path, 'r', encoding='utf-8') as bare_file:
            bare_code = bare_file.read()
        logger.debug("Bare code file read successfully")

        with open(docstring_file_path, 'r', encoding='utf-8') as docstring_file:
            docstrings = ast.literal_eval(docstring_file.read())
        logger.debug("Docstring file read successfully")
    except IOError as e:
        logger.error("Error reading input files: %s", e)
        raise FileReadError(f"Error reading input files: {e}") from e
    except SyntaxError as e:
        logger.error("Error parsing docstring file: %s", e)
        raise FileReadError(f"Error parsing docstring file: {e}") from e

    try:
        combined_code = _merge_docstrings(bare_code, docstrings)
    except DocstringMismatchError as e:
        logger.error("Error merging docstrings: %s", e)
        raise

    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(combined_code)
        logger.info("Combined code saved to: %s", output_file_path)
    except IOError as e:
        logger.error("Error saving output file: %s", e)
        raise FileSaveError(f"Error saving output file: {e}") from e

    logger.info("Files combined successfully")

def _merge_docstrings(bare_code: str, docstrings: Dict[str, Any]) -> str:
    """
    Merge docstrings back into the bare code.

    This function takes the bare code and a dictionary of docstrings, and
    inserts the docstrings back into their original positions in the code.

    Args:
        bare_code (str): The bare code without docstrings.
        docstrings (Dict[str, Any]): A dictionary containing docstrings.

    Returns:
        str: The combined code with docstrings inserted.

    Raises:
        DocstringMismatchError: If there's a mismatch between bare code and docstrings.
    """
    logger.debug("Merging docstrings into bare code")

    output_lines = []

    # Insert module docstring if present
    if 'module' in docstrings:
        output_lines.append(f'"""{docstrings["module"]}"""')
        output_lines.append('')  # Add an extra newline after the module docstring
        logger.debug("Module docstring inserted")

    lines = bare_code.splitlines()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('def ', 'class ')):
            name = stripped.split()[1].split('(')[0].strip(':')
            indent = len(line) - len(line.lstrip())
            output_lines.append(line)
            if name in docstrings:
                docstring = docstrings[name].strip()
                formatted_docstring = f'{" " * (indent + 4)}"""{docstring}"""'
                output_lines.append(formatted_docstring)
                logger.debug("Docstring inserted for: %s", name)
            else:
                logger.warning("Docstring not found for: %s", name)
        else:
            output_lines.append(line)

    # Join lines and ensure only one newline at the end
    combined_code = '\n'.join(output_lines).rstrip() + '\n'
    logger.debug("Docstrings merged successfully")
    return combined_code

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        logger.error("Usage: python combiner.py <barecode_file> <docstring_file> <output_file>")
        sys.exit(1)
    try:
        combine_files(sys.argv[1], sys.argv[2], sys.argv[3])
    except CombinerError as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)

__version__ = "0.1.8"
