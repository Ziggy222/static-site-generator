import unittest

from textnode import TextNode, TextType
from utilityfunctions import text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_neq_one_with_url_other_without(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_neq_all_different(self):
        node = TextNode("Text A", TextType.PLAIN, "https://a.com")
        node2 = TextNode("Text B", TextType.BOLD, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_repr_plain_text(self):
        node = TextNode("Hello, World!", TextType.PLAIN)
        expected = "TextNode(Hello, World!, 1, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_bold_text(self):
        node = TextNode("Bold Text", TextType.BOLD)
        expected = "TextNode(Bold Text, 2, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("Link Text", TextType.LINK, "https://example.com")
        expected = "TextNode(Link Text, 5, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_text_node_to_html_node_plain(self):
        tn = TextNode("plain", TextType.PLAIN)
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag=None, value="plain")
        self.assertEqual(got.tag, expected.tag)
        self.assertEqual(got.value, expected.value)
        self.assertEqual(got.props, expected.props)

    def test_text_node_to_html_node_bold(self):
        tn = TextNode("bold", TextType.BOLD)
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="b", value="bold")
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_link(self):
        tn = TextNode("link text", TextType.LINK, "https://example.com")
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="a", value="link text", props={"href": "https://example.com"})
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_image(self):
        tn = TextNode("alt text", TextType.IMAGE, "https://img.com/pic.png")
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="img", value="", props={"src": "https://img.com/pic.png", "alt": "alt text"})
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_unsupported(self):
        class FakeType:
            pass

        tn = TextNode("x", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(tn)

    def test_eq_with_empty_text(self):
        node1 = TextNode("", TextType.PLAIN)
        node2 = TextNode("", TextType.PLAIN)
        self.assertEqual(node1, node2)

    def test_neq_empty_vs_nonempty(self):
        node1 = TextNode("", TextType.PLAIN)
        node2 = TextNode("text", TextType.PLAIN)
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html_node_code(self):
        tn = TextNode("print('hello')", TextType.CODE)
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="code", value="print('hello')")
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_italic(self):
        tn = TextNode("italic text", TextType.ITALIC)
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="i", value="italic text")
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_image_empty_alt(self):
        tn = TextNode("", TextType.IMAGE, "https://img.com/pic.png")
        got = text_node_to_html_node(tn)
        expected = LeafNode(tag="img", value="", props={"src": "https://img.com/pic.png", "alt": ""})
        self.assertEqual(got, expected)

    def test_text_node_to_html_node_link_special_chars(self):
        tn = TextNode("link", TextType.LINK, "https://example.com?foo=bar&baz=qux")
        got = text_node_to_html_node(tn)
        self.assertEqual(got.tag, "a")
        self.assertIn("?foo=bar&baz=qux", got.props["href"])

    def test_repr_with_empty_text(self):
        node = TextNode("", TextType.PLAIN)
        expected = "TextNode(, 1, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_all_texttypes(self):
        # Ensure all TextType enum values produce valid reprs
        for text_type in TextType:
            node = TextNode("test", text_type)
            result = repr(node)
            self.assertIn("TextNode", result)
            self.assertIn(str(text_type.value), result)

    def test_text_node_to_html_node_link_no_url(self):
        # Links require URL but this tests the constructor allows None
        tn = TextNode("link text", TextType.LINK, None)
        got = text_node_to_html_node(tn)
        # Should still convert but props won't have href
        self.assertEqual(got.tag, "a")
        # The function should include the href as None or handle gracefully
        self.assertIn("href", got.props)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()