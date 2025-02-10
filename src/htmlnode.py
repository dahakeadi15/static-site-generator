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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid ParentNode: no tag")
        if self.children is None:
            raise ValueError("invalid ParentNode: no children")
        children = []
        for child in self.children:
            children.append(child.to_html())
        return f'<{self.tag}{self.props_to_html()}>{"".join(children)}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
