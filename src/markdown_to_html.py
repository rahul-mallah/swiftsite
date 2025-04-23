from block_markdown import *
from inline_markdown import *
from htmlnode import *
from textnode import *


def convert_inline_html(text):
    # get text nodes for the text block
    text_nodes = text_to_textnodes(text)
    # convert each text node to html node
    html_nodes = list(map(lambda node: text_node_to_html_node(node), text_nodes))
    return html_nodes


def handle_list(block, tag):
    new_nodes = []
    # split the list block by line
    lines = block.split("\n")

    # check ordered or unordered list
    if tag == "ul":
        lines = list(map(lambda line: line[2:], lines))
    elif tag == "ol":
        # slice off numbered bullet points and . and space
        lines = list(map(lambda line: line[len(line.split(".")[0])+2:], lines))

    # convert each line to textnodes and then html nodes
    # list will contain list of html nodes for each line
    inline_nodes_arr = list(map(lambda line: convert_inline_html(line), lines))
    
    # enclose each list in parent node of li
    for nodes_arr in inline_nodes_arr:
        new_nodes.append(ParentNode("li", nodes_arr))  
    # enclose the li's to final ol or ul tag
    return ParentNode(tag, new_nodes)


def handle_header(block):
    # split by # and space. Count check will be 1 lesser
    count = block.split("# ")[0].count("#")
    tag = ""
    if count == 0:
        tag = "h1"
    elif count == 1:
        tag = "h2"
    elif count == 2:
        tag = "h3"
    elif count == 3:
        tag = "h4"
    elif count == 4:
        tag = "h5"
    elif count == 5:
        tag = "h6"
    html_nodes = convert_inline_html(block.split("# ")[1])
    return ParentNode(tag, html_nodes)


def handle_paragraph(block):
    text = block.replace("\n", " ")
    html_nodes = convert_inline_html(text)
    return ParentNode("p", html_nodes)


def handle_code(block):
    text_node = TextNode(block.split("```")[1].lstrip(), TextType.CODE_TEXT)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node])


def handle_blockquote(block):
    lines = block.split(">")
    lines = list(filter(lambda line: line, list(map(lambda line: line.strip(), lines))))
    text = " ".join(lines)
    html_nodes = convert_inline_html(text)
    return ParentNode("blockquote", html_nodes)
    

def markdown_to_html_node(markdown):
    result = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.UNORDERED_LIST:
                result.append(handle_list(block, "ul"))
            case BlockType.ORDERED_LIST:
                result.append(handle_list(block, "ol"))
            case BlockType.HEADING:
                result.append(handle_header(block))
            case BlockType.QUOTE:
                result.append(handle_blockquote(block))
            case BlockType.CODE:
                result.append(handle_code(block))
            case BlockType.PARAGRAPH:
                result.append(handle_paragraph(block))
            case _:
                return ValueError("Invalid Block Type")
    return ParentNode("div", result)
