import unittest
from io import StringIO
import sys
from sed import process_sed

class TestSed(unittest.TestCase):
    
    def setUp(self):
        # Redirect stdout to capture print outputs
        self.held, sys.stdout = sys.stdout, StringIO()
    
    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held
    
    def test_substitution(self):
        # Test case for substitution
        input_data = "The date is Jun 10."
        expected_output = "The date is DATE."
        result = process_sed("s/Jun [0-9][0-9]/DATE/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)
    
    def test_deletion(self):
        # Test case for deletion
        input_data = "Please remove this line.\nKeep this line."
        expected_output = "Keep this line."
        result = process_sed("d/remove/", input_data, is_file=False)
        self.assertEqual(result, expected_output)
    
    def test_insertion(self):
        # Test case for insertion
        input_data = "Match this line with regex."
        expected_output = "Inserted text\nMatch this line with regex."
        result = process_sed("i/regex/Inserted text/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_append(self):
        # Test case for append
        input_data = "Append this line with text."
        expected_output = "Append this line with text.additional text\n"
        result = process_sed("a/text/additional text/", input_data, is_file=False)
        self.assertEqual(result, expected_output)
    
    def test_print(self):
        # Test case for print
        input_data = "The quick brown fox.\nJumps over the lazy dog."
        expected_output = "The quick brown fox.\n"
        result = process_sed("p/quick/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_substitution_file(self):
        # Test case for substitution in a file
        input_data = """The quick brown fox jumps over the lazy dog.
Python is a versatile programming language.
Regular expressions can be tricky to master.
Text manipulation is a common task in scripting.
Efficient code can save a lot of time.
Debugging is an essential skill for developers."""
        expected_output = """The quick brown fox jumps over the lazy dog.
Java is a versatile programming language.
Regular expressions can be tricky to master.
Text manipulation is a common task in scripting.
Efficient code can save a lot of time.
Debugging is an essential skill for developers."""
        result = process_sed("s/Python/Java/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_deletion_file(self):
        # Test case for deletion in a file
        input_data = """Please remove this line.
Keep this line."""
        expected_output = "Keep this line."
        result = process_sed("d/remove/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_insertion_file(self):
        # Test case for insertion in a file
        input_data = "Match this line with regex."
        expected_output = "Inserted text\nMatch this line with regex."
        result = process_sed("i/regex/Inserted text/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_append_file(self):
        # Test case for appending in a file
        input_data = "This line ends with pattern."
        expected_output = "This line ends with pattern.Append this line\n"
        result = process_sed("a/pattern/Append this line/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_print_file(self):
        # Test case for printing in a file
        input_data = """The quick brown fox jumps over the lazy dog.
Python is a versatile programming language."""
        expected_output = "The quick brown fox jumps over the lazy dog.\n"
        result = process_sed("p/quick/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_multiple_substitutions(self):
        # Test case for multiple substitutions
        input_data = "I love Python.\nPython is great."
        expected_output = "I love Java.\nJava is great."
        result = process_sed("s/Python/Java/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_substitution_and_deletion(self):
        # Test case for substitution and deletion
        input_data = "Remove this line.\nKeep this line.\nSubstitute this."
        expected_output = "Keep this line.\nChanged this."
        result = process_sed("d/Remove/;s/Substitute/Changed/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_append_and_insertion(self):
        # Test case for append and insertion
        input_data = "Line to match."
        expected_output = "Inserted text\nLine to match.additional text\n"
        result = process_sed("i/match/Inserted text/;a/match/additional text/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_print_and_substitution(self):
        # Test case for print and substitution
        input_data = "Print this line.\nChange this line."
        expected_output = "Print this line.\nChanged this line."
        result = process_sed("p/Print/;s/Change/Changed/g", input_data, is_file=False)
        self.assertEqual(result, "Print this line.\n")

    def test_multiple_commands(self):
        # Test case for multiple commands
        input_data = "Line one.\nLine two.\nLine three."
        expected_output = "Line one.\nAdded Line.\nInserted line\nLine two.\nLine three."
        result = process_sed("a/one/Added Line./;i/two/Inserted line/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_multiple_print(self):
        # Test case for multiple print commands
        input_data = "First line.\nSecond line.\nThird line."
        expected_output = "First line.\n"
        result = process_sed("p/First/;p/Third/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_complex_substitution(self):
        # Test case for complex substitution
        input_data = "This is a test.\nTesting 123."
        expected_output = "This is a test.\nChanged 123."
        result = process_sed("s/Testing/Changed/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_substitution_no_match(self):
        # Test case for substitution with no match
        input_data = "No match here."
        expected_output = "No match here."
        result = process_sed("s/NotHere/Changed/g", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_deletion_no_match(self):
        # Test case for deletion with no match
        input_data = "This line stays."
        expected_output = "This line stays."
        result = process_sed("d/NotHere/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

    def test_append_no_match(self):
        # Test case for append with no match
        input_data = "Nothing to append."
        expected_output = "Nothing to append."
        result = process_sed("a/NotHere/Additional text/", input_data, is_file=False)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
