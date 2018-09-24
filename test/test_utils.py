import unittest
from pybootstrap.core import Component
from pybootstrap import utils

TITLE="test title"
SCRIPT1="script1"
SCRIPT2="script2"

CLASS1="test1"
CLASS2="test1"


class TestUtilsMethods(unittest.TestCase):
    def test_add_class_attributes(self):
        c = Component("div")
        self.assertTrue(c.get_attribute("class") is None)

        utils.add_class_attributes(c, CLASS1, CLASS2)
        self.assertTrue(c.get_attribute("class") is not None)
        self.assertTrue(CLASS1 in c.get_attribute("class").values)
        self.assertTrue(CLASS2 in c.get_attribute("class").values)


class TestHeader(unittest.TestCase):
    def setUp(self):
        self.header = utils.Header(TITLE, SCRIPT1, SCRIPT2)

    def test_init(self):
        self.assertTrue(hasattr(self.header, "title"))
        self.assertTrue(hasattr(self.header, "scripts"))

        self.assertTrue(TITLE == self.header.title)
        self.assertTrue(SCRIPT1 in self.header.scripts)
        self.assertTrue(SCRIPT2 in self.header.scripts)

    def test_str(self):
        output = str(self.header)
        self.assertTrue(self.header.BOOTSTRAP_URL in output)
        self.assertTrue(self.header.BOOTSTRAP_INTEGRITY in output)
        self.assertTrue(self.header.META_CHARSET in output)
        self.assertTrue(self.header.META_VIEWPORT_CONTENT in output)
        self.assertTrue(self.header.LANG in output)

        self.assertTrue(SCRIPT1 in output)
        self.assertTrue(SCRIPT2 in output)


class TestFooter(unittest.TestCase):
    def setUp(self):
        self.footer = utils.Footer(SCRIPT1, SCRIPT2)

    def test_init(self):
        self.assertTrue(hasattr(self.footer, "scripts"))
        self.assertTrue(SCRIPT1 in self.footer.scripts)
        self.assertTrue(SCRIPT2 in self.footer.scripts)

    def test_str(self):
        output = str(self.footer)

        self.assertTrue(SCRIPT1 in output)
        self.assertTrue(SCRIPT2 in output)
