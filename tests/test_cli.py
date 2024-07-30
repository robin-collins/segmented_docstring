"""
test_cli.py

This module contains unit tests for the CLI functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
from io import StringIO

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from segmented_docstring.cli import main
from segmented_docstring.config import DEFAULT_CONFIG

class TestCLI(unittest.TestCase):
    @patch('segmented_docstring.cli.split_file')
    @patch('segmented_docstring.cli.Path.is_file')
    @patch('segmented_docstring.cli.read_config')
    def test_split_single_file(self, mock_read_config, mock_is_file, mock_split_file):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_file.return_value = True
        main(['split', 'test.py'])
        mock_split_file.assert_called_once()

    @patch('segmented_docstring.cli.split_file')
    @patch('segmented_docstring.cli.Path.is_dir')
    @patch('segmented_docstring.cli.Path.glob')
    @patch('segmented_docstring.cli.read_config')
    def test_split_directory(self, mock_read_config, mock_glob, mock_is_dir, mock_split_file):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_dir.return_value = True
        mock_glob.return_value = [Path('test1.py'), Path('test2.py')]
        main(['split', 'testdir'])
        self.assertEqual(mock_split_file.call_count, 2)

    @patch('segmented_docstring.cli.split_file')
    @patch('segmented_docstring.cli.Path.is_dir')
    @patch('segmented_docstring.cli.Path.rglob')
    @patch('segmented_docstring.cli.read_config')
    def test_split_recursive(self, mock_read_config, mock_rglob, mock_is_dir, mock_split_file):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_dir.return_value = True
        mock_rglob.return_value = [Path('test1.py'), Path('subdir/test2.py')]
        main(['split', 'testdir', '-r'])
        self.assertEqual(mock_split_file.call_count, 2)

    @patch('segmented_docstring.cli.combine_files')
    @patch('segmented_docstring.cli.Path.is_dir')
    @patch('segmented_docstring.cli.Path.glob')
    @patch('segmented_docstring.cli.read_config')
    def test_combine(self, mock_read_config, mock_glob, mock_is_dir, mock_combine_files):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_dir.return_value = True
        mock_glob.return_value = [Path('test.barecode.py')]
        with patch('segmented_docstring.cli.Path.exists', return_value=True):
            main(['combine', 'testdir'])
        mock_combine_files.assert_called_once()

    @patch('sys.stderr', new_callable=StringIO)
    @patch('segmented_docstring.cli.Path.is_file')
    @patch('segmented_docstring.cli.Path.is_dir')
    @patch('segmented_docstring.cli.read_config')
    def test_invalid_source(self, mock_read_config, mock_is_dir, mock_is_file, mock_stderr):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_file.return_value = False
        mock_is_dir.return_value = False
        with self.assertRaises(SystemExit):
            main(['split', 'nonexistent.py'])
        self.assertIn("Error:", mock_stderr.getvalue())

    @patch('segmented_docstring.cli.split_file')
    @patch('segmented_docstring.cli.Path.is_file')
    @patch('segmented_docstring.cli.read_config')
    def test_dry_run(self, mock_read_config, mock_is_file, mock_split_file):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_file.return_value = True
        main(['split', 'test.py', '--dry-run'])
        mock_split_file.assert_not_called()

    @patch('builtins.print')
    @patch('segmented_docstring.cli.split_file')
    @patch('segmented_docstring.cli.Path.is_file')
    @patch('segmented_docstring.cli.read_config')
    def test_verbose_mode(self, mock_read_config, mock_is_file, mock_split_file, mock_print):
        mock_read_config.return_value = DEFAULT_CONFIG
        mock_is_file.return_value = True
        main(['-v', 'split', 'test.py'])
        mock_print.assert_any_call("Verbose mode enabled")

if __name__ == '__main__':
    unittest.main()
