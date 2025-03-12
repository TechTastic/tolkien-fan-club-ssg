import unittest

from textnode import TextNode, TextType
import inline


class TestTextNode(unittest.TestCase):
    def test_markdown_parsing_bold(self):
        nodes = [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ]
        new_nodes = inline.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This", TextType.BOLD),
            TextNode(" is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ])
    
    def test_markdown_parsing_italic(self):
        nodes = [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ]
        new_nodes = inline.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("This", TextType.ITALIC),
            TextNode(" is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ])
    
    def test_markdown_parsing_code(self):
        nodes = [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ]
        new_nodes = inline.split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("This", TextType.CODE),
            TextNode(" is an inline code block!", TextType.TEXT)
        ])
    
    def test_markdown_parsing_all(self):
        nodes = [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ]
        bold_nodes = inline.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        italic_nodes = inline.split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
        code_nodes = inline.split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
        self.assertEqual(code_nodes, [
            TextNode("This", TextType.BOLD),
            TextNode(" is bold!", TextType.TEXT),
            TextNode("This", TextType.ITALIC),
            TextNode(" is italicized!", TextType.TEXT),
            TextNode("This", TextType.CODE),
            TextNode(" is an inline code block!", TextType.TEXT)
        ])
    
    def test_markdown_parsing_all_again(self):
        nodes = [
            TextNode("**This** is bold and _this_ is italicized and `this` is an inline code block!", TextType.TEXT)
        ]
        nodes = inline.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = inline.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = inline.split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(nodes, [
            TextNode("This", TextType.BOLD),
            TextNode(" is bold and ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" is italicized and ", TextType.TEXT),
            TextNode("this", TextType.CODE),
            TextNode(" is an inline code block!", TextType.TEXT)
        ])

    def test_markdown_parsing_all_again_reversed(self):
        nodes = [
            TextNode("`This` is an inline code block and _this_ is italicized and **this** is bold!", TextType.TEXT)
        ]
        nodes = inline.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = inline.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = inline.split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(nodes, [
            TextNode("This", TextType.CODE),
            TextNode(" is an inline code block and ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" is italicized and ", TextType.TEXT),
            TextNode("this", TextType.BOLD),
            TextNode(" is bold!", TextType.TEXT)
        ])



    def test_extract_markdown_images(self):
        self.assertEqual(inline.extract_markdown_images("This is an image! ![alt text](https://thisi.san/image.png)"), [("alt text", "https://thisi.san/image.png")])

    def test_extract_markdown_links(self):
        self.assertEqual(inline.extract_markdown_links("This is a [link](https://boot.dev)!"), [("link", "https://boot.dev")])

    

    def test_markdown_parsing_image(self):
        node = TextNode("This is text with ![first image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        self.assertEqual(inline.split_nodes_image([node]), [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("first image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ])

    def test_markdown_parsing_link(self):
        node = TextNode("This is text with a [link](https://boot.dev) and another [link](https://boot.dev)", TextType.TEXT)
        self.assertEqual(inline.split_nodes_link([node]), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])
    
    def test_markdown_parsing_full(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        bold_nodes = inline.split_nodes_delimiter([node], "**", TextType.BOLD)
        italic_nodes = inline.split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
        code_nodes = inline.split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
        image_nodes = inline.split_nodes_image(code_nodes)
        link_nodes = inline.split_nodes_link(image_nodes)

        self.assertEqual(link_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])