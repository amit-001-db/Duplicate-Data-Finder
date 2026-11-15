import unittest
import os
import tempfile
from io import StringIO
import sys
from unittest.mock import patch

from duplicate_datafinder import find_duplicats


class TestDuplicateDataFinder(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.test_dir.cleanup)

    def _create_file(self, filename: str, content: str) -> str:
        filepath = os.path.join(self.test_dir.name, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def test_tc1_exact_match_with_duplicates(self):
        """TC1: Exact Match (Option 1) correctly identifies duplicates and writes unique items."""
        data = "Apple\nBanana\nApple\nCherry\nBanana\nDate\n"
        input_path = self._create_file("test_data_exact.txt", data)
        output_path = os.path.join(self.test_dir.name, "out_exact.txt")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=1, output_file=output_path)

        output = captured_stdout.getvalue()
        self.assertIn("Total items: 6 | Unique items: 4", output)
        self.assertIn("Duplicates: Apple (2 times) | Banana (2 times)", output)
        self.assertIn(f"Unique list saved to {output_path}", output)

        self.assertTrue(os.path.exists(output_path))
        with open(output_path, "r", encoding="utf-8") as f:
            saved_lines = f.read().splitlines()
        self.assertEqual(saved_lines, ["Apple", "Banana", "Cherry", "Date"])

    def test_tc2_no_duplicates_found(self):
        """TC2: File with all distinct items reports 'No duplicates found.'."""
        data = "Cat\nDog\nElephant\nFox\n"
        input_path = self._create_file("test_data_no_dups.txt", data)
        output_path = os.path.join(self.test_dir.name, "out_no_dups.txt")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=1, output_file=output_path)

        output = captured_stdout.getvalue()
        self.assertIn("Total items: 4 | Unique items: 4", output)
        self.assertIn("No duplicates found.", output)
        self.assertNotIn("Duplicates:", output)

        with open(output_path, "r", encoding="utf-8") as f:
            saved_lines = f.read().splitlines()
        self.assertEqual(saved_lines, ["Cat", "Dog", "Elephant", "Fox"])

    def test_tc3a_file_not_found(self):
        """TC3a: Gracefully handles non-existent file with user-friendly error message."""
        non_existent_path = os.path.join(self.test_dir.name, "non_existent_file.txt")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=non_existent_path, option=1)

        output = captured_stdout.getvalue()
        self.assertIn(f"File '{non_existent_path}' not found. Please enter a valid file name.", output)

    def test_tc3b_empty_file(self):
        """TC3b: Gracefully handles completely empty file."""
        input_path = self._create_file("empty.txt", "")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=1)

        output = captured_stdout.getvalue()
        self.assertIn("File is empty. Nothing to check.", output)

    def test_tc3c_whitespace_only_file(self):
        """TC3c: Handles file containing only whitespace or blank lines."""
        input_path = self._create_file("whitespace.txt", "   \n\t\n  \n")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=1)

        output = captured_stdout.getvalue()
        self.assertIn("File is empty. Nothing to check.", output)

    def test_tc4_ignore_case_and_extra_spaces(self):
        """TC4: Option 2 collapses spaces and normalizes case."""
        data = "Machine Learning\n  machine   learning  \nMACHINE LEARNING\nDeep Learning\n"
        input_path = self._create_file("test_data_option2.txt", data)
        output_path = os.path.join(self.test_dir.name, "out_option2.txt")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=2, output_file=output_path)

        output = captured_stdout.getvalue()
        self.assertIn("Total items: 4 | Unique items: 2", output)
        self.assertIn("Duplicates: machine learning (3 times)", output)

        with open(output_path, "r", encoding="utf-8") as f:
            saved_lines = f.read().splitlines()
        self.assertEqual(saved_lines, ["machine learning", "deep learning"])

    def test_tc5_preserves_first_occurrence_order(self):
        """TC5: Preserves the original order of first occurrence for unique entries."""
        data = "zebra\nlion\nzebra\nantelope\nlion\ngiraffe\n"
        input_path = self._create_file("test_order.txt", data)
        output_path = os.path.join(self.test_dir.name, "out_order.txt")

        captured_stdout = StringIO()
        with patch("sys.stdout", captured_stdout):
            find_duplicats(file_name=input_path, option=1, output_file=output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            saved_lines = f.read().splitlines()
        self.assertEqual(saved_lines, ["zebra", "lion", "antelope", "giraffe"])

    def test_tc6_interactive_input_fallbacks(self):
        """TC6: Interactive mode prompts user and correctly defaults on empty inputs."""
        data = "Alpha\nBeta\nAlpha\n"
        input_path = self._create_file("data.txt", data)
        output_path = os.path.join(self.test_dir.name, "unique.txt")

        # Mock inputs: user presses Enter for filename (defaults to data.txt), and Enter for option (defaults to 1)
        captured_stdout = StringIO()
        with patch("builtins.input", side_effect=["", ""]):
            with patch("sys.stdout", captured_stdout):
                # Run from directory containing default data.txt
                cwd = os.getcwd()
                try:
                    os.chdir(self.test_dir.name)
                    find_duplicats()
                finally:
                    os.chdir(cwd)

        output = captured_stdout.getvalue()
        self.assertIn("Total items: 3 | Unique items: 2", output)
        self.assertIn("Duplicates: Alpha (2 times)", output)


if __name__ == "__main__":
    unittest.main()
