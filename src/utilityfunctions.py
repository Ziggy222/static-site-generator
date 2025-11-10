from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    """Convert a `TextNode` into an appropriate `LeafNode`.

    The conversion depends on `text_node.text_type` (see `TextType`). For
    LINK and IMAGE types the function will populate `props` with the
    appropriate URL fields.

    Returns a `LeafNode` instance.
    """
    # Handle each type of TextType appropriately
    match text_node.text_type: 
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", 
                value=text_node.text, 
                props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", 
                value="", 
                props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split nodes of `text_type` on `delimiter` and return a new list.

    For each input node whose `.text_type` equals `text_type` this function
    splits `node.text` by `delimiter` and appends TextNode parts for non-empty
    text fragments. Between parts it inserts a `TextNode(delimiter,
    TextType.PLAIN)` node so the delimiter appears in the output stream.

    Non-matching nodes are appended unchanged. The function returns a list
    of nodes (does not yield).
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    new_nodes.append(TextNode(part, text_type))
                if i < len(parts) - 1:
                    new_nodes.append(TextNode(delimiter, TextType.PLAIN))
        else:
            new_nodes.append(node)

    return new_nodes