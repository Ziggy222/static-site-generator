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
