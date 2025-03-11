import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("h1", "Lorum ipsum", [], {})
        self.assertEqual(node.tag, "h1")

    def test_none_tag(self):
        node = HTMLNode(value="Lorum ipsum", children=[], props={})
        self.assertEqual(node.tag, None)

    def test_value(self):
        node = HTMLNode("h1", "Lorum ipsum", [], {})
        self.assertEqual(node.value, "Lorum ipsum")

    def test_none_value(self):
        node = HTMLNode(tag="h1", children=[], props={})
        self.assertEqual(node.value, None)
    
    def test_children(self):
        node = HTMLNode("h1", "Lorum ipsum", [], {})
        self.assertEqual(node.children, [])

    def test_none_children(self):
        node = HTMLNode(tag="h1", value="Lorum ipsum", props={})
        self.assertEqual(node.children, None)
    
    def test_props(self):
        node = HTMLNode("h1", "Lorum ipsum", [], {})
        self.assertEqual(node.props, {})

    def test_none_props(self):
        node = HTMLNode("h1", "Lorum ipsum", [])
        self.assertEqual(node.props, None)