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


def split_nodes_delimiter_from_plain(old_nodes, delimiter, text_type):
    """Split PLAIN nodes on delimiter and mark extracted text with the given type.

    This function processes PLAIN text nodes, splits them on the delimiter,
    and marks the text between delimiters with the specified TextType.
    
    For example, splitting "hello **bold** world" on "**" with TextType.BOLD
    produces: [PLAIN("hello "), BOLD("bold"), PLAIN(" world")]
    
    Non-PLAIN nodes are passed through unchanged.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            # Split on delimiter
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    # Alternate between PLAIN and the target type
                    # Even indices (0, 2, 4...) are PLAIN
                    # Odd indices (1, 3, 5...) are the target type
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.PLAIN))
                    else:
                        new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes


def extract_markdown_images(text):
    """Extract inline Markdown images from `text`.

    Finds occurrences of the form: ![alt text](url) and returns a list of
    (alt_text, url) tuples. The function performs a simple regex-based
    extraction and does not attempt to fully parse all Markdown edge cases
    (reference-style images, nested parentheses in URLs, etc.).
    """
    import re

    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    results = []
    for m in pattern.finditer(text or ""):
        alt = m.group(1)
        url = m.group(2).strip()
        results.append((alt, url))
    return results


def extract_markdown_links(text):
    """Extract inline Markdown links from `text`.

    Finds occurrences of the form: [link text](url) and returns a list of
    (link_text, url) tuples. This function intentionally avoids matching
    image syntax (i.e. ![alt](url)). The implementation is regex-based and
    handles common simple cases but does not fully implement Markdown
    reference-style links or complex nested punctuation in URLs.
    """
    import re

    # Negative lookbehind ensures we don't match image syntax (![...](...)).
    pattern = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)")
    results = []
    for m in pattern.finditer(text or ""):
        text_part = m.group(1)
        url = m.group(2).strip()
        results.append((text_part, url))
    return results

def split_nodes_image(old_nodes):
    """
    Unlike split_nodes_delimiter, this function does not need a delimiter
    nor a TextType. It only handles processing of Text with Images.
    This function should take in a Text node, and return a list of nodes 
    where each piece of text before and after an image is its own TextNode,
    and each image is its own TextNode of type IMAGE.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            images = extract_markdown_images(node.text)
            if not images:
                # No images found, append the original node
                new_nodes.append(node)
            else:
                # Process the text, splitting on images
                current_text = node.text
                for alt, url in images:
                    # Find the image markdown in the current text
                    image_md = f"![{alt}]({url})"
                    parts = current_text.split(image_md, 1)
                    
                    # Add the text before the image (if any)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.PLAIN))
                    
                    # Add the image node
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    
                    # Update current_text to the remainder
                    current_text = parts[1] if len(parts) > 1 else ""
                
                # Add any remaining text after the last image
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.PLAIN))
        else:
            # Non-PLAIN nodes are appended unchanged
            new_nodes.append(node)
    
    return new_nodes
    
    
def split_nodes_link(old_nodes):
    """
    Similar to split_nodes_image, this function processes PLAIN text nodes
    by extracting Markdown links and returning a list of nodes where each
    piece of text before and after a link is its own TextNode, and each link
    is its own TextNode of type LINK.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            links = extract_markdown_links(node.text)
            if not links:
                # No links found, append the original node
                new_nodes.append(node)
            else:
                # Process the text, splitting on links
                current_text = node.text
                for link_text, url in links:
                    # Find the link markdown in the current text
                    link_md = f"[{link_text}]({url})"
                    parts = current_text.split(link_md, 1)
                    
                    # Add the text before the link (if any)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.PLAIN))
                    
                    # Add the link node
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                    
                    # Update current_text to the remainder
                    current_text = parts[1] if len(parts) > 1 else ""
                
                # Add any remaining text after the last link
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.PLAIN))
        else:
            # Non-PLAIN nodes are appended unchanged
            new_nodes.append(node)
    
    return new_nodes


def text_to_textnode(text):
    """Convert a Markdown string into a list of appropriately typed TextNode objects.

    This function parses inline Markdown syntax and returns a list of TextNode
    objects with the correct types (PLAIN, BOLD, ITALIC, CODE, IMAGE, LINK).

    The parsing is done by sequentially applying split functions in order:
    1. Split on bold (**text**)
    2. Split on italic (_text_)
    3. Split on code (`text`)
    4. Split on images (![alt](url))
    5. Split on links ([text](url))

    Example:
        text = "This is **bold** and _italic_ with a [link](https://example.com)"
        nodes = text_to_textnode(text)
        # Returns: [
        #     TextNode("This is ", TextType.PLAIN),
        #     TextNode("bold", TextType.BOLD),
        #     TextNode(" and ", TextType.PLAIN),
        #     TextNode("italic", TextType.ITALIC),
        #     TextNode(" with a ", TextType.PLAIN),
        #     TextNode("link", TextType.LINK, "https://example.com"),
        # ]

    Args:
        text: A markdown-formatted string containing inline formatting.

    Returns:
        A list of TextNode objects representing the parsed markdown.
    """
    # Start with the input text as a single PLAIN TextNode
    nodes = [TextNode(text, TextType.PLAIN)]
    
    # Apply each split function in order
    # Use the new split_nodes_delimiter_from_plain for delimiter-based splitting
    nodes = split_nodes_delimiter_from_plain(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter_from_plain(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter_from_plain(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    """Convert a raw Markdown string into a list of block strings.

    This function takes a raw Markdown document and splits it into blocks
    separated by double newlines (\n\n). Each block is stripped of leading
    and trailing whitespace. Any empty blocks resulting from excess newlines
    are filtered out and not included in the return value.

    Args:
        markdown: A raw markdown string representing a full document.

    Returns:
        A list of block strings, with each block separated by double newlines
        and whitespace-stripped. Empty blocks are excluded.
        
    Example:
        markdown = "Block 1\\n\\nBlock 2\\n\\n\\n\\nBlock 3"
        result = markdown_to_blocks(markdown)
        # Returns: ["Block 1", "Block 2", "Block 3"]
    """
    blocks = []
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            final_blocks.append(block)
    return final_blocks
