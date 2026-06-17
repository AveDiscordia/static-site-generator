from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    filtered = filter(lambda block: block, blocks)
    return list(map(str.strip, filtered))

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if __is_block_quote(lines):
        return BlockType.QUOTE
    if __is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    if __is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def __is_block_quote(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith((">", "> ")):
            return False
    return True

def __is_unordered_list(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def __is_ordered_list(lines: list[str]) -> bool:
    ordinal = 1
    for line in lines:
        if not line.startswith(f"{ordinal}. "):
            return False
        ordinal += 1
    return True