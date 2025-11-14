from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """Represents an HTML leaf node (no children).

    Leaf nodes have a `tag` and `value` and may have `props`. They must not
    contain children.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        """Render the leaf node to HTML.

        Enforces that the node has no children and that it has a value.
        Supports a small set of tags (currently 'p' and 'a'). If `tag` is
        None the method returns the raw `value` (plain text).
        """
        # LeafNode must not have children (we only support leaf nodes here)
        if self.children:
            raise ValueError("LeafNode must not have children")

        # If no tag, return the value as plain text
        if self.tag is None:
            # value may be empty string
            return self.value

        tag_lower = self.tag.lower()
        props_html = self.props_to_html()

        # Support <img> as a self-closing tag; it does not use `value`.
        if tag_lower == "img":
            return f"<img{props_html} />"

        # For other leaf tags, `value` must be present (can be empty string)
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML.")

        # Support p and a tags
        if tag_lower == "p":
            return f"<p{props_html}>{self.value}</p>"
        if tag_lower == "a":
            return f"<a{props_html}>{self.value}</a>"

        raise NotImplementedError(f"LeafNode.to_html not implemented for tag: {self.tag}")
