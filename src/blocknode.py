import re
from enum import Enum
from textnode import *
from parentnode import *
from leafnode import *
import os

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UL="unordered_list"
    OL="ordered_list"

def get_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    elif (len(markdown) > 5 
          and markdown[:3] == "```" 
          and markdown[-3:] == "```"):
        return BlockType.CODE
    elif all(list(map(lambda l: len(l) >= 1 and l[0] == ">", markdown.split("\n")))):
        return BlockType.QUOTE
    elif all(list(map(lambda l: len(l) > 2 and l[:2] == "- ", markdown.split("\n")))):
        print("FOUND UL")
        return BlockType.UL
    else:
        current_index = 1
        for line in markdown.split("\n"):
            if (len(line) < 2
                    or not line.startswith(f"{current_index}.")):
                return BlockType.PARAGRAPH
            current_index += 1
        return BlockType.OL
    return BlockType.PARAGRAPH


def markdown_to_blocks(md):
    return list(filter(lambda a: len(a.strip()) > 0, map(lambda b: b.strip(), md.split("\n\n"))))

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = get_block_type(block)
        tag = node_type_to_tag(block_type, text_to_children(block))
        if block_type == BlockType.CODE:
            child = LeafNode("code", trim_tag(block, block_type))
            html_node = ParentNode(tag, [child])
            nodes.append(html_node)
        else:
            children = text_to_children(trim_tag(block, block_type))
            html_node = ParentNode(tag, children)
            nodes.append(html_node)
    parent = ParentNode("div", nodes)
    return parent



def text_to_children(text):
    nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        nodes.append(html_node)
    return nodes
    
def trim_tag(text, type):
    match (type):
        case BlockType.PARAGRAPH:
            return text.replace("\n"," ")
        case BlockType.HEADING:
            while text[0] == "#":
                text = text[1:]
            return text
        case BlockType.CODE:
            return text[4:-3]
        case BlockType.QUOTE:
            return "\n".join(map(lambda l: l[2:], text.split("\n")))
        case BlockType.UL:
            return "\n".join(map(lambda l: f"<li>{l[2:]}</li>", text.split("\n")))
        case BlockType.OL:
            output = ""
            index = 1
            for line in text.split("\n"):
                output = output + "<li>" + line.replace(f"{index}. ","") + "</li>\n"
                index += 1
            return output


def node_type_to_tag(type, content):
    match (type):
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            index = 0
            while len(content) > index and content[index] == "#":
                index += 1
            return f"h{index}"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UL:
            return "ul"
        case BlockType.OL:
            return "ol"

def extract_title(markdown):
    for line in markdown.split("\n"):
        if len(line) > 2 and line[:2] == "# ":
            return f"<h1>{line[2:].strip()}</h1>"
    raise Exception("No header line")

def get_child_node(type):
    match (type):
        case BlockType.PARAGRAPH:
            return ""
        case BlockType.HEADING:
            return ""
        case BlockType.CODE:
            return ""
        case BlockType.QUOTE:
            return "p"
        case BlockType.UL:
            return "li"
        case BlockType.OL:
            return "li"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content = ""
    with open(from_path) as file:
        content = file.read()
    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    output = ""
    with open(template_path) as file:
        output = file.read()
    output = output.replace("{{ Title }}",title)
    output = output.replace("{{ Content }}",html)
    dest_folder = "/".join(dest_path.split("/")[:-1])
    print(f"========================dest path: {dest_folder}")
    os.makedirs(dest_folder, exist_ok=True)
    with open(dest_path, mode="w") as dest:
        dest.write(output)
def generate_pages_recursive(from_path, template_path, dest_path):
    for node in os.listdir(from_path):
        node_path = os.path.join(from_path, node)
        node_dest_path = os.path.join(dest_path, node)
        if os.path.isfile(node_path):
            generate_page(node_path, template_path, node_dest_path.replace(".md",".html"))
        else:
            generate_pages_recursive(node_path, template_path, node_dest_path)
