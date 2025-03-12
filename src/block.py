from enum import Enum
import re

import inline
from textnode import TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"
    PARAGRAPH = "parargraph"

def markdown_to_blocks(markdown):
    return list(filter(lambda t: t, map(lambda t: t.strip(), markdown.split("\n\n"))))

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED
    return BlockType.PARAGRAPH

    # For posterities sake, I am leaving in my solution
    # The Enum had also saved the Regex expressions I used but I've now stripped that away
    '''
    for type in BlockType:
        matches = re.findall(type.value[1], block)
        if not matches:
            continue
        match type:
            case BlockType.HEADING | BlockType.CODE | BlockType.QUOTE | BlockType.UNORDERED:
                if len(matches) > 1:
                    continue
                return type

            case BlockType.ORDERED:
                counter = 0
                is_ordered = True
                for i in range(1, len(matches)):
                    match = matches[i - 1]
                    if (not match[0].startswith(". ", 1)) or i != match[1] or counter - 1 != match[i]:
                        is_ordered = False
                        break
                    counter = i
                if not is_ordered:
                    continue
                return type

            case _:
                return BlockType.PARAGRAPH
    '''

def markdown_to_html_node(markdown):
    main_children = []

    blocks = markdown_to_blocks(markdown)
    for bl in blocks:
        parsed_children = parse_inline_markdown_formatting(bl)
        match block_to_block_type(bl):
            case BlockType.HEADING:
                main_children.append(ParentNode(f"h{bl.count("#")}", parsed_children))
            case BlockType.CODE:
                main_children.append(ParentNode("pre", [to_code_text_node(bl)]))
            case BlockType.QUOTE:
                main_children.append(ParentNode("blockquote", parsed_children))
            case BlockType.UNORDERED:
                main_children.append(to_unordered_list(bl))
            case BlockType.ORDERED:
                main_children.append(to_ordered_list(bl))
            case BlockType.PARAGRAPH:
                main_children.append(ParentNode("p", parsed_children))

    return ParentNode("div", main_children)

def to_code_text_node(code):
    split = code.split("\n")
    return TextNode("\n".join(split[1:len(split) - 1]), TextType.CODE).to_html_node()

def parse_inline_markdown_formatting(text):
    nodes = inline.text_to_textnodes(text)
    nodes = list(map(lambda node: TextNode(node.text.replace("> ", "").strip(), node.text_type, node.url).to_html_node(), nodes))
    nodes = list(map(lambda node: ParentNode("pre", [node]) if node.tag == "code" else node, nodes))
    return nodes

def to_unordered_list(text):
    children = []
    items = text.split("- ")
    for item in items:
        if not item:
            continue
        children.append(ParentNode("li", parse_inline_markdown_formatting(item)))
    return ParentNode("ul", children)

def to_ordered_list(text):
    children = []
    items = text.split("\n")
    for i in range(0, len(items)):
        item = items[i].replace(f"{i + 1}. ", "")
        children.append(ParentNode("li", parse_inline_markdown_formatting(item)))
    return ParentNode("ol", children)