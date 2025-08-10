import unittest

from generatepage import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_error(self):
        markdown = """
no title
"""
        self.assertRaises(ValueError, lambda: extract_title(markdown))

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

* and
* a
* list
"""
        )
        self.assertEqual(actual, "title")


if __name__ == "__main__":
    unittest.main()
