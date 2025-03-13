import unittest

from textnode import TextNode, TextType
import markdown_inline


class TestTextNode(unittest.TestCase):
    def test_bold_delimiter(self):
        single = TextNode("This is a **bold** statement", TextType.TEXT)
        double = TextNode("This is a **bold** statement and another **bold** statement", TextType.TEXT)
        invalid = TextNode("This is an **invalid statement", TextType.TEXT)
        invalid2 = TextNode("This is **also** an **invalid statement", TextType.TEXT)

        self.assertEqual(markdown_inline.split_node_delimiter([single], "**", TextType.BOLD), [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement", TextType.TEXT)
        ])

        self.assertEqual(markdown_inline.split_node_delimiter([double], "**", TextType.BOLD), [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement", TextType.TEXT)
        ])

        try:
            markdown_inline.split_node_delimiter([invalid], "**", TextType.BOLD)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '**' in 'This is an **invalid statement'")

        try:
            markdown_inline.split_node_delimiter([invalid2], "**", TextType.BOLD)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '**' in 'This is **also** an **invalid statement'")

    def test_italic_delimiter(self):
        single = TextNode("This is an _italic_ statement", TextType.TEXT)
        double = TextNode("This is an _italic_ statement and another _italic_ statement", TextType.TEXT)
        invalid = TextNode("This is an _invalid statement", TextType.TEXT)
        invalid2 = TextNode("This is _also_ an _invalid statement", TextType.TEXT)

        self.assertEqual(markdown_inline.split_node_delimiter([single], "_", TextType.ITALIC), [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" statement", TextType.TEXT)
        ])

        self.assertEqual(markdown_inline.split_node_delimiter([double], "_", TextType.ITALIC), [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" statement and another ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" statement", TextType.TEXT)
        ])

        try:
            markdown_inline.split_node_delimiter([invalid], "_", TextType.ITALIC)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '_' in 'This is an _invalid statement'")

        try:
            markdown_inline.split_node_delimiter([invalid2], "_", TextType.ITALIC)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '_' in 'This is _also_ an _invalid statement'")

    def test_code_delimiter(self):
        single = TextNode("This is a `code` statement", TextType.TEXT)
        double = TextNode("This is a `code` statement and another `code` statement", TextType.TEXT)
        invalid = TextNode("This is an `invalid statement", TextType.TEXT)
        invalid2 = TextNode("This is `also` an `invalid statement", TextType.TEXT)

        self.assertEqual(markdown_inline.split_node_delimiter([single], "`", TextType.CODE), [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" statement", TextType.TEXT)
        ])

        self.assertEqual(markdown_inline.split_node_delimiter([double], "`", TextType.CODE), [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" statement and another ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" statement", TextType.TEXT)
        ])

        try:
            markdown_inline.split_node_delimiter([invalid], "`", TextType.CODE)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '`' in 'This is an `invalid statement'")

        try:
            markdown_inline.split_node_delimiter([invalid2], "`", TextType.CODE)
        except Exception as e:
            self.assertEqual(f"{e}", "Invalid markdown syntax, missing closing '`' in 'This is `also` an `invalid statement'")
    
    def test_extract_markdown_images(self):
        matches = markdown_inline.extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_markdown_link(self):
        matches = markdown_inline.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and this is a ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

        matches = markdown_inline.extract_markdown_links("[to boot dev](https://www.boot.dev)")
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])


if __name__ == "__main__":
    unittest.main()