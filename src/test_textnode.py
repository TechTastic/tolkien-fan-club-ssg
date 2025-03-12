import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)


    
    def test_text(self):
        node = TextNode("This is a normal text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a normal text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://boot.dev")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href":"https://boot.dev"})
    
    def test_image(self):
        image = "https://media.discordapp.net/attachments/920333580729741432/1348969052021723187/48f1f1e0b66a0627.png?ex=67d164d4&is=67d01354&hm=7762355230b57ecaf5dd4a59d2e573438167e27226f30e4a1f1702ba62297e03&=&format=webp&quality=lossless"
        node = TextNode("This is an image text node", TextType.IMAGE, image)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": image, "alt": "This is an image text node"})

    
    
    def test_markdown_parsing_bold(self):
        nodes = [
            TextNode("**This** is bold!", TextType.TEXT),
            TextNode("_This_ is italicized!", TextType.TEXT),
            TextNode("`This` is an inline code block!", TextType.TEXT)
        ]
        new_nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        new_nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
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
        new_nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)
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
        bold_nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        italic_nodes = TextNode.split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
        code_nodes = TextNode.split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
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
        nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)
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
        nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(nodes, [
            TextNode("This", TextType.CODE),
            TextNode(" is an inline code block and ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" is italicized and ", TextType.TEXT),
            TextNode("this", TextType.BOLD),
            TextNode(" is bold!", TextType.TEXT)
        ])



    def test_extract_markdown_images(self):
        self.assertEqual(TextNode.extract_markdown_images("This is an image! ![alt text](https://thisi.san/image.png)"), [("alt text", "https://thisi.san/image.png")])

    def test_extract_markdown_links(self):
        self.assertEqual(TextNode.extract_markdown_links("This is a [link](https://boot.dev)!"), [("link", "https://boot.dev")])

    

    def test_markdown_parsing_image(self):
        node = TextNode("This is text with ![first image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        self.assertEqual(TextNode.split_nodes_image([node]), [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("first image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ])

    def test_markdown_parsing_link(self):
        node = TextNode("This is text with a [link](https://boot.dev) and another [link](https://boot.dev)", TextType.TEXT)
        self.assertEqual(TextNode.split_nodes_link([node]), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])

if __name__ == "__main__":
    unittest.main()