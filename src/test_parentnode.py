import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_leaf_children_and_props(self):
        c1 = LeafNode("p", "child1")
        c2 = LeafNode("a", "link", props={"href": "https://ex.com"})
        node = ParentNode("div", [c1, c2], props={"class": "container"})
        expected = '<div class="container"><p>child1</p><a href="https://ex.com">link</a></div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_string_child(self):
        # strings are not valid children for strict ParentNode behavior;
        # ensure a ValueError is raised when a non-to_html child is present.
        c1 = "intro"
        c2 = LeafNode("p", "para")
        node = ParentNode("section", [c1, c2])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_raises_on_child_without_to_html(self):
        class BadChild:
            pass

        bad = BadChild()
        node = ParentNode("div", [bad])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_nested_parentnode(self):
        inner = ParentNode("span", [LeafNode("a", "x", props={"href": "/"})])
        outer = ParentNode("div", [inner])
        expected = '<div><span><a href="/">x</a></span></div>'
        self.assertEqual(outer.to_html(), expected)

    def test_raises_when_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_raises_when_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "x")]).to_html()


if __name__ == "__main__":
    unittest.main()
