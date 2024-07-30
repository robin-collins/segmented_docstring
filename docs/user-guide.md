

## Advanced Usage

### Recursive Processing

To process all Python files in a directory and its subdirectories:

```bash
segmented-docstring split path/to/directory -r
```

### Custom Output Directory

Specify a custom output directory:

```bash
segmented-docstring split path/to/your_file.py -o path/to/output
```

### Dry Run

Perform a dry run to see what would happen without making any changes:

```bash
segmented-docstring split path/to/your_file.py --dry-run
```

## Configuration

Segmented Docstring can be configured using a `.segmentedrc` file in your project root. Here's an example configuration:

```toml
[segmented_docstring]
source_folder = "src"
output_folder = "output"
barecode_extension = ".code.py"
docstring_extension = ".docs.py"
recursion = true
dry_run = false
```

## Best Practices

1. **Version Control**: Always commit your changes before splitting or combining files.
2. **Consistent Usage**: Use Segmented Docstring consistently across your project for best results.
3. **Documentation**: Keep your docstrings up-to-date and in sync with your code.
4. **Backup**: Regularly backup your project, especially when using tools that modify your files.

## Troubleshooting

If you encounter any issues:

1. Ensure you're using the latest version of Segmented Docstring.
2. Check your configuration file for any errors.
3. Use the `--verbose` flag for more detailed output.
4. If the problem persists, please [open an issue](https://github.com/robin-collins/segmented_docstring/issues) on our GitHub repository.

For more detailed information about the API, please refer to our [API Reference](api-reference.md).