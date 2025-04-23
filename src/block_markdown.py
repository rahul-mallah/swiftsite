from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list" 


def markdown_to_blocks(markdown):
    # split markdown by double line
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks
    

def block_to_block_type(md_text):
    block_type = BlockType.PARAGRAPH
    # Header 
    split_text = md_text.split("# ")
    if len(split_text) > 1 and len(split_text[0]) < 6:
        block_type = BlockType.HEADING

    # Code 
    split_text = md_text.split("```")
    if len(split_text) == 3:
        block_type = BlockType.CODE
    
    # Quote
    split_text = md_text.split("\n")
    filtered_text = list(filter(lambda line: line[0] == ">", split_text))
    if len(split_text) == len(filtered_text):
        block_type = BlockType.QUOTE
    
    # Unordered list
    filtered_text = list(filter(lambda line: line[0:2] == "- ", split_text))
    if len(split_text) == len(filtered_text):
        block_type = BlockType.UNORDERED_LIST

    # Ordered list
    isOrdList = True
    for i in range(0, len(split_text)):
        num = len(split_text[i].split(".")[0])
        if split_text[i][0:num+2] != f"{str(i+1)}. ":
            isOrdList = False
    
    if isOrdList:
        block_type = BlockType.ORDERED_LIST
    
    return block_type


