class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        # tag = f"<{self.tag}></{self.tag}>" if self.tag else None
        # value = self.value
        # n_children = len(self.children) if self.children else "No"
        # props = self.props
        # return f"HTMLNode(tag: {tag}, value: {value}, number_of_children: {n_children} HTMLNode(s), props: {props})"
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, props: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")

        html = ""
        if self.tag:
            html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            html = f"{self.value}"

        return html
