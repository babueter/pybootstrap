import unittest
from pybootstrap.utils import Header, Footer

TITLE="test title"
SCRIPT1="script1"
SCRIPT2="script2"

class TestHeader(unittest.TestCase):
    def setUp(self):
        self.header = Header(TITLE, SCRIPT1, SCRIPT2)

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
        self.footer = Footer(SCRIPT1, SCRIPT2)

    def test_init(self):
        self.assertTrue(hasattr(self.footer, "scripts"))
        self.assertTrue(SCRIPT1 in self.footer.scripts)
        self.assertTrue(SCRIPT2 in self.footer.scripts)

    def test_str(self):
        output = str(self.footer)

        self.assertTrue(SCRIPT1 in output)
        self.assertTrue(SCRIPT2 in output)
