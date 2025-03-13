import unittest

from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HTMLNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        children = [
            LeafNode("b", "This is bold"),
            ParentNode("a", [LeafNode("b", "This is a bold link")], {"href": "https://www.boot.dev"}),
            ParentNode("b", [ParentNode("i", [LeafNode(None, "This is bold and italic")])])
        ]
        parent = ParentNode("div", children)
        html = HTMLNode("div", children=children)
        self.assertEqual(f"{parent}", f"{html}")
    
    def test_to_html(self):
        children = [
            LeafNode("b", "This is bold"),
            ParentNode("a", [LeafNode("b", "This is a bold link")], {"href": "https://www.boot.dev"}),
            ParentNode("b", [ParentNode("i", [LeafNode(None, "This is bold and italic")])])
        ]
        parent = ParentNode("div", children)
        self.assertEqual(parent.to_html(), "<div><b>This is bold</b><a href=\"https://www.boot.dev\"><b>This is a bold link</b></a><b><i>This is bold and italic</i></b></div>")
    
    def test_error(self):
        try:
            ParentNode("div", None).to_html()
            ParentNode("div", []).to_html()
        except ValueError as e:
            self.assertEqual(f"{e}", "All parent nodes need children")
        
        try:
            ParentNode(None, []).to_html()
        except ValueError as e:
            self.assertEqual(f"{e}", "All parent nodes need a tag")