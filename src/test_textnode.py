import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()