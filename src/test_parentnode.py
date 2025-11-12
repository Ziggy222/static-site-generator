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

    def test_to_html_with_single_child(self):
        child = LeafNode("p", "only child")
        node = ParentNode("div", [child])
        expected = "<div><p>only child</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_three_children(self):
        c1 = LeafNode("p", "first")
        c2 = LeafNode("p", "second")
        c3 = LeafNode("p", "third")
        node = ParentNode("section", [c1, c2, c3])
        expected = "<section><p>first</p><p>second</p><p>third</p></section>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_deeply_nested(self):
        inner = LeafNode("p", "deep")
        level2 = ParentNode("div", [inner])
        level1 = ParentNode("section", [level2])
        expected = "<section><div><p>deep</p></div></section>"
        self.assertEqual(level1.to_html(), expected)

    def test_to_html_tag_case_insensitive(self):
        child = LeafNode("p", "test")
        node1 = ParentNode("DIV", [child])
        node2 = ParentNode("div", [child])
        self.assertEqual(node1.to_html(), node2.to_html())

    def test_to_html_mixed_children_types(self):
        leaf = LeafNode("p", "paragraph")
        inner_leaf = LeafNode("a", "link", props={"href": "/"})
        nested = ParentNode("span", [inner_leaf])
        node = ParentNode("div", [leaf, nested])
        expected = '<div><p>paragraph</p><span><a href="/">link</a></span></div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_empty_props_dict(self):
        child = LeafNode("p", "test")
        node = ParentNode("div", [child], props={})
        expected = "<div><p>test</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_multiple_props(self):
        child = LeafNode("p", "test")
        node = ParentNode("div", [child], props={"class": "container", "id": "main"})
        result = node.to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn("<div", result)


if __name__ == "__main__":
    unittest.main()
