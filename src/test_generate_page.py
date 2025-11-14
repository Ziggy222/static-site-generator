import unittest
import os
import tempfile

from main import generate_page


class TestGeneratePage(unittest.TestCase):
    def test_generate_page_creates_file_and_replaces_placeholders(self):
        md = "# Test Title\n\nThis is a paragraph."
        template = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"

        with tempfile.TemporaryDirectory() as td:
            md_path = os.path.join(td, "index.md")
            tpl_path = os.path.join(td, "template.html")
            out_path = os.path.join(td, "out", "index.html")

            # Write sample files
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md)
            with open(tpl_path, "w", encoding="utf-8") as f:
                f.write(template)

            # Ensure output directory does not exist to exercise creation logic
            if os.path.exists(os.path.dirname(out_path)):
                os.rmdir(os.path.dirname(out_path))

            # Run generate_page
            generate_page(md_path, tpl_path, out_path)

            # Assertions
            self.assertTrue(os.path.exists(out_path), "Output file was not created")

            with open(out_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            # Title should be present and placeholders removed
            self.assertIn("Test Title", content)
            self.assertNotIn("{{ Title }}", content)
            self.assertNotIn("{{ Content }}", content)

            # Content should include the converted markdown (wrapped in a div)
            self.assertIn("<div", content)
            self.assertIn("This is a paragraph.", content)


if __name__ == "__main__":
    unittest.main()
