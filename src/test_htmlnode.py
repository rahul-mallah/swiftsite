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

    # Test Leaf Node
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
    
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "url/of/image.jpg", "alt": "Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')
    
    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")

    # Test Parent Node
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parent(self):
        grandchild_node = ParentNode("p", [LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            child_node = ParentNode("span", [])
            child_node.to_html()

        with self.assertRaises(ValueError) as context2:
            child_node = ParentNode("span", None)
            child_node.to_html()
        self.assertEqual(
            str(context.exception),
            "Parent node must have children",
        )
        self.assertEqual(
            str(context2.exception),
            "Parent node must have children",
        )
    
    def test_to_html_with_nested_parent2(self):
        grandchild_node = ParentNode("p", [LeafNode("b", "Bold text"),
                ParentNode("b", [LeafNode(None, "bold text"),
                ParentNode("i", [LeafNode("u","bold, italic and underline")])]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>Bold text</b><b>bold text<i><u>bold, italic and underline</u></i></b><i>italic text</i>Normal text</p></span></div>",
        )

if __name__ == "__main__":
    unittest.main()