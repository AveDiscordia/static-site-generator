import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if (delimiter != "**" and delimiter != "_") and delimiter != "`":
        raise ValueError(f"delimiter '{delimiter}' not recognized")
    if (
        ((delimiter == "**" and text_type != TextType.BOLD)
        or (delimiter == "_" and text_type != TextType.ITALIC))
        or (delimiter == "`" and text_type != TextType.CODE)
    ):
        raise ValueError(f"delimiter '{delimiter}' does not match text type {text_type}")

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text: list[str] = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"closing delimiter not found in text: '{node.text}'")
        new_nodes.extend(__transform_split_text(delimiter, text_type, split_text))
    return new_nodes

def __transform_split_text(delimiter, text_type, split_text):
    new_nodes: list[TextNode] = []
    for i in range(len(split_text)):
        text = split_text[i]
        if i % 2 == 0:
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            if text == "" or text.strip() != text:
                new_nodes.append(TextNode(delimiter + text + delimiter, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)