from textnode import TextNode, TextType
from blockutils import block_to_block_type,BlockType
from nodes_utils import text_to_textnodes
from parentnode import ParentNode

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    final_children_nodes_list = []
    for block_text in blocks:
        block_type = block_to_block_type(block_text)
        match block_type:
            case BlockType.PARAGRAPH:
                block_text = block_text.replace("\n", " ")
                children = text_to_children(block_text)
                paragraph_parent = ParentNode("p", children)
                final_children_nodes_list.append(paragraph_parent)
            case BlockType.HEADING:
                heading_level = get_heading_level(block_text)
                filtered_block_text = block_text.replace("#", "").strip()
                filtered_block_text = filtered_block_text.replace("\n", " ")
                children = text_to_children(filtered_block_text)
                final_children_nodes_list.append(ParentNode(f"h{heading_level}", children))
            case BlockType.CODE:
                block_text = block_text.replace("```", "")
                block_text = block_text[1:]
                children = handle_block_type(block_text)
                final_children_nodes_list.append(ParentNode("pre", [children]))
            case BlockType.QUOTE:
                block_text = block_text.replace(">", "").strip()
                block_text = block_text.replace('\n', '')
                children = text_to_children(block_text)
                final_children_nodes_list.append(ParentNode("blockquote", children))
            case BlockType.UNORDERED_LIST:
                unordered_list = block_text.split("\n")
                list_items = handle_list_items_for_unordered_list(unordered_list)
                final_children_nodes_list.append(ParentNode("ul", list_items))
            case BlockType.ORDERED_LIST:
                text_to_children(block_text)
                ordered_list = block_text.split("\n")
                list_items = handle_list_items_for_ordered_list(ordered_list)
                final_children_nodes_list.append(ParentNode("ol", list_items))
            case _:
                print('unknown block type')
    return ParentNode("div", final_children_nodes_list)
        

def handle_list_items_for_ordered_list(list):
    final_list = []
    for i in range(len(list)):
        list[i] = list[i].replace(f"{i + 1}. ", "").strip()
        list[i] = list[i].replace("\n", " ")
        children = text_to_children(list[i])
        final_list.append(ParentNode("li", children))
    return final_list

def handle_list_items_for_unordered_list(list):
    final_list = []
    for i in range(len(list)):
        list[i] = list[i].replace("- ", "").strip()
        list[i] = list[i].replace("\n", " ")
        children = text_to_children(list[i])
        final_list.append(ParentNode("li", children))
    return final_list

def get_heading_level(block_text):
    heading_level = 0
    for char in block_text:
        if char == "#":
            heading_level += 1
        else:
            break
    return heading_level

def handle_block_type(block_text):
    text_node = TextNode(block_text, TextType.CODE_TEXT)
    return text_node.text_node_to_html_node()
    

def text_to_children(text):
    return list(map(lambda x: x.text_node_to_html_node(),text_to_textnodes(text)))

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("#"):
            return line.replace("#", "").strip()
            break
    if title == "":
        raise ValueError("No title found in the markdown")
    return title
        



