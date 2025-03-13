from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes need a tag")
        if not self.children:
            raise ValueError("All parent nodes need children")
        parsed_children = "".join(list(map(lambda node: node.to_html(), self.children)))
        return f"<{self.tag}{self.props_to_html()}>{parsed_children}</{self.tag}>"