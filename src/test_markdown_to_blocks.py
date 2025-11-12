import unittest

from utilityfunctions import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    """Test suite for the markdown_to_blocks function."""

    def test_simple_two_blocks(self):
        """Test splitting two simple blocks separated by double newlines."""
        markdown = "Block 1\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_three_blocks(self):
        """Test splitting three blocks."""
        markdown = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(result, expected)

    def test_excess_newlines_filtered(self):
        """Test that empty blocks from excess newlines are filtered out."""
        markdown = "Block 1\n\n\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_leading_whitespace_stripped(self):
        """Test that leading whitespace is stripped from blocks."""
        markdown = "  Block 1  \n\n  Block 2  "
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_trailing_whitespace_stripped(self):
        """Test that trailing whitespace is stripped from blocks."""
        markdown = "Block 1   \n\nBlock 2   "
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_internal_whitespace_preserved(self):
        """Test that internal whitespace within blocks is preserved."""
        markdown = "Block 1 with spaces\n\nBlock 2 with spaces"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1 with spaces", "Block 2 with spaces"]
        self.assertEqual(result, expected)

    def test_single_block(self):
        """Test with a single block (no double newlines)."""
        markdown = "Just one block"
        result = markdown_to_blocks(markdown)
        expected = ["Just one block"]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """Test with empty string input."""
        markdown = ""
        result = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(result, expected)

    def test_only_whitespace(self):
        """Test with only whitespace."""
        markdown = "   \n\n   "
        result = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(result, expected)

    def test_only_newlines(self):
        """Test with only newlines."""
        markdown = "\n\n\n\n"
        result = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(result, expected)

    def test_single_newline_not_separator(self):
        """Test that single newlines do NOT separate blocks."""
        markdown = "Block 1\nstill block 1\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1\nstill block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_multiline_blocks(self):
        """Test blocks containing multiple lines separated by single newlines."""
        markdown = "Line 1\nLine 2\nLine 3\n\nBlock 2 Line 1\nBlock 2 Line 2"
        result = markdown_to_blocks(markdown)
        expected = ["Line 1\nLine 2\nLine 3", "Block 2 Line 1\nBlock 2 Line 2"]
        self.assertEqual(result, expected)

    def test_tabs_stripped(self):
        """Test that tabs are stripped from block boundaries."""
        markdown = "\tBlock 1\t\n\n\tBlock 2\t"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_mixed_whitespace_stripped(self):
        """Test that mixed whitespace (spaces, tabs, etc.) is stripped."""
        markdown = "  \t  Block 1  \t  \n\n  \t  Block 2  \t  "
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_block_with_special_characters(self):
        """Test that blocks with special characters are handled correctly."""
        markdown = "**Bold** text\n\nCode: `x = 1`"
        result = markdown_to_blocks(markdown)
        expected = ["**Bold** text", "Code: `x = 1`"]
        self.assertEqual(result, expected)

    def test_block_with_links_and_images(self):
        """Test blocks containing markdown links and images."""
        markdown = "[Link](https://example.com)\n\n![Image](url.jpg)"
        result = markdown_to_blocks(markdown)
        expected = ["[Link](https://example.com)", "![Image](url.jpg)"]
        self.assertEqual(result, expected)

    def test_many_blocks(self):
        """Test with many blocks."""
        markdown = "Block 1\n\nBlock 2\n\nBlock 3\n\nBlock 4\n\nBlock 5"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2", "Block 3", "Block 4", "Block 5"]
        self.assertEqual(result, expected)

    def test_blocks_separated_by_many_newlines(self):
        """Test blocks separated by many consecutive newlines."""
        markdown = "Block 1\n\n\n\n\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_trailing_double_newline(self):
        """Test markdown ending with double newline."""
        markdown = "Block 1\n\nBlock 2\n\n"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_leading_double_newline(self):
        """Test markdown starting with double newline."""
        markdown = "\n\nBlock 1\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_leading_and_trailing_newlines(self):
        """Test markdown with leading and trailing newlines."""
        markdown = "\n\n\nBlock 1\n\nBlock 2\n\n\n"
        result = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(result, expected)

    def test_realistic_markdown_document(self):
        """Test with a realistic markdown document."""
        markdown = """# Heading

This is a paragraph with some text.

This is another paragraph.

- Item 1
- Item 2
- Item 3

Final paragraph."""
        result = markdown_to_blocks(markdown)
        expected = [
            "# Heading",
            "This is a paragraph with some text.",
            "This is another paragraph.",
            "- Item 1\n- Item 2\n- Item 3",
            "Final paragraph."
        ]
        self.assertEqual(result, expected)

    def test_code_block_with_newlines(self):
        """Test that code blocks with internal newlines are treated as single block."""
        markdown = "```python\ncode line 1\ncode line 2\n```\n\nNext block"
        result = markdown_to_blocks(markdown)
        expected = ["```python\ncode line 1\ncode line 2\n```", "Next block"]
        self.assertEqual(result, expected)

    def test_unicode_text(self):
        """Test with unicode characters."""
        markdown = "Block with 你好\n\nBloque con español"
        result = markdown_to_blocks(markdown)
        expected = ["Block with 你好", "Bloque con español"]
        self.assertEqual(result, expected)

    def test_block_unchanged_structure(self):
        """Test that block structure within a block is unchanged."""
        markdown = "para1\npara2\npara3\n\nblock2"
        result = markdown_to_blocks(markdown)
        # The first block should have preserved internal newlines
        self.assertEqual(result[0], "para1\npara2\npara3")
        self.assertEqual(result[1], "block2")


if __name__ == "__main__":
    unittest.main()
