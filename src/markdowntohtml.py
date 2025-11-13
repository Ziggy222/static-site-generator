from utilityfunctions import markdown_to_blocks, text_to_textnode, text_node_to_html_node
from blocktype import block_to_block_type, BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType

def text_to_children(text):
    """Convert inline markdown text into a list of HTMLNode children.

    This function takes a string of text containing inline markdown syntax
    (bold, italic, code, links, images) and converts it to a list of
    HTMLNode objects representing those elements.

    Args:
        text: A string potentially containing inline markdown.

    Returns:
        A list of HTMLNode objects (LeafNodes) representing the parsed inline markdown.
    """
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def block_to_html_node(block):
    """Convert a single markdown block into an HTMLNode.

    Determines the block type and creates the appropriate HTMLNode structure
    with children based on the block content.

    Args:
        block: A markdown block string.

    Returns:
        An HTMLNode representing the block.

    Raises:
        ValueError: If the block type is unsupported.
    """
    block_type = block_to_block_type(block)
    
    match block_type:
        case BlockType.HEADING:
            return block_to_heading(block)
        case BlockType.CODE:
            return block_to_code(block)
        case BlockType.QUOTE:
            return block_to_quote(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list(block)
        case BlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")


def block_to_heading(block):
    """Convert a heading block to an HTMLNode.

    Example: "## Heading" -> <h2>Heading</h2>

    Args:
        block: A markdown heading block string.

    Returns:
        A ParentNode with the appropriate heading tag (h1-h6).
    """
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    # Extract the text after the # symbols and space
    text = block[level + 1:].strip()
    children = text_to_children(text)
    
    tag = f"h{level}"
    return ParentNode(tag, children)


def block_to_code(block):
    """Convert a code block to an HTMLNode.

    Code blocks should not have inline markdown parsing. The code content
    is wrapped in <pre><code></code></pre> tags.

    Args:
        block: A markdown code block string (surrounded by ```).

    Returns:
        A ParentNode with <pre> tag containing a <code> child.
    """
    # Remove the opening and closing ``` markers
    code_content = block[3:-3].strip()
    
    # Create a text node for the code (no markdown parsing)
    code_text_node = TextNode(code_content, TextType.CODE)
    code_html_node = text_node_to_html_node(code_text_node)
    
    # Wrap in <pre> tag
    return ParentNode("pre", [code_html_node])


def block_to_quote(block):
    """Convert a quote block to an HTMLNode.

    Each line in the quote block starts with >. Lines are joined with <br> tags.

    Args:
        block: A markdown quote block string.

    Returns:
        A ParentNode with <blockquote> tag.
    """
    # Split into lines and remove the > prefix from each
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            # Remove the > and any following space
            line = line[1:].strip()
        quote_lines.append(line)
    
    # Join lines with newline to preserve structure
    quote_text = "\n".join(quote_lines)
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)


def block_to_unordered_list(block):
    """Convert an unordered list block to an HTMLNode.

    Each list item (line starting with - or *) becomes an <li> element.

    Args:
        block: A markdown unordered list block string.

    Returns:
        A ParentNode with <ul> tag containing <li> children.
    """
    # Split into list items
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        line = line.strip()
        # Remove the - or * and following space
        if line.startswith("- "):
            item_text = line[2:]
        elif line.startswith("* "):
            item_text = line[2:]
        else:
            continue
        
        # Create li element with inline markdown parsing
        children = text_to_children(item_text)
        li_node = ParentNode("li", children)
        list_items.append(li_node)
    
    return ParentNode("ul", list_items)


def block_to_ordered_list(block):
    """Convert an ordered list block to an HTMLNode.

    Each list item (line starting with N.) becomes an <li> element.

    Args:
        block: A markdown ordered list block string.

    Returns:
        A ParentNode with <ol> tag containing <li> children.
    """
    # Split into list items
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        line = line.strip()
        # Find the first digit and the dot, then extract the text after
        dot_index = line.find(". ")
        if dot_index != -1:
            item_text = line[dot_index + 2:]
            children = text_to_children(item_text)
            li_node = ParentNode("li", children)
            list_items.append(li_node)
    
    return ParentNode("ol", list_items)


def block_to_paragraph(block):
    """Convert a paragraph block to an HTMLNode.

    Paragraphs are wrapped in <p> tags and support inline markdown.

    Args:
        block: A markdown paragraph block string.

    Returns:
        A ParentNode with <p> tag.
    """
    # Clean up the block - replace newlines with spaces
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    """Convert a markdown document (string) to an HTMLNode tree.

    Splits the markdown into blocks, determines each block's type, converts
    each block to an appropriate HTMLNode, and returns a single parent div
    containing all block nodes as children.

    Args:
        markdown: A markdown-formatted string representing a full document.

    Returns:
        A ParentNode with tag 'div' containing all block HTMLNodes as children.

    Example:
        markdown = "# Title\\n\\nThis is a paragraph.\\n\\n- Item 1\\n- Item 2"
        html_node = markdown_to_html_node(markdown)
        # Returns a div containing h1, p, and ul nodes
    """
    blocks = markdown_to_blocks(markdown)
    
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    # Return a single parent div containing all block nodes
    return ParentNode("div", children)

        
