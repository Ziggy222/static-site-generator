class HTMLNode:
    """Base class for HTML nodes.

    Attributes:
        tag: Optional[str] - the tag name (e.g. 'div', 'p').
        value: Optional[str] - inner text value for leaf nodes.
        children: Optional[list] - list of child HTMLNode objects.
        props: Optional[dict] - attributes for the tag.
    """
    def __init__(self, tag=None, value=None, 
                 children=None, props=None):
        # A string representing the HTML tag
        self.tag = tag
        # The value inside the HTML tag
        self.value = value
        # A list of HTMLNode objects representing child nodes
        self.children = children
        # Dictionary of key-value pairs for the HTML attributes
        self.props = props

    def to_html(self):
        """Render this node (and its children) to an HTML string.

        This base implementation is intentionally not implemented. Subclasses
        such as `LeafNode` and `ParentNode` should implement rendering.
        """
        raise NotImplementedError("to_html method is not implemented yet.")
    
    def props_to_html(self):
        """Convert the `props` dict into an HTML attributes string.

        Example: {'class': 'x', 'id': 'y'} -> ' class="x" id="y"'
        Returns an empty string when there are no props.
        """
        # if we have no props, return empty string
        if self.props is None or len(self.props) == 0:
            return ""

        # else, convert from props to return string
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
    
    def __eq__(self, other):
        """Equality comparison for HTMLNode instances.

        Two nodes are equal when their tag, value, children, and props
        compare equal.
        """
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    