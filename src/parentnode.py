from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        converted_children = "".join(map(lambda child: child.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{converted_children}</{self.tag}>"