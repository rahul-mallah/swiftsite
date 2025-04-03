import unittest

from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "alt": "Testing"
        }
        node = HTMLNode("h1", "Header One",[], props)
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\" alt=\"Testing\"",
        node.props_to_html())
        self.assertNotEqual(" href=\"https://www.boot.dev\" target=\"_blank\" alt=\"Testing\"",
        node.props_to_html())
        
    
    def test_values(self):
        node = HTMLNode("h1","Header One",[], {"alt": "Testing"})
        node2 = HTMLNode("h1","Header One",[], {"alt": "Testing"})
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_repr(self):
        node = HTMLNode("h1","Header One", [], {"alt": "Testing"})
        self.assertEqual("HTMLNode(h1, Header One, [], {'alt': 'Testing'})", repr(node))

if __name__ == "__main__":
    unittest.main()