import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_to_html_without_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")
    def test_to_html_with_paragraph(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")
    def test_to_html_with_link_tag(self):
        node = LeafNode("a", "Google", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_to_html_when_props_without_tag(self):
        node = LeafNode(None, "Hello World", {"class":"text"})
        self.assertEqual(node.to_html(), "Hello World")
    

if __name__ == "__main__":
    unittest.main()