import unittest
from pybootstrap.collections import *

TABLE_ROWS=3
TABLE_COLUMNS=2

CAROUSEL_INTERVAL=9999

class TestProgressBar(unittest.TestCase):
    def setUp(self):
        self.progressbar = ProgressBar()

    def test_init(self):
        self.assertTrue(hasattr(self.progressbar, "valuenow"))
        self.assertTrue(hasattr(self.progressbar, "valuemin"))
        self.assertTrue(hasattr(self.progressbar, "valuemax"))
        self.assertTrue(self.progressbar.get_component("{}-progressbar".format(self.progressbar.id)))

    def test_html_body(self):
        output = str(self.progressbar)
        self.assertTrue('aria-valuenow="{}"'.format(self.progressbar.valuenow) in output)
        self.assertTrue('aria-valuemin="{}"'.format(self.progressbar.valuemin) in output)
        self.assertTrue('aria-valuemax="{}"'.format(self.progressbar.valuemax) in output)
        self.assertTrue('style="width: {}%"'.format(self.progressbar.valuenow) in output)

        self.progressbar.valuenow = 1
        self.progressbar.valuemin = 2
        self.progressbar.valuemax = 3

        output = str(self.progressbar)
        self.assertTrue('aria-valuenow="{}"'.format(self.progressbar.valuenow) in output)
        self.assertTrue('aria-valuemin="{}"'.format(self.progressbar.valuemin) in output)
        self.assertTrue('aria-valuemax="{}"'.format(self.progressbar.valuemax) in output)
        self.assertTrue('style="width: {}%"'.format(self.progressbar.valuenow) in output)


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table(rows=TABLE_ROWS, cols=TABLE_COLUMNS)

    def test_init(self):
        self.assertTrue(self.table.rows() == TABLE_ROWS)
        self.assertTrue(self.table.cols() == TABLE_COLUMNS)
        self.assertTrue(self.table.tag == self.table.TABLE_TAG)

    def test_add_cols(self):
        col_count = self.table.cols()
        for row in self.table.components:
            self.assertTrue(len(row.components) == col_count)

        self.table.add_cols(1)
        for row in self.table.components:
            self.assertTrue(len(row.components) == col_count+1)

    def test_get_col(self):
        c = self.table.get_col(2, 1)
        self.assertTrue(c is not None)
        self.assertTrue(c.id == "{}_row_2_col_1".format(self.table.id))

    def test_add_rows(self):
        row_count = self.table.rows()
        self.table.add_rows(1)
        self.assertFalse(self.table.rows() == row_count)

        for row in self.table.components:
            self.assertTrue(len(row.components) == self.table.cols())


class TestCarousel(unittest.TestCase):
    def setUp(self):
        self.carousel = Carousel(controls=True, indicators=True)

    def test_init(self):
        self.assertTrue(self.carousel.components[0].tag == "ol")
        self.assertTrue(self.carousel.components[1] == self.carousel.inner)
        self.assertTrue("carousel-control-prev" in self.carousel.components[2].get_attribute("class").get_values())
        self.assertTrue("carousel-control-next" in self.carousel.components[3].get_attribute("class").get_values())

    def test_interval(self):
        self.assertTrue("data-interval=\"{}\"".format(CAROUSEL_INTERVAL) not in str(self.carousel))
        self.carousel.interval = CAROUSEL_INTERVAL
        self.assertTrue("data-interval=\"{}\"".format(CAROUSEL_INTERVAL) in str(self.carousel))

    def test_keyboard(self):
        self.assertTrue("data-keyboard=\"false\"" not in str(self.carousel))
        self.carousel.keyboard = False
        self.assertTrue("data-keyboard=\"false\"" in str(self.carousel))

    def test_ride(self):
        self.assertTrue("data-ride=\"true\"" not in str(self.carousel))
        self.carousel.ride = True
        self.assertTrue("data-ride=\"true\"" in str(self.carousel))

    def test_wrap(self):
        self.assertTrue("data-wrap=\"false\"" not in str(self.carousel))
        self.carousel.wrap = False
        self.assertTrue("data-wrap=\"false\"" in str(self.carousel))

    def test_add_item(self):
        self.assertFalse(self.carousel.indicators.components)
        self.assertFalse(self.carousel.inner.components)

        item = Component("img", src="...", alt="Slide")
        self.carousel.add_item(item)

        self.assertTrue(self.carousel.indicators.components)
        self.assertTrue(self.carousel.inner.components)
