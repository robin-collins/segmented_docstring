"""
test_combiner.py

This module contains unit tests for the combine_files function in the combiner module.
"""
import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys
from os.path import abspath, dirname, join

# Add the src directory to the Python path
sys.path.insert(0, abspath(join(dirname(__file__), '..', 'src')))

from segmented_docstring.combiner import combine_files, FileReadError, FileSaveError, DocstringMismatchError

class TestCombiner(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.barecode_file = os.path.join(self.temp_dir, "test_input.bare.py")
        self.docstring_file = os.path.join(self.temp_dir, "test_input.doc.py")
        self.output_file = os.path.join(self.temp_dir, "test_output.py")

    def tearDown(self):
        # Use shutil.rmtree to remove the temporary directory and all its contents
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_combine_files_with_docstrings(self):
        barecode_content = '''def func():
    pass

class TestClass:
    
    def method(self):
        return True'''
        docstring_content = '''{"module": "Module docstring.", "func": "Function docstring.", "TestClass": "Class docstring.", "method": "Method docstring."}'''

        with open(self.barecode_file, 'w', encoding='utf-8') as f:
            f.write(barecode_content)
        with open(self.docstring_file, 'w', encoding='utf-8') as f:
            f.write(docstring_content)

        combine_files(self.barecode_file, self.docstring_file, self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as f:
            combined_content = f.read()

        expected_content = '''"""Module docstring."""

def func():
    """Function docstring."""
    pass

class TestClass:
    """Class docstring."""
    
    def method(self):
        """Method docstring."""
        return True
'''
        self.assertEqual(combined_content, expected_content)

    def test_combine_files_input_not_found(self):
        non_existent_file = os.path.join(self.temp_dir, "non_existent.py")
        with self.assertRaises(FileReadError):
            combine_files(non_existent_file, self.docstring_file, self.output_file)

    def test_combine_files_invalid_docstring_file(self):
        with open(self.barecode_file, 'w', encoding='utf-8') as f:
            f.write("def func():\n    pass")
        with open(self.docstring_file, 'w', encoding='utf-8') as f:
            f.write("This is not a valid Python dictionary")

        with self.assertRaises(FileReadError):
            combine_files(self.barecode_file, self.docstring_file, self.output_file)

    def test_combine_files_output_permission_error(self):
        with open(self.barecode_file, 'w', encoding='utf-8') as f:
            f.write("def func():\n    pass")
        with open(self.docstring_file, 'w', encoding='utf-8') as f:
            f.write('{"func": "Function docstring."}')

        # Create a directory with the same name as the output file to simulate a permission error
        os.mkdir(self.output_file)

        with self.assertRaises(FileSaveError):
            combine_files(self.barecode_file, self.docstring_file, self.output_file)

    def test_combine_files_docstring_mismatch(self):
        with open(self.barecode_file, 'w', encoding='utf-8') as f:
            f.write("def func():\n    pass")
        with open(self.docstring_file, 'w', encoding='utf-8') as f:
            f.write('{"other_func": "Docstring for non-existent function."}')

        combine_files(self.barecode_file, self.docstring_file, self.output_file)
        
        # The combination should succeed, but a warning should be logged


if __name__ == '__main__':
    unittest.main()
