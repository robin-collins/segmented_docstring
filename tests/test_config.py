# tests/test_config.py

import unittest
from pathlib import Path
import tempfile
import os
import sys
from os.path import abspath, dirname, join

# Add the src directory to the Python path
sys.path.insert(0, abspath(join(dirname(__file__), '..', 'src')))

from segmented_docstring.config import read_config, ConfigFileNotFoundError, ConfigFileParseError

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / '.segmentedrc'

    def tearDown(self):
        if self.config_path.exists():
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    def test_read_config_default_values(self):
        config = read_config()
        self.assertEqual(config['source_folder'], 'segmented_src')
        self.assertEqual(config['output_folder'], 'src')
        self.assertEqual(config['barecode_extension'], '.barecode.py')
        self.assertEqual(config['docstring_extension'], '.docstring.py')
        self.assertTrue(config['recursion'])
        self.assertFalse(config['dry_run'])

    def test_read_config_custom_values(self):
        with open(self.config_path, 'w') as f:
            f.write("""
[segmented_docstring]
source_folder = "custom_src"
output_folder = "custom_out"
barecode_extension = ".bare.py"
docstring_extension = ".doc.py"
recursion = false
dry_run = true
            """)

        config = read_config(config_path=self.config_path)
        self.assertEqual(config['source_folder'], 'custom_src')
        self.assertEqual(config['output_folder'], 'custom_out')
        self.assertEqual(config['barecode_extension'], '.bare.py')
        self.assertEqual(config['docstring_extension'], '.doc.py')
        self.assertFalse(config['recursion'])
        self.assertTrue(config['dry_run'])

    def test_read_config_partial_custom_values(self):
        with open(self.config_path, 'w') as f:
            f.write("""
[segmented_docstring]
source_folder = "partial_src"
recursion = false
            """)

        config = read_config(config_path=self.config_path)
        self.assertEqual(config['source_folder'], 'partial_src')
        self.assertEqual(config['output_folder'], 'src')  # Default value
        self.assertEqual(config['barecode_extension'], '.barecode.py')  # Default value
        self.assertEqual(config['docstring_extension'], '.docstring.py')  # Default value
        self.assertFalse(config['recursion'])
        self.assertFalse(config['dry_run'])  # Default value

    def test_read_config_file_not_found(self):
        non_existent_path = Path(self.temp_dir) / 'non_existent.toml'
        config = read_config(config_path=non_existent_path)
        # Should return default config without raising an exception
        self.assertEqual(config['source_folder'], 'segmented_src')

    def test_read_config_parse_error(self):
        with open(self.config_path, 'w') as f:
            f.write("""
[segmented_docstring
invalid_toml = true
            """)

        with self.assertRaises(ConfigFileParseError):
            read_config(config_path=self.config_path)

if __name__ == '__main__':
    unittest.main()
