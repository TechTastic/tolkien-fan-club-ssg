from enum import Enum
import re

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