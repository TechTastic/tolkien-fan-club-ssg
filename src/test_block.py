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
- with normal items
- and **bolded** items
- and _italic_ items

1. This is an ordered list
2. with normal items
3. and **bolded** items
4. and _italic_ items!

> This is a quote
> This is the same quote

```python
def main():
    print(\"Hello World\")
main()
```
"""

    def test_markdown_to_blocks(self):
        blocks = block.markdown_to_blocks(TestBlock.md)
        self.assertEqual(
            blocks,
            [
                '# This is a heading',
                'This is **bolded** paragraph',
                'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line',
                '- This is a unordered list\n- with normal items\n- and **bolded** items\n- and _italic_ items',
                '1. This is an ordered list\n2. with normal items\n3. and **bolded** items\n4. and _italic_ items!',
                '> This is a quote\n> This is the same quote',
                '```python\ndef main():\n    print("Hello World")\nmain()\n```'
            ]
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
    
    def test_markdown_to_html_node(self):
        html = block.markdown_to_html_node(TestBlock.md).to_html()
        self.maxDiff = None
        self.assertEqual(
            html, 
            "<div><h1># This is a heading</h1><p>This is<b>bolded</b>paragraph</p><p>This is another paragraph with<i>italic</i>text and<pre><code>code</code></pre>here\nThis is the same paragraph on a new line</p><ul><li>This is a unordered list</li><li>with normal items</li><li>and<b>bolded</b>items</li><li>and<i>italic</i>items</li></ul><ol><li>This is an ordered list</li><li>with normal items</li><li>and<b>bolded</b>items</li><li>and<i>italic</i>items!</li></ol><blockquote>This is a quote\nThis is the same quote</blockquote><pre><code>def main():\n    print(\"Hello World\")\nmain()</code></pre></div>"
        )