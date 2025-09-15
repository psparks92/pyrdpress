class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(map(lambda p: f"{p}=\"{self.props[p]}\"", self.props))

    def __repr__(self):
        return f"HTMLNode tag={self.tag}\n value={self.value}\n children={self.children}\nprops={self.props_to_html()}"

