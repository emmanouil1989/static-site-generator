import unittest
from nodes_utils import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word and ", TextType.NORMAL_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded word", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        node = extract_markdown_images(text)
        self.assertEqual(
            node,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
        )

    def test_delim_link(self):
        text = "This is text with a [link](https://www.google.com) and [another link](https://www.google.com)"

        node = extract_markdown_links(text)
        self.assertEqual(
            node,
            [("link", "https://www.google.com"), ("another link", "https://www.google.com")],
        )

    def test_delim_image(self):
        node = TextNode(
            "This is text with a link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) or ![obi wan](https://i.imgur.com/fJRm)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("obi wan", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" or ", TextType.NORMAL_TEXT),
                TextNode("obi wan", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm")
            ],
            new_nodes,
        )
    
    def test_delim_image_with_two_images_at_the_start(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some text here",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode('obi wan', TextType.IMAGE_TEXT, 'https://i.imgur.com/fJRm4Vk.jpeg'),
                TextNode(' some text here', TextType.NORMAL_TEXT)
            ],
            new_nodes,
        )

    def test_delim_with_two_images_at_the_end(self):
        node = TextNode(
            "some text here ![rick roll](https://i.imgur.com/aKaOqIh.gif) ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("some text here ", TextType.NORMAL_TEXT),
                TextNode("rick roll", TextType.IMAGE_TEXT, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode('obi wan', TextType.IMAGE_TEXT, 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            new_nodes,
        )
    
    def test_delim_with_two_images_at_the_end_and_start(self):
        node = TextNode(
            "![rick roll](https//i.imgur.com/aKaOqIh.gif) some text here ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE_TEXT, "https//i.imgur.com/aKaOqIh.gif"),
                TextNode(' some text here ', TextType.NORMAL_TEXT),
                TextNode('obi wan', TextType.IMAGE_TEXT, 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            new_nodes,
        )

    def test_delim_with_two_images_at_the_end_and_start_and_middle(self):
        node = TextNode(
            "![rick roll](https//i.imgur.com/aKaOqIh.gif) ![rick roll](https//i.imgur.com/aKaOqIh.gif) ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE_TEXT, "https//i.imgur.com/aKaOqIh.gif"),
                TextNode("rick roll", TextType.IMAGE_TEXT, "https//i.imgur.com/aKaOqIh.gif"),
                TextNode('obi wan', TextType.IMAGE_TEXT, 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("obi wan", TextType.LINK_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )

    def test_split_link_with_two_links_at_the_start(self):
        node = TextNode(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif) [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some text here",
            TextType.NORMAL_TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode("obi wan", TextType.LINK_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" some text here", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_split_link_with_two_links_at_the_end(self):
        node = TextNode(
            "some text here [rick roll](https://i.imgur/aKaOqIh.gif) [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.NORMAL_TEXT,

        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("some text here ", TextType.NORMAL_TEXT),
                TextNode("rick roll", TextType.LINK_TEXT, "https://i.imgur/aKaOqIh.gif"),
                TextNode("obi wan", TextType.LINK_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE_TEXT, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ],
            nodes,
        )
    
    def test_text_to_textnodes_with_just_text(self):
        text = "This is text with no markdown"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with no markdown", TextType.NORMAL_TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_with_one_image_and_bold_text(self):
        text = "This is **text** with an ![obi wan image](https://i.imgur.com/ffJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/ffJRm4Vk.jpeg"),
            ],
            nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ],
            nodes,
        )
    
    def test_text_to_textnodes_with_just_text(self):
        text = "This is text with no markdown"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with no markdown", TextType.NORMAL_TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_with_one_image_and_bold_text(self):
        text = "This is **text** with an ![obi wan image](https://i.imgur.com/ffJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/ffJRm4Vk.jpeg"),
            ],
            nodes,
        )

    def test_text_to_textnodes_with_one_link_one_bold_and_one_italic(self):
        text = "This is **text** with an [obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and *italic*"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.LINK_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            nodes,
        )
    
    if __name__ == "__main__":
        unittest.main()

  