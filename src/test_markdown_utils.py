import unittest
from markdown_utils import (
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
  

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

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

    def test_single_heading(self):
        md = """

# This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>",
        )
    
    def test_heading_two(self):
        md = """
## This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading</h2></div>",
        )
    def test_heading_three(self):
        md = """
### This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>",
        )

    def test_heading_four(self):
        md = """
#### This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is a heading</h4></div>",
        )
    def test_heading_five(self):
        md = """
##### This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h5>This is a heading</h5></div>",
        )
    def test_heading_six(self):
        md = """
###### This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading</h6></div>",
        )
    def test_unordered_list(self):
        md = """
- This is a list
- with items
- and more items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and more items</li></ul></div>",
        )
    def test_ordered_list(self):
        md = """
1. This is a list
2. with items
3. and more items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li><li>and more items</li></ol></div>",
        )
    
    def test_quote(self):
        md = """
> This is a quote
> with more text
> and even more text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with more text and even more text</blockquote></div>",
        )
    
    def test_code(self):
        md = """
```
This is a code block
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is a code block\n</code></pre></div>",
        )
    def test_code_with_newlines(self):
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

    def test_extract_title(self):
        md = """

This is a paragraph
```
This is a code block
```
This is another paragraph
# This is a title
- This is a list
- with items
- and more items
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a title")
        
    if __name__ == "__main__":
        unittest.main()



