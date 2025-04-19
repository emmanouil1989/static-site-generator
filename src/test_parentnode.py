import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_without_tag(self):
        node = ParentNode(None, [ParentNode("p", "Hello World")])
        with self.assertRaises(ValueError):
            node.to_html()
    def test_to_html_without_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_one_nested_children(self):
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_to_html_with_multiple_nested_children(self):
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),ParentNode("p", [LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text")])])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")

    def test_to_html_with_five_nested_children_with_props(self):
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),ParentNode("p", [LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text")])],{"class":"text"})
        self.assertEqual(node.to_html(), '<p class="text"><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>')
