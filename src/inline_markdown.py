import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        result = []

        while len(text) > 0:
            # find first position of delimiter
            start_index = text.find(delimiter)
            
            if start_index != -1:
                normal_text = text[:start_index]
                if normal_text != "":
                    result.append(TextNode(normal_text, TextType.NORMAL_TEXT))
        
                end_index = text.find(delimiter, start_index + len(delimiter))

                if end_index != -1:
                    delimiter_text = text[start_index + len(delimiter):end_index]
                    result.append(TextNode(delimiter_text, text_type))
                else:
                    raise ValueError("Markdown Syntax Error: Closing delimiter not found")
                text = text[end_index+len(delimiter):]
            else:
                result.append(TextNode(text, TextType.NORMAL_TEXT))
                text = ""
        new_nodes.extend(result)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_common_func(text, extracted_list, text_type):
    result = []
    temp_text = text
    md_text = ""
    for alt_text, url in extracted_list:
        if text_type == TextType.IMAGE:
            md_text = f"![{alt_text}]({url})"
        else:
            md_text = f"[{alt_text}]({url})"
        split_text = temp_text.split(md_text, 1)
        if split_text[0].strip():
            result.append(TextNode(split_text[0], TextType.NORMAL_TEXT))
        result.append(TextNode(alt_text, text_type, url))
        end_index = len(split_text[0]) + len(md_text)
        temp_text = temp_text[end_index:]

    if temp_text.strip():
        result.append(TextNode(temp_text, TextType.NORMAL_TEXT))

    return result


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.NORMAL_TEXT:
            images = extract_markdown_images(old_node.text)
            if len(images) == 0:
                new_nodes.append(old_node)
            else:
                new_nodes.extend(split_nodes_common_func(old_node.text, images, TextType.IMAGE))
        else:
            new_nodes.append(old_node)
    #print(new_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.NORMAL_TEXT:
            links = extract_markdown_links(old_node.text)
            if len(links) == 0:
                new_nodes.append(old_node)
            else:
                new_nodes.extend(split_nodes_common_func(old_node.text, links, TextType.LINK))
        else:
            new_nodes.append(old_node)
    #print(new_nodes)
    return new_nodes


def text_to_textnodes(text):
    result = []
    delimiters = [("`",TextType.CODE_TEXT),("**",TextType.BOLD_TEXT),("_",TextType.ITALIC_TEXT)]

    node = TextNode(text, TextType.NORMAL_TEXT)
    result = [node]
    for delim, text_type in delimiters:
        result = split_nodes_delimiter(result, delim, text_type)
    
    result = split_nodes_link(split_nodes_image(result))
    return result