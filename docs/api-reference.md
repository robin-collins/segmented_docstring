# API Reference

This page provides detailed information about the Segmented Docstring API.

## segmented_docstring.splitter

### `split_file(input_file_path: str, output_directory: str, barecode_extension: str, docstring_extension: str) -> None`

Splits a Python file into separate files for bare code and docstrings.

**Parameters:**
- `input_file_path` (str): Path to the input Python file.
- `output_directory` (str): Directory to save the output files.
- `barecode_extension` (str): File extension for the bare code file.
- `docstring_extension` (str): File extension for the docstring file.

**Raises:**
- `FileReadError`: If there's an error reading the input file.
- `ParseError`: If there's an error parsing the Python source.
- `FileSaveError`: If there's an error saving the output files.

## segmented_docstring.combiner

### `combine_files(barecode_file_path: str, docstring_file_path: str, output_file_path: str) -> None`

Combines bare code and docstring files into a single Python source file.

**Parameters:**
- `barecode_file_path` (str): Path to the file containing the bare code.
- `docstring_file_path` (str): Path to the file containing the docstrings.
- `output_file_path` (str): Path to write the combined output file.

**Raises:**
- `FileReadError`: If there's an error reading the input files.
- `FileSaveError`: If there's an error saving the output file.
- `DocstringMismatchError`: If there's a mismatch between bare code and docstrings.

## segmented_docstring.config

### `read_config(config_path: Path = None) -> Dict[str, Any]`

Reads configuration from a TOML file or returns default values.

**Parameters:**
- `config_path` (Path, optional): Path to the configuration file. Defaults to None.

**Returns:**
- Dict[str, Any]: Configuration dictionary with all settings.

**Raises:**
- `ConfigFileNotFoundError`: If the specified config file is not found.
- `ConfigFileParseError`: If there's an error parsing the config file.

## segmented_docstring.cli

### `main(argv: Optional[List[str]] = None) -> None`

The main entry point for the CLI application.

**Parameters:**
- `argv` (Optional[List[str]]): Command-line arguments. Defaults to None.

This function parses command-line arguments and executes the appropriate actions (split or combine).
