from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Tag not set")
        if self.children is None:
            raise ValueError("Parent with no children")
        html = f"<{self.tag}>"
        for c in self.children:
            html = html + c.to_html()
        html = html + f"</{self.tag}>"
        return html
