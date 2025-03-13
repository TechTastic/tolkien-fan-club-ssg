import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_code(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"invalid markdown syntax: {node.text}")
        
        texts = node.text.split(delimiter)
        for i in range(0, len(texts)):
            text = texts[i]
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def split_nodes_bold(old_nodes):
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

def split_nodes_italic(old_nodes):
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

def split_nodes_code(old_nodes):
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)

        if node.text_type != TextType.TEXT or not matches:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            splitter = f"![{alt_text}]({image_url})"

            split = text.split(splitter, 1)

            before = split[0]
            if before:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            text = text.replace(before + splitter, "")
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        
        if not matches:
            new_nodes.append(node)
            continue
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            wrapped_text = match[0]
            link_url = match[1]
            splitter = f"[{wrapped_text}]({link_url})"

            split = text.split(splitter)

            before = split[0]
            print(f"Before: {before}")
            if before:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(wrapped_text, TextType.LINK, link_url))

            text = text.replace(before + splitter, "")
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes