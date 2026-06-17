from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown: str) -> ParentNode:
    html_blocks: list[HTMLNode] = []
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_tag: str = html_tag_from_block(block, block_type)
        if block_type == BlockType.CODE:
            stripped_block = block.removeprefix("```\n").removesuffix("```")
            code_textnode = TextNode(stripped_block, TextType.TEXT)
            code_htmlnode = text_node_to_html_node(code_textnode)
            tagged_block = ParentNode(html_tag, [code_htmlnode])
            html_blocks.append(ParentNode("pre", [tagged_block]))
            continue

        lines: list[str] = block.split("\n")
        lines = strip_block_identifiers(lines, block_type)
        if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            list_item_htmlnodes: list[HTMLNode] = []
            for line in lines:
                list_item_child_nodes: list[HTMLNode] = text_to_children(line)
                list_item_htmlnodes.append(ParentNode("li", list_item_child_nodes))
            html_blocks.append(ParentNode(html_tag, list_item_htmlnodes))
            continue
        
        text = " ".join(lines)
        child_nodes = text_to_children(text)
        html_blocks.append(ParentNode(html_tag, child_nodes))

    return ParentNode("div", html_blocks)

def html_tag_from_block(block: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            level = len(block.split(maxsplit=1)[0])
            if level < 1 or level > 6:
                raise ValueError(f"block is not a valid heading level: {block}")
            return f"h{level}"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        
def strip_block_identifiers(lines: list[str], block_type: BlockType) -> list[str]:
    if block_type == BlockType.CODE:
        raise ValueError("code blocks are handled earlier")
    
    if block_type == BlockType.PARAGRAPH:
        return lines
    elif block_type == BlockType.HEADING:
        return [lines[0].split(maxsplit=1)[1]] + lines[1:]
    elif block_type == BlockType.QUOTE:
        return list(
            map(
                lambda line: line.removeprefix("> ").removeprefix(">"),
                lines
            )
        )
    else:
        return list(
            map(
                lambda line: line.split(maxsplit=1)[1],
                lines
            )
        )

def text_to_children(text: str) -> list[HTMLNode]:
    child_nodes: list[HTMLNode] = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes