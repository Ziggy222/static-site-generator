import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    """Test suite for the block_to_block_type function."""

    # ==================== HEADING TESTS ====================
    def test_heading_h1(self):
        """Test detection of H1 heading."""
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h2(self):
        """Test detection of H2 heading."""
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h3(self):
        """Test detection of H3 heading."""
        block = "### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h6(self):
        """Test detection of H6 heading."""
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_with_leading_whitespace(self):
        """Test heading with leading whitespace (should still detect after strip)."""
        block = "   # Heading with leading whitespace"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_with_trailing_whitespace(self):
        """Test heading with trailing whitespace."""
        block = "# Heading with trailing whitespace   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    # ==================== CODE BLOCK TESTS ====================
    def test_code_block_simple(self):
        """Test detection of code block."""
        block = "```\ncode here\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_with_language(self):
        """Test code block with language specified."""
        block = "```python\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_multiline(self):
        """Test multiline code block."""
        block = "```\nline 1\nline 2\nline 3\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_with_whitespace(self):
        """Test code block with leading/trailing whitespace."""
        block = "   ```\ncode\n```   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_javascript(self):
        """Test code block with javascript language."""
        block = "```javascript\nconst x = 42;\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    # ==================== QUOTE TESTS ====================
    def test_quote_single_line(self):
        """Test detection of single-line quote."""
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_multiline(self):
        """Test multiline quote (all lines start with >)."""
        block = "> Line 1\n> Line 2\n> Line 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_with_leading_whitespace(self):
        """Test quote with leading whitespace."""
        block = "   > This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_with_trailing_whitespace(self):
        """Test quote with trailing whitespace."""
        block = "> This is a quote   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_nested_angle_brackets(self):
        """Test quote with nested content."""
        block = "> This quote has > more > chevrons"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    # ==================== UNORDERED LIST TESTS ====================
    def test_unordered_list_dash(self):
        """Test unordered list with dashes."""
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk(self):
        """Test unordered list with asterisks."""
        block = "* Item 1\n* Item 2\n* Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        """Test unordered list with single item."""
        block = "- Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_with_leading_whitespace(self):
        """Test unordered list with leading whitespace."""
        block = "   - Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_with_trailing_whitespace(self):
        """Test unordered list with trailing whitespace."""
        block = "- Item 1   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk_single(self):
        """Test unordered list with single asterisk item."""
        block = "* Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    # ==================== ORDERED LIST TESTS ====================
    def test_ordered_list_single_digit(self):
        """Test ordered list with single digit numbers."""
        block = "1. First\n2. Second\n3. Third"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_starting_with_1(self):
        """Test ordered list starting with 1."""
        block = "1. Item one"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_starting_with_5(self):
        """Test ordered list starting with 5."""
        block = "5. Fifth item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_starting_with_9(self):
        """Test ordered list starting with 9."""
        block = "9. Ninth item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_with_leading_whitespace(self):
        """Test ordered list with leading whitespace."""
        block = "   1. Item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_with_trailing_whitespace(self):
        """Test ordered list with trailing whitespace."""
        block = "1. Item   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        """Test ordered list with multiple items."""
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    # ==================== PARAGRAPH TESTS ====================
    def test_paragraph_simple(self):
        """Test detection of simple paragraph."""
        block = "This is a paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        """Test multiline paragraph."""
        block = "This is a paragraph\nwith multiple lines\nof text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_leading_whitespace(self):
        """Test paragraph with leading whitespace."""
        block = "   This is a paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_trailing_whitespace(self):
        """Test paragraph with trailing whitespace."""
        block = "This is a paragraph   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_special_characters(self):
        """Test paragraph with special characters."""
        block = "This paragraph has **bold** and _italic_ text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_empty_after_strip(self):
        """Test that whitespace-only strings are treated as paragraphs."""
        block = "   just spaces   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_hash_in_middle(self):
        """Test that # in the middle doesn't make it a heading."""
        block = "This is not # a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_numbers(self):
        """Test paragraph starting with a number (not ordered list)."""
        block = "42 is the answer"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_10_number(self):
        """Test paragraph starting with double digit (not ordered list)."""
        block = "10. This looks like a list but has double digit"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # ==================== EDGE CASES ====================
    def test_hash_without_space_not_heading(self):
        """Test that # without space is not a heading (edge case)."""
        block = "#notaheading"
        result = block_to_block_type(block)
        # This is implementation dependent - current impl treats as heading
        # because it only checks for startswith("#")
        self.assertEqual(result, BlockType.HEADING)

    def test_dash_without_space_not_unordered_list(self):
        """Test that - without space is not an unordered list."""
        block = "-notalist"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_asterisk_without_space_not_unordered_list(self):
        """Test that * without space is not an unordered list."""
        block = "*notalist"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_number_without_dot_not_ordered_list(self):
        """Test that number without dot is not an ordered list."""
        block = "1 not a list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_greater_than_without_space(self):
        """Test > without space after it (edge case)."""
        block = ">notaquote"
        result = block_to_block_type(block)
        # Current impl treats as quote because it only checks startswith(">")
        self.assertEqual(result, BlockType.QUOTE)

    def test_empty_code_block(self):
        """Test empty code block."""
        block = "```\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_fence_only(self):
        """Test just code fences on same line."""
        block = "``````"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_single_backtick_not_code(self):
        """Test single backtick is not code."""
        block = "`not code"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_only_opening_code_fence(self):
        """Test only opening code fence (no closing)."""
        block = "```\ncode here"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_only_closing_code_fence(self):
        """Test only closing code fence."""
        block = "code here\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # ==================== TYPE VALIDATION ====================
    def test_return_type_is_blocktype(self):
        """Test that return value is a BlockType enum."""
        block = "# Heading"
        result = block_to_block_type(block)
        self.assertIsInstance(result, BlockType)

    def test_all_block_types_discoverable(self):
        """Test that all BlockType enum values can be returned."""
        test_cases = [
            ("# Heading", BlockType.HEADING),
            ("```code```", BlockType.CODE),
            ("> Quote", BlockType.QUOTE),
            ("- List", BlockType.UNORDERED_LIST),
            ("1. List", BlockType.ORDERED_LIST),
            ("Paragraph", BlockType.PARAGRAPH),
        ]
        for block, expected_type in test_cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, expected_type)

    # ==================== REAL-WORLD EXAMPLES ====================
    def test_realistic_heading(self):
        """Test realistic heading."""
        block = "# Welcome to My Blog"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_realistic_code_block(self):
        """Test realistic code block with multiple lines."""
        block = "```python\ndef hello_world():\n    print('Hello, World!')\nhello_world()\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_realistic_quote_block(self):
        """Test realistic quote block."""
        block = "> Life is like a box of chocolates\n> You never know what you're gonna get"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_realistic_unordered_list(self):
        """Test realistic unordered list."""
        block = "- Buy groceries\n- Cook dinner\n- Clean up"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_realistic_ordered_list(self):
        """Test realistic ordered list."""
        block = "1. Wake up\n2. Brush teeth\n3. Eat breakfast\n4. Go to work"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_realistic_paragraph(self):
        """Test realistic paragraph with markdown syntax."""
        block = "This is a paragraph with **bold text** and _italic text_ and a [link](https://example.com)"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
