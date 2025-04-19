import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        self.assertEqual(node, node2)
    
    def test_not_eq_when_url_is_different(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.googl111e.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_when_one_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_when_text_is_different(self):
        node = TextNode("This is a text node111", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    
    def teset_not_eq_when_text_type_is_different(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_normal_text(self):
        text_node = TextNode("Hello World", TextType.NORMAL_TEXT)
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Hello World")
    
    def test_text_node_to_html_node_bold_text(self):
        text_node = TextNode("Hello World", TextType.BOLD_TEXT)
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Hello World")

    def test_text_node_to_html_node_italic_text(self):
        text_node = TextNode("Hello World", TextType.ITALIC_TEXT)
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "Hello World")
    
    def test_text_node_to_html_node_code_text(self):
        text_node = TextNode("Hello World", TextType.CODE_TEXT)
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "Hello World")
    
    def test_text_node_to_html_node_link_text(self):
        text_node = TextNode("Google", TextType.LINK_TEXT, "https://www.google.com")
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Google")
        self.assertEqual(node.props, {"href":"https://www.google.com"})
    
    def test_text_node_to_html_node_image_text(self):
        text_node = TextNode("Google", TextType.IMAGE_TEXT, "https://www.google.com")
        node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src":"https://www.google.com","alt":"Google"})
    


if __name__ == "__main__":
    unittest.main()