"""
cli.py

This module implements the command-line interface for the segmented_docstring package.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from colored_custom_logger import CustomLogger
from .splitter import split_file, SplitterError
from .combiner import combine_files, CombinerError
from .config import read_config, ConfigError

logger = CustomLogger.get_logger("cli")

class CLIError(Exception):
    """Base exception for CLI-related errors."""
    pass

def create_parser() -> argparse.ArgumentParser:
    """
    Create and return the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Segmented Docstring CLI")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Common arguments for all subcommands
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-o', '--output', type=str, help="Output directory")
    common_parser.add_argument('-r', '--recursive', action='store_true', help="Process directories recursively")
    common_parser.add_argument('--dry-run', action='store_true', help="Perform a dry run without making changes")

    # Split command
    split_parser = subparsers.add_parser('split', help="Split Python files into bare code and docstrings", parents=[common_parser])
    split_parser.add_argument('source', type=str, help="Source file or directory")

    # Combine command
    combine_parser = subparsers.add_parser('combine', help="Combine bare code and docstring files", parents=[common_parser])
    combine_parser.add_argument('source', type=str, help="Source directory containing bare code and docstring files")

    return parser

def main(argv: Optional[List[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    
    try:
        config = read_config()
    except ConfigError as e:
        logger.error("Configuration error: %s", e)
        sys.exit(1)

    if args.verbose:
        logger.setLevel("DEBUG")
        print("Verbose mode enabled")  # Keep this print statement for backward compatibility
        logger.debug("Verbose mode enabled")
        logger.debug("Configuration: %s", config)

    try:
        if args.command == 'split':
            process_split(args, config)
        elif args.command == 'combine':
            process_combine(args, config)
    except CLIError as e:
        print(f"Error: {e}", file=sys.stderr)  # Print to stderr for backward compatibility
        logger.error("CLI error: %s", e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)  # Print to stderr for backward compatibility
        logger.error("An unexpected error occurred: %s", e)
        sys.exit(1)

def process_split(args: argparse.Namespace, config: dict) -> None:
    """
    Process the split command.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        config (dict): Configuration dictionary.

    Raises:
        CLIError: If there's an error processing the split command.
    """
    source = Path(args.source)
    output = Path(args.output) if args.output else Path(config['output_folder'])
    
    if source.is_file():
        logger.info("Splitting file: %s", source)
        if not args.dry_run:
            try:
                split_file(str(source), str(output), config['barecode_extension'], config['docstring_extension'])
            except SplitterError as e:
                raise CLIError(f"Error splitting file {source}: {e}")
    elif source.is_dir():
        if args.recursive:
            files = source.rglob('*.py')
        else:
            files = source.glob('*.py')
        
        for python_file in files:
            logger.info("Splitting file: %s", python_file)
            if not args.dry_run:
                try:
                    split_file(str(python_file), str(output), config['barecode_extension'], config['docstring_extension'])
                except SplitterError as e:
                    logger.error("Error splitting file %s: %s", python_file, e)
    else:
        raise CLIError(f"Error: {source} is not a valid file or directory")

def process_combine(args: argparse.Namespace, config: dict) -> None:
    """
    Process the combine command.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        config (dict): Configuration dictionary.

    Raises:
        CLIError: If there's an error processing the combine command.
    """
    source = Path(args.source)
    output = Path(args.output) if args.output else Path(config['output_folder'])
    
    if not source.is_dir():
        raise CLIError(f"Error: {source} is not a valid directory")

    def combine_pair(barecode_file: Path, docstring_file: Path) -> None:
        logger.info("Combining files: %s and %s", barecode_file, docstring_file)
        if not args.dry_run:
            output_file = output / barecode_file.with_suffix('.py').name
            try:
                combine_files(str(barecode_file), str(docstring_file), str(output_file))
            except CombinerError as e:
                logger.error("Error combining files %s and %s: %s", barecode_file, docstring_file, e)

    if args.recursive:
        barecode_files = source.rglob(f"*{config['barecode_extension']}")
    else:
        barecode_files = source.glob(f"*{config['barecode_extension']}")

    for barecode_file in barecode_files:
        docstring_file = barecode_file.with_suffix(config['docstring_extension'])
        if docstring_file.exists():
            combine_pair(barecode_file, docstring_file)
        else:
            logger.warning("Docstring file not found for: %s", barecode_file)

def entry_point():
    """
    Entry point for the command-line interface.
    This function is called when the package is run as a script.
    """
    main(sys.argv[1:])

if __name__ == '__main__':
    entry_point()

__version__ = '0.1.8'
