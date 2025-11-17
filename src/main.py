from textnode import TextNode
from textnode import TextType
from utilityfunctions import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from markdowntohtml import markdown_to_html_node


def extract_title(markdown):
    """Extract the H1 header from a markdown document.

    Searches through the markdown for an H1 header (line starting with "# ").
    Returns the header text stripped of whitespace and the leading "# ".

    Args:
        markdown: A markdown-formatted string.

    Returns:
        The H1 header text without the leading "# " and whitespace.

    Raises:
        Exception: If no H1 header is found in the markdown.

    Example:
        markdown = "# My Title\\n\\nContent here"
        title = extract_title(markdown)  # Returns "My Title"
    """
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            # Check if it's an H1 (starts with "# ")
            stripped = block.strip()
            if stripped.startswith("# "):
                # Extract text after "# " and strip whitespace
                return stripped[2:].strip()
    
    # No H1 header found
    raise Exception("No H1 header found in markdown")


def main():
    # Clear and copy static files, then generate the index page
    copy_source_to_destination("static", "public")
    # Generate `public/index.html` from `content/index.md` using `template.html`
    generate_pages_recursive("content", "template.html", "public")

def copy_source_to_destination(source_directory, destination_directory):
    """Recursively Copy all files from source_directory to destination_directory.
    Delete everything from destination_directory before copying.

    Args:
        source_directory: Path to the source directory.
        destination_directory: Path to the destination directory.
    """
    import os
    import shutil

    # Remove the destination directory entirely if it exists to ensure a clean copy
    if os.path.exists(destination_directory):
        # Remove everything under the destination directory
        shutil.rmtree(destination_directory)

    # Recreate the destination directory
    os.makedirs(destination_directory, exist_ok=True)

    # Copy files and directories from source to destination
    for item in os.listdir(source_directory):
        s = os.path.join(source_directory, item)
        d = os.path.join(destination_directory, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def generate_page(from_path, template_path, dest_path):
    """Generate an HTML page from a markdown source and an HTML template.

    Reads the markdown file at `from_path`, converts it to HTML using the
    markdown pipeline, extracts the document title (first H1), inserts the
    generated HTML and title into the template, and writes the result to
    `dest_path`. Creates destination directories as needed.
    """
    import os

    # Read source markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown to HTML string
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    # Extract title (may raise if no H1 present)
    title = extract_title(markdown)

    # Replace placeholders in template
    output = template.replace("{{ Title }}", title)
    output = output.replace("{{ Content }}", content_html)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Write output
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(output)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Generate HTML pages for all markdown files in a directory recursively.

    Args:
        dir_path_content: Path to the content directory containing markdown files.
        template_path: Path to the HTML template file.
        dest_dir_path: Path to the destination directory for generated HTML files.
    """
    import os

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                # Determine relative path to maintain directory structure
                rel_path = os.path.relpath(md_path, dir_path_content)
                html_file_name = os.path.splitext(rel_path)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, html_file_name)

                # Generate the page
                generate_page(md_path, template_path, dest_path)


if __name__ == "__main__":
    main()