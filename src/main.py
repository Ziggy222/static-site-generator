from textnode import TextNode
from textnode import TextType

def main():
    """Small demo entrypoint used by the repository example.

    Creates a sample TextNode and prints its representation. This module is
    not used by the unit tests but is convenient for manual inspection.
    """
    node = TextNode("Dummy Text", TextType.PLAIN, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()