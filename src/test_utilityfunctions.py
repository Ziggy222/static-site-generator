import unittest

from textnode import TextNode, TextType
from utilityfunctions import split_nodes_delimiter, extract_markdown_images
from utilityfunctions import extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode, split_nodes_delimiter_from_plain



class TestUtilityFunctions(unittest.TestCase):
    def test_simple_split(self):
        old = [TextNode("hello,world", TextType.BOLD)]
        out = split_nodes_delimiter(old, ",", TextType.BOLD)
        expected = [
            TextNode("hello", TextType.BOLD),
            TextNode(",", TextType.PLAIN),
            TextNode("world", TextType.BOLD),
        ]
        self.assertEqual(out, expected)

    def test_mixed_nodes(self):
        old = [TextNode("x|y|z", TextType.CODE), TextNode("keep", TextType.PLAIN)]
        out = split_nodes_delimiter(old, "|", TextType.CODE)
        expected = [
            TextNode("x", TextType.CODE),
            TextNode("|", TextType.PLAIN),
            TextNode("y", TextType.CODE),
            TextNode("|", TextType.PLAIN),
            TextNode("z", TextType.CODE),
            TextNode("keep", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_consecutive_delimiters(self):
        old = [TextNode("a,,b", TextType.BOLD)]
        out = split_nodes_delimiter(old, ",", TextType.BOLD)
        expected = [
            TextNode("a", TextType.BOLD),
            TextNode(",", TextType.PLAIN),
            TextNode(",", TextType.PLAIN),
            TextNode("b", TextType.BOLD),
        ]
        self.assertEqual(out, expected)

    def test_leading_and_trailing_delimiters(self):
        old = [TextNode(",start,end,", TextType.BOLD)]
        out = split_nodes_delimiter(old, ",", TextType.BOLD)
        expected = [
            TextNode(",", TextType.PLAIN),
            TextNode("start", TextType.BOLD),
            TextNode(",", TextType.PLAIN),
            TextNode("end", TextType.BOLD),
            TextNode(",", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_empty_string_node_produces_no_nodes(self):
        old = [TextNode("", TextType.BOLD)]
        out = split_nodes_delimiter(old, ",", TextType.BOLD)
        expected = []
        self.assertEqual(out, expected)

    def test_extract_markdown_images_simple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        out = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(out, expected)

    def test_extract_markdown_images_none(self):
        text = "no images here"
        out = extract_markdown_images(text)
        self.assertEqual(out, [])

    def test_extract_markdown_links_simple(self):
        text = "Visit [Boot.dev](https://boot.dev) and [Example](https://example.com)"
        out = extract_markdown_links(text)
        expected = [("Boot.dev", "https://boot.dev"), ("Example", "https://example.com")]
        self.assertEqual(out, expected)

    def test_extract_markdown_links_ignores_images(self):
        text = "Image ![alt](https://img) and link [here](https://here)"
        out = extract_markdown_links(text)
        expected = [("here", "https://here")]
        self.assertEqual(out, expected)

    def test_extract_markdown_links_none(self):
        text = "no links here"
        out = extract_markdown_links(text)
        self.assertEqual(out, [])

    def test_split_nodes_image_simple(self):
        text = "text before ![alt1](url1) text between ![alt2](url2) text after"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [
            TextNode("text before ", TextType.PLAIN),
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode(" text between ", TextType.PLAIN),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode(" text after", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_image_no_images(self):
        text = "text with no images"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [TextNode(text, TextType.PLAIN)]
        self.assertEqual(out, expected)

    def test_split_nodes_image_only_image(self):
        text = "![alt](url)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [TextNode("alt", TextType.IMAGE, "url")]
        self.assertEqual(out, expected)

    def test_split_nodes_image_non_plain_nodes_unchanged(self):
        old = [TextNode("some link text", TextType.LINK, "url")]
        out = split_nodes_image(old)
        expected = [TextNode("some link text", TextType.LINK, "url")]
        self.assertEqual(out, expected)

    def test_split_nodes_link_simple(self):
        text = "text before [link1](url1) text between [link2](url2) text after"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [
            TextNode("text before ", TextType.PLAIN),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" text between ", TextType.PLAIN),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" text after", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_link_no_links(self):
        text = "text with no links"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [TextNode(text, TextType.PLAIN)]
        self.assertEqual(out, expected)

    def test_split_nodes_link_only_link(self):
        text = "[link](url)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [TextNode("link", TextType.LINK, "url")]
        self.assertEqual(out, expected)

    def test_split_nodes_link_non_plain_nodes_unchanged(self):
        old = [TextNode("some image text", TextType.IMAGE, "url")]
        out = split_nodes_link(old)
        expected = [TextNode("some image text", TextType.IMAGE, "url")]
        self.assertEqual(out, expected)

    def test_extract_markdown_images_empty_alt(self):
        text = "Image with empty alt: ![](https://example.com)"
        out = extract_markdown_images(text)
        expected = [("", "https://example.com")]
        self.assertEqual(out, expected)

    def test_extract_markdown_links_empty_text(self):
        text = "Link with empty text: [](https://example.com)"
        out = extract_markdown_links(text)
        # The regex requires at least one character in the link text, so empty [] is not matched
        expected = []
        self.assertEqual(out, expected)

    def test_extract_markdown_images_with_whitespace_in_url(self):
        text = "Image: ![alt]( https://example.com )"
        out = extract_markdown_images(text)
        expected = [("alt", "https://example.com")]
        self.assertEqual(out, expected)

    def test_extract_markdown_links_with_whitespace_in_url(self):
        text = "Link: [text]( https://example.com )"
        out = extract_markdown_links(text)
        expected = [("text", "https://example.com")]
        self.assertEqual(out, expected)

    def test_split_nodes_image_consecutive_images(self):
        text = "![img1](url1)![img2](url2)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_link_consecutive_links(self):
        text = "[link1](url1)[link2](url2)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_image_leading_image(self):
        text = "![alt](url) text after"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_link_leading_link(self):
        text = "[link](url) text after"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text after", TextType.PLAIN),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_image_trailing_image(self):
        text = "text before ![alt](url)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [
            TextNode("text before ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_link_trailing_link(self):
        text = "text before [link](url)"
        old = [TextNode(text, TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [
            TextNode("text before ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_image_mixed_input(self):
        text1 = "plain with ![img](url)"
        old = [
            TextNode(text1, TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
        ]
        out = split_nodes_image(old)
        expected = [
            TextNode("plain with ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_link_mixed_input(self):
        text1 = "plain with [link](url)"
        old = [
            TextNode(text1, TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
        ]
        out = split_nodes_link(old)
        expected = [
            TextNode("plain with ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "url"),
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(out, expected)

    def test_split_nodes_delimiter_no_delimiter_found(self):
        old = [TextNode("no delimiter here", TextType.BOLD)]
        out = split_nodes_delimiter(old, ",", TextType.BOLD)
        expected = [TextNode("no delimiter here", TextType.BOLD)]
        self.assertEqual(out, expected)

    def test_split_nodes_image_empty_plain_node(self):
        old = [TextNode("", TextType.PLAIN)]
        out = split_nodes_image(old)
        expected = [TextNode("", TextType.PLAIN)]
        self.assertEqual(out, expected)

    def test_split_nodes_link_empty_plain_node(self):
        old = [TextNode("", TextType.PLAIN)]
        out = split_nodes_link(old)
        expected = [TextNode("", TextType.PLAIN)]
        self.assertEqual(out, expected)

    def test_text_to_textnode_plain_text(self):
        """Test parsing plain text with no formatting."""
        text = "This is plain text"
        result = text_to_textnode(text)
        expected = [TextNode("This is plain text", TextType.PLAIN)]
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_bold(self):
        """Test parsing text with only bold."""
        text = "This is **bold** text"
        result = text_to_textnode(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_italic(self):
        """Test parsing text with only italic."""
        text = "This is _italic_ text"
        result = text_to_textnode(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_code(self):
        """Test parsing text with only code."""
        text = "This is `code` text"
        result = text_to_textnode(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_image(self):
        """Test parsing text with only image."""
        text = "Image: ![alt](https://example.com/img.png)"
        result = text_to_textnode(text)
        expected = [
            TextNode("Image: ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_link(self):
        """Test parsing text with only link."""
        text = "Check [this](https://example.com)"
        result = text_to_textnode(text)
        expected = [
            TextNode("Check ", TextType.PLAIN),
            TextNode("this", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_comprehensive(self):
        """Test the comprehensive example from the requirements."""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnode(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_same_type(self):
        """Test parsing multiple bold sections."""
        text = "**bold1** and **bold2** text"
        result = text_to_textnode(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_and_italic(self):
        """Test parsing bold and italic together."""
        text = "**bold** and _italic_"
        result = text_to_textnode(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_consecutive_delimiters(self):
        """Test consecutive formatting without text between."""
        text = "**bold**_italic_"
        result = text_to_textnode(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_images_and_links(self):
        """Test multiple images and links."""
        text = "![img1](url1) text [link1](url1) more ![img2](url2) and [link2](url2)"
        result = text_to_textnode(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" text ", TextType.PLAIN),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" more ", TextType.PLAIN),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_code_with_special_chars(self):
        """Test code containing special characters."""
        text = "Use `print('hello')` for output"
        result = text_to_textnode(text)
        expected = [
            TextNode("Use ", TextType.PLAIN),
            TextNode("print('hello')", TextType.CODE),
            TextNode(" for output", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_empty_string(self):
        """Test empty input string."""
        text = ""
        result = text_to_textnode(text)
        # Empty string produces empty list (no nodes needed)
        expected = []
        self.assertEqual(result, expected)

    def test_text_to_textnode_only_delimiters(self):
        """Test string with only delimiters."""
        text = "**bold** with _italic_ and `code`"
        result = text_to_textnode(text)
        # After all splits, should have multiple nodes
        self.assertGreater(len(result), 1)
        # First should be bold
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_text_to_textnode_link_with_query_params(self):
        """Test link with query parameters."""
        text = "Check [this](https://example.com?foo=bar&baz=qux)"
        result = text_to_textnode(text)
        expected = [
            TextNode("Check ", TextType.PLAIN),
            TextNode("this", TextType.LINK, "https://example.com?foo=bar&baz=qux"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_image_with_spaces_in_alt(self):
        """Test image with spaces in alt text."""
        text = "Picture: ![alt text with spaces](url)"
        result = text_to_textnode(text)
        expected = [
            TextNode("Picture: ", TextType.PLAIN),
            TextNode("alt text with spaces", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_from_plain_simple(self):
        """Test split_nodes_delimiter_from_plain with simple case."""
        node = TextNode("hello **bold** world", TextType.PLAIN)
        result = split_nodes_delimiter_from_plain([node], "**", TextType.BOLD)
        expected = [
            TextNode("hello ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_from_plain_multiple(self):
        """Test with multiple occurrences."""
        node = TextNode("**bold1** and **bold2**", TextType.PLAIN)
        result = split_nodes_delimiter_from_plain([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_from_plain_non_plain_nodes_unchanged(self):
        """Test that non-PLAIN nodes pass through unchanged."""
        node1 = TextNode("**bold** text", TextType.BOLD)
        node2 = TextNode("other", TextType.PLAIN)
        result = split_nodes_delimiter_from_plain([node1, node2], "_", TextType.ITALIC)
        expected = [
            TextNode("**bold** text", TextType.BOLD),
            TextNode("other", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_from_plain_no_delimiter(self):
        """Test when delimiter not found."""
        node = TextNode("no delimiter here", TextType.PLAIN)
        result = split_nodes_delimiter_from_plain([node], "**", TextType.BOLD)
        expected = [TextNode("no delimiter here", TextType.PLAIN)]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
