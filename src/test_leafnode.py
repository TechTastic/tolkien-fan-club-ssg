import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_node_p(self):
        node = LeafNode("p", "Lorum ipsum")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Lorum ipsum")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "<p>Lorum ipsum</p>")

    def test_leaf_node_h1(self):
        node = LeafNode("h1", "Lorum ipsum")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Lorum ipsum")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "<h1>Lorum ipsum</h1>")

    def test_leaf_node_h1(self):
        node = LeafNode("a", "Lorum ipsum", {"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Lorum ipsum")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"https://boot.dev\">Lorum ipsum</a>")

    def test_leaf_node_none(self):
        node = LeafNode(None, "Lorum ipsum")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Lorum ipsum")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "Lorum ipsum")