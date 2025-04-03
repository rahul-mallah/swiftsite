from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have value")
        if self.tag is None:
            return self.value
        if self.props is not None:
            html_props = super().props_to_html()
            return f'<{self.tag}{html_props}>{self.value}</{self.tag}>'   
        return f"<{self.tag}>{self.value}</{self.tag}>"
    

    