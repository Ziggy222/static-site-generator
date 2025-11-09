from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        # LeafNode must not have children (we only support leaf nodes here)
        if self.children:
            raise ValueError("LeafNode must not have children")

        # if no value, raise an error.
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML.")

        # If no tag, return the value as plain text
        if self.tag is None:
            return self.value

        tag_lower = self.tag.lower()
        props_html = self.props_to_html()

        # Only support p and a tags for now
        if tag_lower == "p":
            return f"<p{props_html}>{self.value}</p>"
        if tag_lower == "a":
            return f"<a{props_html}>{self.value}</a>"

        raise NotImplementedError(f"LeafNode.to_html not implemented for tag: {self.tag}")
