import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_not_eq_and_eq(self):
        for first_type in TextType:
            first_url = None
            if first_type == TextType.LINK:
                first_url = "https://www.boot.dev"
            for second_type in TextType:
                second_url = None
                if second_type == TextType.LINK:
                    second_url = "https://www.boot.dev"

                first_node = TextNode(f"This is a {first_type.value} node", first_type, first_url)
                second_node = TextNode(f"This is a {second_type.value} node", second_type, second_url)

                if first_type == second_type:
                    self.assertEqual(first_node, second_node)
                else:
                    self.assertNotEqual(first_node, second_node)
    
    def test_print(self):
        for text_type in TextType:
            url = None
            if text_type == TextType.LINK:
                url = "https://www.boot.dev"
            node = TextNode(f"This is a {text_type.value} node", text_type, url)
            self.assertEqual(f"{node}", f"TextNode(This is a {text_type.value} node, {text_type}, {url})")
    
    def test_html_conversion(self):
        text_node = TextNode("This is normal text", TextType.TEXT)
        leaf_node = LeafNode(None, "This is normal text")
        self.assertEqual(f"{TextNode.text_node_to_html_node(text_node)}", f"{leaf_node}")

        text_node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        leaf_node = LeafNode("a", "This is a link", {"href": "https://www.boot.dev"})
        self.assertEqual(f"{TextNode.text_node_to_html_node(text_node)}", f"{leaf_node}")


if __name__ == "__main__":
    unittest.main()