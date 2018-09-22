"""
Core object classes
"""


class Attribute(object):
    """
    HTML Attribute
    """
    def __init__(self, name, *values):
        self.name = name

        self.values = set()
        for value in values:
            self.add_value(value)

    def add_value(self, value):
        self.values.add(value)

    def del_value(self, value):
        self.values.discard(value)

    def get_values(self):
        return " ".join(self.values)

    def clear_values(self):
        self.values = set()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{}=\"{}\"".format(
            self.name,
            self.get_values(),
        )


class Component(object):
    """
    HTML Component
    """
    INDENT_SPACING = 4
    attributes = set()

    def __init__(self, tag, text: str = "", inline: bool = False, indent: int = 0, **attributes):
        self.tag = tag
        self.text = text
        self.inline = inline
        self.indent = indent

        self.attributes = set()
        for attr in attributes.keys():
            attribute = Attribute(attr, attributes[attr])
            self.add_attribute(attribute)

    def add_attribute(self, attribute: Attribute):
        self.attributes.add(attribute)

    def del_attribute(self, attribute: Attribute):
        self.attributes.discard(attribute)

    def get_attributes(self):
        return " ".join(
            [str(attr) for attr in self.attributes]
        )

    def clear_attributes(self):
        self.attributes = set()

    def _indent(self, indent: int = 0):
        return " "*(
            (self.indent + indent) * self.INDENT_SPACING
        )

    def html_open(self):
        return "{}<{} {}>".format(
            self._indent(),
            self.tag,
            self.get_attributes(),
        )

    def html_body(self):
        body = ""
        if not self.inline:
            body = self._indent(1)

        body += self.text
        return body

    def html_close(self):
        indent = "" if self.inline else self._indent()
        return "{}</{}>".format(indent, self.tag)

    def __str__(self):
        text = self.html_open()
        text += "" if self.inline else "\n"
        text += self.html_body()
        text += "" if self.inline else "\n"
        text += self.html_close()

        return text


class Container(Component):
    """
    HTML Container
    """
    def __init__(self, *args, **kwargs):
        if not args:
            args = ['div']

        kwargs['inline'] = False

        super().__init__(*args, **kwargs)
        self.components = list()

    def add_component(self, component: Component):
        component.indent = self.indent + 1
        self.components.append(component)

    def del_component(self, index: int):
        self.components.pop(index)

    def clear_components(self):
        self.components.clear()

    def html_body(self):
        return "\n".join(
            [str(component) for component in self.components]
        )
