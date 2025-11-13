import unittest

from markdowntohtml import (
    markdown_to_html_node,
    block_to_heading,
    block_to_code,
    block_to_quote,
    block_to_unordered_list,
    block_to_ordered_list,
    block_to_paragraph,
    text_to_children,
)
from parentnode import ParentNode
from leafnode import LeafNode


class TestTextToChildren(unittest.TestCase):
    """Test suite for text_to_children function."""

    def test_plain_text_to_children(self):
        """Test converting plain text to children."""
        text = "plain text"
        result = text_to_children(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].value, "plain text")

    def test_bold_text_to_children(self):
        """Test converting text with bold to children."""
        text = "**bold** text"
        result = text_to_children(text)
        self.assertGreater(len(result), 1)
        # Should have bold element
        bold_found = any(node.tag == "b" for node in result if hasattr(node, "tag"))
        self.assertTrue(bold_found)

    def test_link_text_to_children(self):
        """Test converting text with link to children."""
        text = "[link text](https://example.com)"
        result = text_to_children(text)
        self.assertGreater(len(result), 0)
        # Should have anchor element
        link_found = any(node.tag == "a" for node in result if hasattr(node, "tag"))
        self.assertTrue(link_found)

    def test_image_text_to_children(self):
        """Test converting text with image to children."""
        text = "![alt text](image.jpg)"
        result = text_to_children(text)
        self.assertGreater(len(result), 0)
        # Should have img element
        img_found = any(node.tag == "img" for node in result if hasattr(node, "tag"))
        self.assertTrue(img_found)

    def test_mixed_formatting_to_children(self):
        """Test converting text with mixed formatting."""
        text = "**bold** and _italic_ with [link](url)"
        result = text_to_children(text)
        self.assertGreater(len(result), 1)


class TestBlockToHeading(unittest.TestCase):
    """Test suite for block_to_heading function."""

    def test_heading_level_1(self):
        """Test H1 heading conversion."""
        block = "# Main Title"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h1")
        self.assertIsInstance(result, ParentNode)

    def test_heading_level_2(self):
        """Test H2 heading conversion."""
        block = "## Subtitle"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h2")

    def test_heading_level_3(self):
        """Test H3 heading conversion."""
        block = "### Section"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h3")

    def test_heading_level_6(self):
        """Test H6 heading conversion."""
        block = "###### Tiny heading"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h6")

    def test_heading_with_inline_markdown(self):
        """Test heading with bold text."""
        block = "# **Bold** Title"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h1")
        self.assertGreater(len(result.children), 0)


