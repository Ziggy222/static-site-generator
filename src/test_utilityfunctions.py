import unittest

from textnode import TextNode, TextType
from utilityfunctions import split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
