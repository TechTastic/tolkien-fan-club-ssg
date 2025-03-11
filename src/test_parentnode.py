import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("i", "great grandchild")
        grandchild_node = ParentNode("p", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><i>great grandchild</i></p></span></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "first child")
        child_node2 = LeafNode(None, "second child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>first child</span>second child</div>")

    def test_to_html_with_multiple_grandchildren_and_great_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        great_grandchild_node = LeafNode("h1", "first great grandchild")
        great_grandchild_node2 = LeafNode(None, "second great grandchild")
        grandchild_node2 = ParentNode("p", [great_grandchild_node, great_grandchild_node2])
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><p><h1>first great grandchild</h1>second great grandchild</p></span></div>",
        )