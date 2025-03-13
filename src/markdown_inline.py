import re

from textnode import TextNode, TextType

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        
        split_texts = node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax, missing closing '{delimiter}' in '{node.text}'")
        
        for i in range(0, len(split_texts)):
            text = split_texts[i]
            new_node = None
            if i % 2 == 0:
                new_node = TextNode(text, TextType.TEXT)
            else:
                new_node = TextNode(text, text_type)
            new_nodes.append(new_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^\!]\[(.*?)\]\((.*?)\)", text)