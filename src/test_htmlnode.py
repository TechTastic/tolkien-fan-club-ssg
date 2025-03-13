import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("p", "Lorum ipsum")
        self.assertEqual(f"{node}", "HTMLNode(p, Lorum ipsum, None, None)")

        node2 = HTMLNode("a", "Boot.Dev", props={"href":"https://www.boot.dev"})
        self.assertEqual(f"{node2}", "HTMLNode(a, Boot.Dev, None, {'href': 'https://www.boot.dev'})")
    
    def test_props(self):
        node = HTMLNode("a", "Boot.Dev", props={"href":"https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\"")

        node = HTMLNode("p", "Lorum ipsum", props={})
        self.assertEqual(node.props_to_html(), "")

        node = HTMLNode("p", "Lorum ipsum")
        self.assertEqual(node.props_to_html(), "")