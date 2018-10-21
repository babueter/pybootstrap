"""
Core object classes
"""

import re
import uuid
import html


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

    def get_values(self) -> str:
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

    # http://w3c.github.io/html/syntax.html#void-elements
    VOID_ELEMENTS = (
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    )

    def __init__(self, tag, text: str = "", inline: bool = False, indent: int = 0, **attributes):
        self.tag = tag
        self.text = text
        self.inline = inline
        self.indent = indent

        self.attributes = set()
        self.add_attributes(**attributes)

    def add_attribute(self, attribute: Attribute):
        existing_attribute = self.get_attribute(attribute)
        if existing_attribute:
            existing_attribute.values.update(attribute.values)
        else:
            self.attributes.add(attribute)

    def add_attributes(self, **attributes):
        for attr in attributes.keys():
            attribute = Attribute(attr, attributes[attr])
            self.add_attribute(attribute)

    def del_attribute(self, attribute: Attribute):
        self.attributes.discard(attribute)

    def get_attribute(self, attr) -> Attribute:
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

    def html_open(self) -> str:
        attributes = " ".join(
            [str(attr) for attr in self.attributes if attr.get_values()]
        )
        return "{}<{} {}>".format(
            self._indent(),
            self.tag,
            attributes,
        )

    def html_body(self) -> str:
        body = ""
        if not self.inline:
            body = self._indent(1)

        body += html.escape(self.text).replace('%', '&#37;')
        return body

    def html_close(self) -> str:
        indent = "" if self.inline else self._indent()
        return "{}</{}>\n".format(indent, self.tag)

    def __str__(self) -> str:
        text = self.html_open()
        if self.tag not in self.VOID_ELEMENTS:
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
            exp = re.compile('^[a-z]')
            uuid_str = str(uuid.uuid4())
            while not exp.match(uuid_str):
                uuid_str = str(uuid.uuid4())

            self.add_attributes(id=uuid_str)

    def _update_indent_and_id(self, indent, component: Component):
        if not component.get_attribute("id"):
            component.add_attributes(id=str(uuid.uuid4()))

        component.indent = indent
        if isinstance(component, Container):
            for sub_component in component.components:
                self._update_indent_and_id(indent+1, sub_component)

    def add_component(self, component: Component):
        self._update_indent_and_id(self.indent+1, component)
        self.components.append(component)

    def del_component(self, id: str):
        for index in range(len(self.components)):
            comp_id = self.components[index].get_attribute("id")
            if comp_id and id == comp_id.get_values():
                self.components.pop(index)
                return

    def get_component(self, id) -> Component:
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

    def html_body(self) -> str:
        return "\n".join(
            [str(component) for component in self.components]
        )

    @property
    def id(self) -> str:
        id_attribute = self.get_attribute("id")
        if id_attribute:
            return id_attribute.get_values()

        return ""
