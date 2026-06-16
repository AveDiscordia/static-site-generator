class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        
        props_as_html = ""
        for attribute, value in self.props.items():
            props_as_html += f' {attribute}="{value}"'
        return props_as_html
    
    def _children_to_str(self, level: int = 2) -> str:
        if self.children is None:
            return "None"
        
        tab = " " * 2 * level
        outer_tab = " " * 2 * (level - 1)
        child_lines: list[str] = []

        opening = "[\n"
        for child in self.children:
            child_lines.append(tab + child._format_node_string(level + 1))
        closing = "\n" + outer_tab + "]"
        return opening + ",\n".join(child_lines) + closing
    
    def _props_to_str(self, level: int = 2) -> str:
        if self.props is None:
            return "None"
        
        tab = " " * 2 * level 
        outer_tab = " " * 2 * (level - 1)
        lines: list[str] = []

        opening = "{\n"
        for prop, value in self.props.items():
            lines.append(tab + prop + ": " + value)
        closing = "\n" + outer_tab + "}"
        return opening + ",\n".join(lines) + closing
    
    def _format_node_string(self, level: int = 1) -> str:
        if self.children is None:
            return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

        tab = " " * 2 * level 
        outer_tab = " " * 2 * (level - 1)
        lines: list[str] = []

        opening = "HTMLNode(\n"
        lines.append(tab + str(self.tag))
        lines.append(tab + str(self.value))
        lines.append(tab + self._children_to_str(level + 1))
        lines.append(tab + self._props_to_str(level + 1)) 
        closing = "\n" + outer_tab + ")"
        return opening + ",\n".join(lines) + closing

    def __repr__(self) -> str:
        return self._format_node_string()
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node must have a value")
        if self.tag is None:
            return self.value
        opening = f"<{self.tag}{self.props_to_html()}>"
        closing = f"</{self.tag}>"
        return opening + self.value + closing
    
    def _format_node_string(self, level: int = 1) -> str:
        return str(self)

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent node must have a tag")
        if self.children is None:
            raise ValueError("parent node must have a child")
        
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        return html_string + f"</{self.tag}>"
