# tests/test_splitter.py

import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys
from os.path import abspath, dirname, join

# Add the src directory to the Python path
sys.path.insert(0, abspath(join(dirname(__file__), '..', 'src')))

from segmented_docstring.splitter import split_file, FileReadError, FileSaveError, ParseError

class TestSplitter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "test_input.py")
        self.barecode_ext = ".bare.py"
        self.docstring_ext = ".doc.py"

    def tearDown(self):
        # Use shutil.rmtree to remove the temporary directory and all its contents
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_split_file_with_docstrings(self):
        input_content = '''"""Module docstring."""

def func():
    """Function docstring."""
    pass

class TestClass:
    """Class docstring."""
    
    def method(self):
        """Method docstring."""
        return True
'''
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write(input_content)

        split_file(self.input_file, self.temp_dir, self.barecode_ext, self.docstring_ext)

        with open(os.path.join(self.temp_dir, "test_input" + self.barecode_ext), 'r', encoding='utf-8') as f:
            barecode = f.read()
        with open(os.path.join(self.temp_dir, "test_input" + self.docstring_ext), 'r', encoding='utf-8') as f:
            docstrings = f.read()

        expected_barecode = '''
def func():
    pass

class TestClass:
    
    def method(self):
        return True
'''
        expected_docstrings = '''"""Module docstring."""

"""Function docstring."""

"""Class docstring."""

    """Method docstring."""
'''
        self.assertEqual(barecode.strip(), expected_barecode.strip())
        self.assertEqual(docstrings.strip(), expected_docstrings.strip())

    def test_split_file_input_not_found(self):
        non_existent_file = os.path.join(self.temp_dir, "non_existent.py")
        with self.assertRaises(FileReadError):
            split_file(non_existent_file, self.temp_dir, self.barecode_ext, self.docstring_ext)

    def test_split_file_invalid_python(self):
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write("This is not valid Python code")

        with self.assertRaises(ParseError):
            split_file(self.input_file, self.temp_dir, self.barecode_ext, self.docstring_ext)

    def test_split_file_output_permission_error(self):
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write("print('Hello, World!')")

        # Create a directory with the same name as the output file to simulate a permission error
        os.mkdir(os.path.join(self.temp_dir, "test_input" + self.barecode_ext))

        with self.assertRaises(FileSaveError):
            split_file(self.input_file, self.temp_dir, self.barecode_ext, self.docstring_ext)

if __name__ == '__main__':
    unittest.main()
