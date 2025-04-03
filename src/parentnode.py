from htmlnode import HTMLNode
from leafnode import LeafNode

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