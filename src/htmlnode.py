class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props

    def __repr__(self):
        tag = f"<{self.tag}></{self.tag}>" if self.tag else None
        value = self.value
        n_children = len(self.children) if self.children else "No"
        props = self.props
        return f"HTMLNode(tag: {tag}, value: {value}, number_of_children: {n_children} HTMLNode(s), props: {props})"
