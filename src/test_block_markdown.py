import unittest
from block_markdown import *

class Test_Block_Markdown(unittest.TestCase):

    # markdown to blocks function
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_lines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )

    # Test Block to block type function
    def test_block_to_block_type(self):
        md = """
###### This is **bolded** Header

More more mroe mroe more mroe more more more mroe more mroe mroe
mroe mroe more mroe more mroe mroe more more more

```More more mroe mroe more mroe more more more mroe more mroe mroe
mroe mroe more mroe more mroe mroe more more more ```

>This is another paragraph with _italic_ text and `code` here
>This is the same paragraph on a new line

- This is a list
- with items
- This is a list
- with items

1. This is a list
2. with items
3. This is a list
4. with items
"""
        blocks = markdown_to_blocks(md)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        
        self.assertListEqual(result, [BlockType.HEADING, BlockType.PARAGRAPH, BlockType.CODE,
        BlockType.QUOTE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST])

    def test_block_to_block_type_false_positives(self):
        md = """
####### This is **bolded** Header

```More more mroe mroe more mroe more more more mroe more mroe mroe
mroe mroe more mroe more mroe mroe more more more ``

>This is another paragraph with _italic_ text and `code` here
<This is the same paragraph on a new line

- This is a list
+ with items
- This is a list
- with items

1. This is a list
2. with items
4. This is a list
4. with items
"""
        blocks = markdown_to_blocks(md)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        
        self.assertListEqual(result, [BlockType.PARAGRAPH, BlockType.PARAGRAPH,
        BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.PARAGRAPH])


if __name__ == "__main__":
    unittest.main()