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

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        
        props_as_html = ""
        for attribute, value in self.props.items():
            props_as_html += f' {attribute}="{value}"'
        return props_as_html
    
    def __children_to_str(self, level) -> str:
        if self.children is None:
            return "None"
        
        tab = " " * 2 * level
        outer_tab = " " * 2 * (level - 1)
        child_lines: list[str] = []

        opening = "[\n"
        for child in self.children:
            child_lines.append(tab + child.__format_node_string(level + 1))
        closing = "\n" + outer_tab + "]"
        return opening + ", \n".join(child_lines) + closing
    
    def __props_to_str(self, level) -> str:
        if self.props is None:
            return "None"
        
        tab = " " * 2 * level 
        outer_tab = " " * 2 * (level - 1)
        lines: list[str] = []

        opening = "{\n"
        for prop, value in self.props.items():
            lines.append(tab + prop + ": " + value)
        closing = "\n" + outer_tab + "}"
        return opening + ", \n".join(lines) + closing
    
    def __format_node_string(self, level = 1) -> str:
        tab = " " * 2 * level 
        outer_tab = " " * 2 * (level - 1)
        lines: list[str] = []

        opening = "HTMLNode(\n"
        lines.append(tab + str(self.tag))
        lines.append(tab + str(self.value))
        lines.append(tab + self.__children_to_str(level + 1))
        lines.append(tab + self.__props_to_str(level + 1)) 
        closing = "\n" + outer_tab + ")"
        return opening + ", \n".join(lines) + closing

    def __repr__(self) -> str:
        return self.__format_node_string()