import unittest

from htmlnode import *
from blocknode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<h1>", "header", None, {"key1":"value1","key2":"value2"})
        node2 = HTMLNode("tag", "value", "children", "none")
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = HTMLNode("<h1>", "header", None, {"key1":"value1","key2":"value2"})
        #print(node)
        self.assertNotEqual(node, None)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_title(self):
        text1 = """
# Heading 1
rest of stuff
"""
        self.assertEqual(extract_title(text1), "Heading 1")

    
if __name__ == "__main__":
    unittest.main()
