import unittest

import block
from block import BlockType

class TestBlock(unittest.TestCase):
    md = """
# This is a heading


This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a unordered list
- with items


1. This is an ordered list
2. with items


> This is a quote
> This is the same quote


```python
# This is code
```
"""

    def test_markdown_to_blocks(self):
        blocks = block.markdown_to_blocks(TestBlock.md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a unordered list\n- with items",
                "1. This is an ordered list\n2. with items",
                "> This is a quote\n> This is the same quote",
                "```python\n# This is code\n```"
            ],
        )
    
    def test_block_to_block_type(self):
        blocks = block.markdown_to_blocks(TestBlock.md)
        
        self.assertEqual(BlockType.HEADING, block.block_to_block_type(blocks[0]))
        self.assertEqual(BlockType.PARAGRAPH, block.block_to_block_type(blocks[1]))
        self.assertEqual(BlockType.PARAGRAPH, block.block_to_block_type(blocks[2]))
        self.assertEqual(BlockType.UNORDERED, block.block_to_block_type(blocks[3]))
        self.assertEqual(BlockType.ORDERED, block.block_to_block_type(blocks[4]))
        self.assertEqual(BlockType.QUOTE, block.block_to_block_type(blocks[5]))
        self.assertEqual(BlockType.CODE, block.block_to_block_type(blocks[6]))