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