class TestBlockToCode(unittest.TestCase):
    """Test suite for block_to_code function."""

    def test_code_block_simple(self):
        """Test simple code block conversion."""
        block = "```\nprint('hello')\n```"
        result = block_to_code(block)
        self.assertEqual(result.tag, "pre")
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "code")

    def test_code_block_with_language(self):
        """Test code block with language specified."""
        block = "```python\ndef hello():\n    pass\n```"
        result = block_to_code(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(result.children[0].tag, "code")

    def test_code_block_multiline(self):
        """Test code block with multiple lines."""
        block = "```\nline 1\nline 2\nline 3\n```"
        result = block_to_code(block)
        self.assertEqual(result.tag, "pre")
        # Code content should have newlines preserved
        code_content = result.children[0].value
        self.assertIn("line 1", code_content)
        self.assertIn("line 2", code_content)


class TestBlockToQuote(unittest.TestCase):
    """Test suite for block_to_quote function."""

    def test_quote_single_line(self):
        """Test single-line quote conversion."""
        block = "> This is a quote"
        result = block_to_quote(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertIsInstance(result, ParentNode)

    def test_quote_multiline(self):
        """Test multiline quote conversion."""
        block = "> Line 1\n> Line 2\n> Line 3"
        result = block_to_quote(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertGreater(len(result.children), 0)

    def test_quote_with_inline_markdown(self):
        """Test quote with bold text."""
        block = "> This is a **bold** quote"
        result = block_to_quote(block)
        self.assertEqual(result.tag, "blockquote")


class TestBlockToUnorderedList(unittest.TestCase):
    """Test suite for block_to_unordered_list function."""

    def test_unordered_list_dashes(self):
        """Test unordered list with dashes."""
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_unordered_list(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 3)
        # Check all children are li elements
        for child in result.children:
            self.assertEqual(child.tag, "li")

    def test_unordered_list_asterisks(self):
        """Test unordered list with asterisks."""
        block = "* Item 1\n* Item 2"
        result = block_to_unordered_list(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)

    def test_unordered_list_single_item(self):
        """Test unordered list with single item."""
        block = "- Single item"
        result = block_to_unordered_list(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "li")

    def test_unordered_list_with_inline_markdown(self):
        """Test list items with markdown formatting."""
        block = "- **Bold** item\n- _Italic_ item"
        result = block_to_unordered_list(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)


class TestBlockToOrderedList(unittest.TestCase):
    """Test suite for block_to_ordered_list function."""

    def test_ordered_list_simple(self):
        """Test simple ordered list conversion."""
        block = "1. First\n2. Second\n3. Third"
        result = block_to_ordered_list(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 3)
        # Check all children are li elements
        for child in result.children:
            self.assertEqual(child.tag, "li")

    def test_ordered_list_different_starting_numbers(self):
        """Test ordered list starting with different numbers."""
        block = "5. Fifth\n6. Sixth\n7. Seventh"
        result = block_to_ordered_list(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 3)

    def test_ordered_list_single_item(self):
        """Test ordered list with single item."""
        block = "1. Only item"
        result = block_to_ordered_list(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 1)

    def test_ordered_list_with_inline_markdown(self):
        """Test ordered list items with markdown."""
        block = "1. **First** item\n2. [Link](url) item"
        result = block_to_ordered_list(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 2)


class TestBlockToParagraph(unittest.TestCase):
    """Test suite for block_to_paragraph function."""

    def test_paragraph_simple(self):
        """Test simple paragraph conversion."""
        block = "This is a paragraph"
        result = block_to_paragraph(block)
        self.assertEqual(result.tag, "p")
        self.assertIsInstance(result, ParentNode)

    def test_paragraph_multiline(self):
        """Test multiline paragraph (joined with spaces)."""
        block = "Line 1\nLine 2\nLine 3"
        result = block_to_paragraph(block)
        self.assertEqual(result.tag, "p")
        # Newlines should be replaced with spaces

    def test_paragraph_with_inline_markdown(self):
        """Test paragraph with bold, italic, and links."""
        block = "This is **bold** and _italic_ with a [link](url)"
        result = block_to_paragraph(block)
        self.assertEqual(result.tag, "p")
        self.assertGreater(len(result.children), 1)


class TestMarkdownToHtmlNode(unittest.TestCase):
    """Test suite for markdown_to_html_node function."""

    def test_empty_markdown(self):
        """Test conversion of empty markdown."""
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_single_paragraph(self):
        """Test conversion of single paragraph."""
        markdown = "This is a paragraph"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")

    def test_paragraph_and_heading(self):
        """Test conversion of paragraph followed by heading."""
        markdown = "# Heading\n\nParagraph text"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")

    def test_multiple_blocks(self):
        """Test conversion of multiple different block types."""
        markdown = "# Title\n\nParagraph\n\n- Item 1\n- Item 2\n\n```\ncode\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 4)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "ul")
        self.assertEqual(result.children[3].tag, "pre")

    def test_heading_levels(self):
        """Test document with multiple heading levels."""
        markdown = "# H1\n\n## H2\n\n### H3"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[2].tag, "h3")

    def test_lists_mixed(self):
        """Test document with unordered and ordered lists."""
        markdown = "- Unordered 1\n- Unordered 2\n\n1. Ordered 1\n2. Ordered 2"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(result.children[1].tag, "ol")

    def test_quote_block(self):
        """Test document with quote block."""
        markdown = "> This is a quote\n> With multiple lines"
        result = markdown_to_html_node(markdown)
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "blockquote")

    def test_return_type_is_parentnode(self):
        """Test that return value is a ParentNode."""
        markdown = "# Title\n\nParagraph"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")

    def test_realistic_document(self):
        """Test with a realistic markdown document."""
        markdown = """# My Blog Post

This is the introduction paragraph with **bold** and _italic_ text.

## Section 1

Here's an ordered list:

1. First point
2. Second point
3. Third point

## Section 2

Here's a code example:

```python
def hello():
    print("world")
```

And here's a quote:

> This is inspiring

- Bullet point 1
- Bullet point 2

Final paragraph."""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertGreater(len(result.children), 5)
        # Should have multiple different block types
        tags = [child.tag for child in result.children]
        self.assertIn("h1", tags)
        self.assertIn("h2", tags)
        self.assertIn("p", tags)
        self.assertIn("ol", tags)
        self.assertIn("ul", tags)
        self.assertIn("blockquote", tags)
        self.assertIn("pre", tags)

    def test_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        markdown = "\n\n# Title\n\n\n\nParagraph\n\n"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        # Empty blocks should be filtered out
        self.assertEqual(len(result.children), 2)

    def test_inline_markdown_in_all_blocks(self):
        """Test that inline markdown works in all block types."""
        markdown = """# **Bold** Title

Paragraph with **bold** and _italic_.

- **Bold** list item

1. **Bold** ordered item

> **Bold** quote"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        # All blocks should render successfully
        for child in result.children:
            self.assertIsNotNone(child)


if __name__ == "__main__":
    unittest.main()
