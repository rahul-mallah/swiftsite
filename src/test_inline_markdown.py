import unittest
from inline_markdown import *

class Test_Inline_Markdown(unittest.TestCase):
    def test_split_nodes_delimiter_block(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.NORMAL_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_block(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("bolded phrase", TextType.BOLD_TEXT),
            TextNode(" in the middle", TextType.NORMAL_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("italic block", TextType.ITALIC_TEXT),
            TextNode(" word", TextType.NORMAL_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_multiple_italic(self):
        node = TextNode("This is text with a _italic block_ or _second italic_ or _third italic_", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("italic block", TextType.ITALIC_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("second italic", TextType.ITALIC_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("third italic", TextType.ITALIC_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_multiple_bold(self):
        node = TextNode("This is text with a **bold block** or **second bold** or **third bold**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("bold block", TextType.BOLD_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("second bold", TextType.BOLD_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("third bold", TextType.BOLD_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_code(self):
        node = TextNode("This is text with a `code block` or `second code` or `third code`", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("second code", TextType.CODE_TEXT),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("third code", TextType.CODE_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("`code block``code block``code block``code block`", TextType.NORMAL_TEXT)
        node1 = TextNode("**code block****code block****code block****code block**", TextType.NORMAL_TEXT)
        node2 = TextNode("_code block__code block__code block__code block_", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "**", TextType.BOLD_TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC_TEXT)
        expected_nodes = [
            TextNode("code block", TextType.CODE_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
        ]
        expected_nodes1 = [
            TextNode("code block", TextType.BOLD_TEXT),
            TextNode("code block", TextType.BOLD_TEXT),
            TextNode("code block", TextType.BOLD_TEXT),
            TextNode("code block", TextType.BOLD_TEXT),
        ]
        expected_nodes2 = [
            TextNode("code block", TextType.ITALIC_TEXT),
            TextNode("code block", TextType.ITALIC_TEXT),
            TextNode("code block", TextType.ITALIC_TEXT),
            TextNode("code block", TextType.ITALIC_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        self.assertEqual(new_nodes1, expected_nodes1)
        self.assertEqual(new_nodes2, expected_nodes2)
    
    def test_split_nodes_delimiter_not_closed_delimiter(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("`code block``code block``code block``code block", TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            str(context.exception),
            "Markdown Syntax Error: Closing delimiter not found",
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty_space(self):
        node = TextNode(
            "   ![image](https://i.imgur.com/zjjcJKZ.png)    ![second image](https://i.imgur.com/3elNhQu.png)     ![third image](https://i.imgur.com/3elNhQu.png) text",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" text", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_space(self):
        node = TextNode(
            "   [to boot dev](https://www.boot.dev)    [to youtube](https://www.youtube.com/@bootdotdev)     [to youtube](https://www.youtube.com/@bootdotdev) text",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" text", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_split_images_mixed(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) [to boot dev](https://www.boot.dev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" [to boot dev](https://www.boot.dev)", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_mixed(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected_result = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected_result)

    def test_text_to_textnodes_random_order(self):
        result = text_to_textnodes("This [link](https://boot.dev) is **link** with an _image_![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block`")
        expected_result = [
            TextNode("This ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" is ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.ITALIC_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
        ]
        self.assertListEqual(result, expected_result)

    def test_text_to_textnodes_consecutive_special_nodes(self):
        result = text_to_textnodes("Hello _world_ **bold** `code` end")
        expected_result = [
            TextNode("Hello ", TextType.NORMAL_TEXT),
            TextNode("world", TextType.ITALIC_TEXT),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" end", TextType.NORMAL_TEXT),
        ]
        self.assertListEqual(result, expected_result)