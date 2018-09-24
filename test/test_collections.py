import unittest
from pybootstrap.collections import ProgressBar, Table

TABLE_ROWS=3
TABLE_COLUMNS=2


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
