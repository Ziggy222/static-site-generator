# All non-Leaf nodes must be ParentNodes.
from htmlnode import HTMLNode
class ParentNode(HTMLNode):
    # Initialize ParentNode with tag, children and optional props
    # It cannot take a value
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        # ParentNode must have a tag
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML.")
        # ParentNode must have children
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children to convert to HTML.")
        
        tag_lower = self.tag.lower()
        props_html = self.props_to_html()

        parts = []
        for child in self.children:
            # Child must implement to_html (strict behavior)
            if not (hasattr(child, 'to_html') and callable(child.to_html)):
                raise ValueError(f"Child of ParentNode must implement to_html: {child!r}")
            parts.append(child.to_html())

        inner = "".join(parts)
        return f"<{tag_lower}{props_html}>{inner}</{tag_lower}>"
