import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Hello World", None, {"class":"text"})
        self.assertEqual(node.props_to_html(), ' class="text"')
        self.assertNotEqual(node.props_to_html(), 'class="text"')

    def test_multiple_props_to_html(self):
        node = HTMLNode("p", "Hello World", None, {"class":"text", "id":"1"})
        self.assertEqual(node.props_to_html(), ' class="text" id="1"')
    
    def test_repr(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node.__repr__(), "HTMLNode(p,Hello World,None,None)")
    def test_repr_with_children(self):
        node = HTMLNode("div", None, [HTMLNode("p", "Hello World")])
        self.assertEqual(node.__repr__(), "HTMLNode(div,None,[HTMLNode(p,Hello World,None,None)],None)")
    
    def test_repr_with_multiple_children(self):
        node = HTMLNode("div", None, [HTMLNode("p", "Hello World"), HTMLNode("p", "Hello World")])
        self.assertEqual(node.__repr__(), "HTMLNode(div,None,[HTMLNode(p,Hello World,None,None), HTMLNode(p,Hello World,None,None)],None)")
    
    def test_repr_with_attrs(self):
        node = HTMLNode("p", "Hello World", None, {"class":"text"})
        self.assertEqual(node.__repr__(), "HTMLNode(p,Hello World,None,{'class': 'text'})")
    




        

if __name__ == "__main__":
    unittest.main()

