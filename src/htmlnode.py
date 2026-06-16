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

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children:{self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node must have a value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

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
