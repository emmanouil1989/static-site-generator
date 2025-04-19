from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            result.append(node)
            continue
        if node.text_type == TextType.NORMAL_TEXT:
      
            splitted_list = node.text.split(delimiter) 
            if len(splitted_list) % 2 == 0:
                raise ValueError("Invalid markdown syntax")
            elif len(splitted_list) == 1:
                result.append(TextNode(node.text, TextType.NORMAL_TEXT))
                continue
            list_of_nodes = []
            for i in range(len(splitted_list)):
                if splitted_list[i].strip() == "":
                    continue
                if i % 2 == 0:
                    list_of_nodes.append(TextNode(splitted_list[i], TextType.NORMAL_TEXT))
                else:
                    list_of_nodes.append(TextNode(splitted_list[i], text_type))
            result.extend(list_of_nodes)
        else:
            result.append(node)
    return result

def extract_markdown_images(text):
    result = []
    image_regex = r"!\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(image_regex, text)

def extract_markdown_links(text):
    result = []
    link_regex = r"\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(link_regex, text)

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            result.append(node)
            continue
        else:
            extracted_images = extract_markdown_images(node.text)
            if len(extracted_images) == 0:
                result.append(node)
            else:
                for alt,url in extracted_images:
                    delimiter = f"![{alt}]({url})"
                    splitted_list = node.text.split(delimiter,1)

                    for i in range(len(splitted_list)):
                            
                        if splitted_list[i].strip() == "" and i == 0  and ("!" in splitted_list[i+1] or splitted_list[i+1].strip() == ""):
                            continue

                        elif i == 1 and splitted_list[i].strip() != "" and splitted_list[i-1].strip() != "" and "!" not in splitted_list[i]:
                            result.append(TextNode(alt, TextType.IMAGE_TEXT, url))
                            result.append(TextNode(splitted_list[i], TextType.NORMAL_TEXT))

                        
                        elif "!" not in splitted_list[i].strip() and splitted_list[i].strip() != "":
                            result.append(TextNode(splitted_list[i], TextType.NORMAL_TEXT))
                            node.text = node.text.replace(splitted_list[i], "")
                        
                        else:
                            result.append(TextNode(alt, TextType.IMAGE_TEXT, url))
                        node.text = node.text.replace(delimiter, "")
                        
    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            result.append(node)
            continue
        else:
            extracted_links = extract_markdown_links(node.text)
            if len(extracted_links) == 0:
                result.append(node)
            else:
                for alt,url in extracted_links:
                    delimiter = f"[{alt}]({url})"
                    splitted_list = node.text.split(delimiter,1)
                    for i in range(len(splitted_list)):
                      
                        if splitted_list[i].strip() == "" and i == 0  and ("[" in splitted_list[i+1] or splitted_list[i+1].strip() == ""):
                            continue
                        elif i == 1 and splitted_list[i].strip() !="" and splitted_list[i-1].strip() != "" and "[" not in splitted_list[i]:
                            result.append(TextNode(alt, TextType.LINK_TEXT, url))
                            result.append(TextNode(splitted_list[i], TextType.NORMAL_TEXT))
                        
                        elif "[" not in splitted_list[i].strip() and splitted_list[i].strip() != "":
                            result.append(TextNode(splitted_list[i], TextType.NORMAL_TEXT))
                            node.text = node.text.replace(splitted_list[i], "")
                        else:
                            result.append(TextNode(alt, TextType.LINK_TEXT, url))
                        node.text = node.text.replace(delimiter, "")
                        
    return result

def text_to_textnodes(text):
    result = []
    result.append(TextNode(text, TextType.NORMAL_TEXT))
    result = split_nodes_delimiter(result, "**", TextType.BOLD_TEXT)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC_TEXT)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC_TEXT)
    result = split_nodes_delimiter(result, "`", TextType.CODE_TEXT)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result

