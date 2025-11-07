from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("Dummy Text", TextType.PLAIN, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()