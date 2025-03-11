class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props = list(map(lambda tup: f" {tup[0]}=\"{tup[1]}\"", self.props.items()))
        return "".join(props)
    
    def __repr__(self):
        return f"HTMLNode({tag}, {value}, {children}, {props})"