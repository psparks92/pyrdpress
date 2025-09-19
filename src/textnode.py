import re
from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT="text"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMAGE="image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    
    def __eq__(self, otherNode):
        return (self.text == otherNode.text
                and self.text_type == otherNode.text_type
                and self.url == otherNode.url)

    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type.value}, {self.url})"

def text_node_to_html_node(textnode):
    match (textnode.text_type):
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href":textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":textnode.url, "alt":textnode.text})
        case _:
            raise ValueError("")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        split_nodes = []
        split = node.text.split(delimiter)
        i = 0
        for val in split:
            if i % 2 == 0:
                new_nodes.append(TextNode(val, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(val, text_type))
            i += 1
    return new_nodes
        
def extract_markdown_images(text):
    img_with_alt_regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(img_with_alt_regex, text)
    results = []
    for match in matches:
        results.append((match[0],match[1]))
    return results

def extract_markdown_links(text):
    link_with_desc_regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_with_desc_regex, text)
    results = []
    for match in matches:
        results.append((match[0],match[1]))
    return results


def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        text = node.text
        imgs = extract_markdown_images(text)
        for image in imgs:
            img_text = f"![{image[0]}]({image[1]})"
            split = text.split(img_text, 1)
            before = split[0]
            if len(before) > 0:
                nodes.append(TextNode(before, node.text_type, node.url))
            nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = text[len(before) + len(img_text):]
        if len(text) > 0:
            nodes.append(TextNode(text, TextType.TEXT))
    return nodes



def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)
        for link in matches:
            link_text = f"[{link[0]}]({link[1]})"
            split = text.split(link_text, 1)
            before = split[0]
            if len(before) > 0:
                nodes.append(TextNode(before, node.text_type, node.url))
            nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = text[len(before) + len(link_text):]
        if len(text) > 0:
            nodes.append(TextNode(text, node.text_type, node.url))
    return nodes

def text_to_textnodes(text):
    init_node = TextNode(text, TextType.TEXT)
    nodes = [init_node]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

