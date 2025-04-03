import unittest

from leafnode import *

class Test_LeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello world!")
        self.assertEqual(node.to_html(), "<b>Hello world!</b>")
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello world!")
        self.assertEqual(node.to_html(), "<h1>Hello world!</h1>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")
    

if __name__ == "__main__":
    unittest.main()