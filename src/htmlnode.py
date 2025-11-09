class HTMLNode: 
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
        # Not implemented at HTMLNode level. Use specialized subclasses
        # (for example LeafNode) to render HTML for leaf-only nodes.
        raise NotImplementedError("to_html method is not implemented yet.")
    
    def props_to_html(self):
        # if we have no props, return empty string
        if self.props is None or len(self.props) == 0:
            return ""
        
        # else, convert from props to return string
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
    
    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"