from enum import Enum

# The below block types are the block types we support from markdown.
class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block):
    """Convert a block (string) to a BlockType.

    This is a stub implementation. In a real implementation, you would parse
    the block content to determine its type.
    """
    stripped = block.strip()
    if stripped.startswith("#"):
        return BlockType.HEADING
    elif stripped.startswith("```") and stripped.endswith("```"):
        return BlockType.CODE
    elif stripped.startswith(">"):
        return BlockType.QUOTE
    elif stripped.startswith("- ") or stripped.startswith("* "):
        return BlockType.UNORDERED_LIST
    elif any(stripped.startswith(f"{i}. ") for i in range(1, 10)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

