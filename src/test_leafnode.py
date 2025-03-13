import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode("b", "This is bold")
        html = HTMLNode("b", "This is bold")
        self.assertEqual(f"{leaf}", f"{html}")

        leaf = LeafNode("a", "Boot.Dev", {"href": "https://www.boot.dev"})
        html = HTMLNode("a", "Boot.Dev", props={"href": "https://www.boot.dev"})
        self.assertEqual(f"{leaf}", f"{html}")
    
    def test_to_html(self):
        leaf = LeafNode("b", "This is bold")
        self.assertEqual(leaf.to_html(), "<b>This is bold</b>")

        leaf = LeafNode("a", "Boot.Dev", {"href": "https://www.boot.dev"})
        self.assertEqual(leaf.to_html(), "<a href=\"https://www.boot.dev\">Boot.Dev</a>")