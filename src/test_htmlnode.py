import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_eq_simple_nodes(self):
        node1 = HTMLNode("p", "Hello, World!")
        node2 = HTMLNode("p", "Hello, World!")
        self.assertEqual(node1, node2)

    def test_eq_with_props(self):
        node1 = HTMLNode("a", "Click me!", props={"href": "https://www.example.com"})
        node2 = HTMLNode("a", "Click me!", props={"href": "https://www.example.com"})
        self.assertEqual(node1, node2)

    def test_eq_with_children(self):
        child1 = HTMLNode("span", "child")
        child2 = HTMLNode("span", "child")
        node1 = HTMLNode("div", children=[child1])
        node2 = HTMLNode("div", children=[child2])
        self.assertEqual(node1, node2)

    def test_eq_with_all_attributes(self):
        child1 = HTMLNode("b", "bold")
        child2 = HTMLNode("b", "bold")
        node1 = HTMLNode("div", "parent", [child1], {"class": "container"})
        node2 = HTMLNode("div", "parent", [child2], {"class": "container"})
        self.assertEqual(node1, node2)

    def test_neq_different_tag(self):
        node1 = HTMLNode("p", "text")
        node2 = HTMLNode("div", "text")
        self.assertNotEqual(node1, node2)

    def test_neq_different_value(self):
        node1 = HTMLNode("p", "text1")
        node2 = HTMLNode("p", "text2")
        self.assertNotEqual(node1, node2)

    def test_neq_different_children(self):
        node1 = HTMLNode("div", children=[HTMLNode("p", "text1")])
        node2 = HTMLNode("div", children=[HTMLNode("p", "text2")])
        self.assertNotEqual(node1, node2)

    def test_neq_different_props(self):
        node1 = HTMLNode("div", props={"class": "container"})
        node2 = HTMLNode("div", props={"class": "wrapper"})
        self.assertNotEqual(node1, node2)

    def test_repr_simple_node(self):
        node = HTMLNode("p", "Hello, World!")
        expected = 'HTMLNode(tag=p, value=Hello, World!, children=None, props=None)'
        self.assertEqual(repr(node), expected)

    def test_repr_with_props(self):
        node = HTMLNode("a", "Click me!", props={"href": "https://www.example.com"})
        expected = "HTMLNode(tag=a, value=Click me!, children=None, props={'href': 'https://www.example.com'})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children(self):
        child = HTMLNode("span", "child")
        node = HTMLNode("div", children=[child])
        expected = f"HTMLNode(tag=div, value=None, children=[{repr(child)}], props=None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_all_attributes(self):
        child = HTMLNode("b", "bold")
        node = HTMLNode("div", "parent", [child], {"class": "container"})
        expected = f"HTMLNode(tag=div, value=parent, children=[{repr(child)}], props={{'class': 'container'}})"
        self.assertEqual(repr(node), expected)

