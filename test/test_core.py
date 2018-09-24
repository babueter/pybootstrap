import unittest
from pybootstrap.core import Attribute, Component, Container

ATTRIBUTE_NAME="attr_name"
ATTRIBUTE_VALUE1="value1"
ATTRIBUTE_VALUE2="value2"
ATTRIBUTE_VALUE3="value3"
ATTRIBUTE_VALUE4="value4"

COMPONENT_TAG="div"
COMPONENT_TEXT="comp_text"
COMPONENT_INLINE=False
COMPONENT_INDENT=1
COMPONENT_ATTRIBUTE="attr"
COMPONENT_ATTRIBUTE_VALUE1="value1"
COMPONENT_ATTRIBUTE_VALUE2="value2"

CONTAINER_TAG="div"


class TestAttribute(unittest.TestCase):
    def setUp(self):
        self.a = Attribute(ATTRIBUTE_NAME, ATTRIBUTE_VALUE1, ATTRIBUTE_VALUE2)

    def test_init(self):
        self.assertTrue(hasattr(self.a, 'name'))
        self.assertTrue(hasattr(self.a, 'values'))
        self.assertTrue(ATTRIBUTE_VALUE1 in self.a.values)
        self.assertTrue(ATTRIBUTE_VALUE2 in self.a.values)

    def test_add_value(self):
        self.assertFalse(ATTRIBUTE_VALUE3 in self.a.values)
        self.a.add_value(ATTRIBUTE_VALUE3)
        self.assertTrue(ATTRIBUTE_VALUE3 in self.a.values)

    def test_del_value(self):
        self.a.add_value(ATTRIBUTE_VALUE4)
        self.assertTrue(ATTRIBUTE_VALUE4 in self.a.values)
        self.a.del_value(ATTRIBUTE_VALUE4)
        self.assertFalse(ATTRIBUTE_VALUE4 in self.a.values)

    def test_clear_values(self):
        self.assertTrue(self.a.values)
        self.a.clear_values()
        self.assertFalse(self.a.values)


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.c = Component(
            COMPONENT_TAG,
            text=COMPONENT_TEXT,
            inline=COMPONENT_INLINE,
            indent=COMPONENT_INDENT,
            **{COMPONENT_ATTRIBUTE: COMPONENT_ATTRIBUTE_VALUE1}
        )

    def test_init(self):
        self.assertTrue(hasattr(self.c, "tag"))
        self.assertTrue(self.c.tag == COMPONENT_TAG)

        self.assertTrue(hasattr(self.c, "text"))
        self.assertTrue(self.c.text == COMPONENT_TEXT)

        self.assertTrue(hasattr(self.c, "inline"))
        self.assertTrue(self.c.inline == COMPONENT_INLINE)

        self.assertTrue(hasattr(self.c, "indent"))
        self.assertTrue(self.c.indent == COMPONENT_INDENT)

        self.assertTrue(hasattr(self.c, "attributes"))
        self.assertTrue(COMPONENT_ATTRIBUTE in self.c.attributes)

    def test_add_attribute(self):
        a = Attribute(ATTRIBUTE_NAME, ATTRIBUTE_VALUE1)

        self.assertFalse(a in self.c.attributes)
        self.c.add_attribute(a)
        self.assertTrue(a in self.c.attributes)

        # Test adding existing attribute appends values
        a = Attribute(ATTRIBUTE_NAME, ATTRIBUTE_VALUE2)
        self.c.add_attribute(a)
        self.assertTrue(ATTRIBUTE_VALUE1 in self.c.get_attribute(a).values)
        self.assertTrue(ATTRIBUTE_VALUE2 in self.c.get_attribute(a).values)

    def test_del_attribute(self):
        a = Attribute(ATTRIBUTE_NAME, ATTRIBUTE_VALUE1)
        self.c.add_attribute(a)

        self.assertTrue(ATTRIBUTE_NAME in self.c.attributes)
        self.c.del_attribute(ATTRIBUTE_NAME)
        self.assertFalse(ATTRIBUTE_NAME in self.c.attributes)

    def test_add_attributes(self):
        self.c.del_attribute(ATTRIBUTE_NAME)

        self.assertFalse(ATTRIBUTE_NAME in self.c.attributes)
        self.c.add_attributes(**{ATTRIBUTE_NAME: ATTRIBUTE_VALUE1})
        self.assertTrue(ATTRIBUTE_NAME in self.c.attributes)

    def test_get_attribute(self):
        a = self.c.get_attribute(COMPONENT_ATTRIBUTE)
        self.assertTrue(a is not None)
        self.assertTrue(isinstance(a, Attribute))
        self.assertTrue(a.name == COMPONENT_ATTRIBUTE)

    def test_clear_attributes(self):
        self.assertTrue(self.c.attributes)
        self.c.clear_attributes()
        self.assertFalse(self.c.attributes)

    def test_str(self):
        html_open = self.c.html_open()
        html_body = self.c.html_body()
        html_close = self.c.html_close()

        self.assertTrue(html_open in str(self.c))
        self.assertTrue(html_body in str(self.c))
        self.assertTrue(html_close in str(self.c))


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.c = Container()

    def test_init(self):
        self.assertTrue(self.c is not None)
        self.assertTrue(isinstance(self.c, Container))
        self.assertTrue(self.c.tag == CONTAINER_TAG)
        self.assertTrue(self.c.inline == False)
        self.assertTrue(hasattr(self.c, "id"))
        self.assertTrue(self.c.id)

    def test_add_component(self):
        c = Component(COMPONENT_TAG)
        self.assertFalse(c.get_attribute("id"))
        self.assertFalse(c in self.c.components)

        # Test that ID is added to components
        self.c.add_component(c)
        self.assertTrue(c.get_attribute("id"))
        self.assertTrue(c in self.c.components)

        # Test that indent is updated on nested objects
        c1 = Container()
        c2 = Container()
        c1.add_component(c2)
        self.assertTrue(c1.indent == c2.indent-1)
        self.c.add_component(c1)
        self.assertTrue(self.c.indent == c1.indent-1)
        self.assertTrue(c1.indent == c2.indent-1)

    def test_del_component(self):
        c = Component(COMPONENT_TAG)
        self.c.add_component(c)
        self.assertTrue(c in self.c.components)

        id = c.get_attribute("id").get_values()
        self.c.del_component(id)
        self.assertFalse(c in self.c.components)

    def test_get_component(self):
        component = Component(COMPONENT_TAG)
        container = Container()
        container.add_component(component)

        self.c.add_component(container)
        self.assertTrue(component in container.components)
        self.assertTrue(container in self.c.components)

        id = component.get_attribute("id").get_values()
        get_c = self.c.get_component(id)
        self.assertTrue(component is get_c)
        self.assertTrue(self.c.get_component('OBJECT_NOT_FOUND') is None)

    def test_clear_components(self):
        c = Component(COMPONENT_TAG)
        self.c.add_component(c)

        self.assertTrue(self.c.components)
        self.c.clear_components()
        self.assertFalse(self.c.components)

    def test_html_body(self):
        c = Component(COMPONENT_TAG)
        self.c.add_component(c)
        self.assertTrue(c in self.c.components)

        id = c.get_attribute("id").get_values()
        self.assertTrue(id in self.c.html_body())
