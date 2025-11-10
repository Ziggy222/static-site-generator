from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    """Represents a piece of text with an associated TextType.

    Attributes:
        text: the string content
        text_type: a member of TextType describing how the text should be
                   interpreted (plain, bold, link, etc.)
        url: optional URL used for LINK and IMAGE types
    """
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Equality checks on text, text_type, and url."""
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        """Return a concise textual representation useful in tests."""
        to_string = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return(to_string)

         