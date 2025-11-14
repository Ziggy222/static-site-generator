import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    """Test suite for the extract_title function."""

    def test_simple_h1_title(self):
        """Test extraction of simple H1 title."""
        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_h1_with_trailing_whitespace(self):
        """Test H1 title with trailing whitespace."""
        markdown = "# My Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_h1_with_leading_whitespace(self):
        """Test H1 title with leading whitespace."""
        markdown = "   # My Title"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_h1_with_both_leading_and_trailing_whitespace(self):
        """Test H1 title with both leading and trailing whitespace."""
        markdown = "   # My Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_h1_title_with_content_after(self):
        """Test H1 title with content following."""
        markdown = "# My Title\n\nThis is a paragraph"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_h1_title_with_multiple_blocks(self):
        """Test H1 title in document with multiple blocks."""
        markdown = "# Main Title\n\n## Subtitle\n\nSome content"
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")

    def test_h1_with_special_characters(self):
        """Test H1 title with special characters."""
        markdown = "# Title with **bold** and _italic_"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with **bold** and _italic_")

    def test_h1_with_symbols(self):
        """Test H1 title with symbols."""
        markdown = "# Hello! World? @#$"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello! World? @#$")

    def test_h1_title_returns_string(self):
        """Test that return value is a string."""
        markdown = "# Title"
        result = extract_title(markdown)
        self.assertIsInstance(result, str)

    def test_no_h1_raises_exception(self):
        """Test that exception is raised when no H1 found."""
        markdown = "## H2 Title\n\nParagraph"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_h1_in_empty_markdown(self):
        """Test exception when markdown is empty."""
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_h1_with_only_paragraphs(self):
        """Test exception when only paragraphs exist."""
        markdown = "Just a paragraph\n\nAnother paragraph"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_h1_with_only_lists(self):
        """Test exception when only lists exist."""
        markdown = "- Item 1\n- Item 2"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_h1_with_code_blocks(self):
        """Test exception when only code blocks exist."""
        markdown = "```\ncode\n```"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_h1_with_quotes(self):
        """Test exception when only quotes exist."""
        markdown = "> A quote"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h1_ignored_if_not_first_heading(self):
        """Test that H1 is found even if not the first heading type."""
        markdown = "## H2 First\n\n# H1 Second"
        result = extract_title(markdown)
        self.assertEqual(result, "H1 Second")

    def test_only_first_h1_returned(self):
        """Test that only the first H1 is returned."""
        markdown = "# First Title\n\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_h1_with_numbers(self):
        """Test H1 title with numbers."""
        markdown = "# Title 123 456"
        result = extract_title(markdown)
        self.assertEqual(result, "Title 123 456")

    def test_h1_with_single_word(self):
        """Test H1 title with single word."""
        markdown = "# Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Title")

    def test_h1_with_long_title(self):
        """Test H1 title with long text."""
        markdown = "# This is a very long title with many words and content"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a very long title with many words and content")

    def test_h1_with_unicode_characters(self):
        """Test H1 title with unicode characters."""
        markdown = "# 你好 世界"
        result = extract_title(markdown)
        self.assertEqual(result, "你好 世界")

    def test_h1_with_emoji(self):
        """Test H1 title with emoji."""
        markdown = "# 🎉 Party Time 🎊"
        result = extract_title(markdown)
        self.assertEqual(result, "🎉 Party Time 🎊")

    def test_h1_with_links(self):
        """Test H1 title with markdown link."""
        markdown = "# [Click me](https://example.com)"
        result = extract_title(markdown)
        self.assertEqual(result, "[Click me](https://example.com)")

    def test_exception_message(self):
        """Test that exception has appropriate message."""
        markdown = "Just text"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No H1 header", str(context.exception))

    def test_h2_through_h6_not_considered_h1(self):
        """Test that H2-H6 are not extracted as H1."""
        for i in range(2, 7):
            markdown = f"{'#' * i} Title"
            with self.assertRaises(Exception):
                extract_title(markdown)

    def test_h1_with_extra_spaces_after_hash(self):
        """Test H1 with multiple spaces after hash (edge case)."""
        # Note: The function looks for "# " specifically
        markdown = "#  Title with extra space"
        # This should still work because it strips after finding "# "
        result = extract_title(markdown)
        self.assertIn("Title", result)

    def test_realistic_markdown_document(self):
        """Test with realistic markdown document."""
        markdown = """# My Blog Post

This is the introduction.

## Section 1

Content here.

- List item 1
- List item 2

## Section 2

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "My Blog Post")

    def test_h1_with_mixed_content(self):
        """Test realistic H1 with mixed content types."""
        markdown = """# Project: Static Site Generator

## Overview

This project converts markdown to HTML.

```python
def hello():
    pass
```

> A quote"""
        result = extract_title(markdown)
        self.assertEqual(result, "Project: Static Site Generator")


if __name__ == "__main__":
    unittest.main()
