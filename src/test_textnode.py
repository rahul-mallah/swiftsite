import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        self.assertEqual(node.url, node2.url)

    def test_false(self):
        node = TextNode("This is node1", TextType.BOLD_TEXT)
        node2 = TextNode("This is node2", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_false_2(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertIsNone(node.url)
        self.assertNotIn(node.text_type, [TextType.LINK, TextType.IMAGE])
      
    def test_false_3(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
