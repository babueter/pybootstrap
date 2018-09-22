"""
Core object classes
"""

import uuid

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

    def __eq__(self, other):
        return hash(self) == hash(other)

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
        self.add_attributes(**attributes)

    def add_attribute(self, attribute: Attribute):
        self.attributes.add(attribute)

    def add_attributes(self, **attributes):
        for attr in attributes.keys():
            attribute = Attribute(attr, attributes[attr])
            self.add_attribute(attribute)

    def del_attribute(self, attribute: Attribute):
        self.attributes.discard(attribute)

    def get_attribute(self, attr):
        for attribute in self.attributes:
            if attribute == attr:
                return attribute

        return None

    def clear_attributes(self):
        self.attributes = set()

    def _indent(self, indent: int = 0):
        return " "*(
            (self.indent + indent) * self.INDENT_SPACING
        )

    def html_open(self):
        attributes = " ".join(
            [str(attr) for attr in self.attributes]
        )
        return "{}<{} {}>".format(
            self._indent(),
            self.tag,
            attributes,
        )

    def html_body(self):
        body = ""
        if not self.inline:
            body = self._indent(1)

        body += self.text
        return body

    def html_close(self):
        indent = "" if self.inline else self._indent()
        return "{}</{}>\n".format(indent, self.tag)

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

        if not self.get_attribute("id"):
            self.add_attributes(id=str(uuid.uuid4()))

    def add_component(self, component: Component):
        component.indent = self.indent + 1
        if not component.get_attribute("id"):
            component.add_attributes(id=str(uuid.uuid4()))

        self.components.append(component)

    def del_component(self, index: int):
        self.components.pop(index)

    def get_component(self, id):
        for component in self.components:
            if component.get_attribute("id").values == set((id,)):
                return component

            if isinstance(component, Container):
                sub_component = component.get_component(id)
                if sub_component:
                    return sub_component

        return None

    def clear_components(self):
        self.components.clear()

    def html_body(self):
        return "\n".join(
            [str(component) for component in self.components]
        )
