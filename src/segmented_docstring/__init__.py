"""
segmented_docstring module

This module provides functionality for splitting Python source files
into separate files containing bare code and docstrings, and combining
them back into a single file.
"""

from .splitter import split_file
from .combiner import combine_files
from .cli import main as cli_main

__all__ = ['split_file', 'combine_files', 'cli_main']
__version__ = '0.4.33'
