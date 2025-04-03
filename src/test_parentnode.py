import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class Test_ParentNode(unittest.TestCase):
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