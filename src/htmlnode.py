class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag, self.value = tag, value
        self.children, self.props = children, props

    def to_html(self):
        raise NotImplementedError("to_html method has not been implemented")

    def props_to_html(self):
        html = ""
        if self.props is None:
            return html
        for key, value in self.props.items():
            html +=  f' {key}="{value}"'
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        html = ""
        if not self.tag:
            raise ValueError("Parent node must have tag")
        if not self.children or self.children is None:
            raise ValueError("Parent node must have children")
        else:
            for child in self.children:
                html += child.to_html()
            return f'<{self.tag}>{html}</{self.tag}>'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have value")
        if self.tag is None:
            return self.value
        if self.props is not None:
            html_props = super().props_to_html()
            html_text = ""
            if self.value == "":
                html_text = f'<{self.tag}{html_props}{self.value} />'
            else:     
                html_text = f'<{self.tag}{html_props}>{self.value}</{self.tag}>' 
            return html_text
        return f"<{self.tag}>{self.value}</{self.tag}>"
