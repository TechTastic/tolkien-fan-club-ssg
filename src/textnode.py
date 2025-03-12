import re
from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href":self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":self.url, "alt":self.text})
    
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
    
    def extract_markdown_images(text):
        return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    
    def extract_markdown_links(text):
        return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
    
    def split_nodes_image(old_nodes):
        new_nodes = []
        for node in old_nodes:
            matches = TextNode.extract_markdown_images(node.text)
            
            if not matches:
                return old_nodes

            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            
            text = node.text
            for match in matches:
                alt_text = match[0]
                image_url = match[1]
                splitter = f"![{alt_text}]({image_url})"

                split = text.split(splitter)

                before = split[0]
                if before:
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

                text = text.replace(before + splitter, "")
        return new_nodes

    def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            matches = TextNode.extract_markdown_links(node.text)
            
            if not matches:
                return old_nodes

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
                if before:
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(wrapped_text, TextType.LINK, link_url))

                text = text.replace(before + splitter, "")
        return new_nodes