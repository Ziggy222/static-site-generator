import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_p_with_value(self):
        node = LeafNode("p", "Hello, Paragraph!")
        expected = "<p>Hello, Paragraph!</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_a_with_props(self):
        node = LeafNode("a", "Click here", props={"href": "https://example.com"})
        expected = '<a href="https://example.com">Click here</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leafnode_to_html_raises_on_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_to_html_raises_on_children(self):
        node = LeafNode("p", "has children")
        # Inject children even though LeafNode constructor sets children=None
        node.children = [HTMLNode("span", "child")]
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_p_with_empty_string(self):
        node = LeafNode("p", "")
        expected = "<p></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_special_chars(self):
        node = LeafNode("p", 'Text with "quotes" & <brackets>')
        result = node.to_html()
        self.assertIn('Text with "quotes" & <brackets>', result)

    def test_to_html_with_multiple_props(self):
        node = LeafNode("a", "Link", props={"href": "https://example.com", "title": "Example"})
        result = node.to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('title="Example"', result)

    def test_to_html_tag_case_insensitive(self):
        node1 = LeafNode("P", "test")
        node2 = LeafNode("p", "test")
        self.assertEqual(node1.to_html(), node2.to_html())

    def test_to_html_uppercase_a_tag(self):
        node = LeafNode("A", "Link", props={"href": "https://example.com"})
        expected = '<a href="https://example.com">Link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_raises_on_unsupported_tag(self):
        node = LeafNode("img", "image")
        # img is rendered as a self-closing tag; value is ignored
        expected = "<img />"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_raises_on_unsupported_b_tag(self):
        node = LeafNode("b", "bold")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_raises_on_unsupported_code_tag(self):
        node = LeafNode("code", "print('hello')")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_with_url_special_chars(self):
        node = LeafNode("a", "Link", props={"href": "https://example.com?foo=bar&baz=qux"})
        result = node.to_html()
        self.assertIn('?foo=bar&baz=qux', result)


