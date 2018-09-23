"""
HTML Component Collections
"""

from pybootstrap.core import Attribute, Container

CONTAINER = Attribute("class", "container")
ROW = Attribute("class", "row")
COL_1 = Attribute("class", "col-1")
COL_2 = Attribute("class", "col-2")
COL_3 = Attribute("class", "col-3")
COL_4 = Attribute("class", "col-4")
COL_5 = Attribute("class", "col-5")
COL_6 = Attribute("class", "col-6")
COL_7 = Attribute("class", "col-7")
COL_8 = Attribute("class", "col-8")
COL_9 = Attribute("class", "col-9")
COL_10 = Attribute("class", "col-10")
COL_11 = Attribute("class", "col-11")
COL_12 = Attribute("class", "col-12")

COL_SM_1 = Attribute("class", "col-sm-1")
COL_SM_2 = Attribute("class", "col-sm-2")
COL_SM_3 = Attribute("class", "col-sm-3")
COL_SM_4 = Attribute("class", "col-sm-4")
COL_SM_5 = Attribute("class", "col-sm-5")
COL_SM_6 = Attribute("class", "col-sm-6")
COL_SM_7 = Attribute("class", "col-sm-7")
COL_SM_8 = Attribute("class", "col-sm-8")
COL_SM_9 = Attribute("class", "col-sm-9")
COL_SM_10 = Attribute("class", "col-sm-10")
COL_SM_11 = Attribute("class", "col-sm-11")
COL_SM_12 = Attribute("class", "col-sm-12")

COL_LG_1 = Attribute("class", "col-lg-1")
COL_LG_2 = Attribute("class", "col-lg-2")
COL_LG_3 = Attribute("class", "col-lg-3")
COL_LG_4 = Attribute("class", "col-lg-4")
COL_LG_5 = Attribute("class", "col-lg-5")
COL_LG_6 = Attribute("class", "col-lg-6")
COL_LG_7 = Attribute("class", "col-lg-7")
COL_LG_8 = Attribute("class", "col-lg-8")
COL_LG_9 = Attribute("class", "col-lg-9")
COL_LG_10 = Attribute("class", "col-lg-10")
COL_LG_11 = Attribute("class", "col-lg-11")
COL_LG_12 = Attribute("class", "col-lg-12")


class Table(Container):
    TABLE_TAG="table"
    ROW_TAG="tr"
    COL_TAG="td"

    def __init__(self, *args, rows: int = 0, cols: int = 0, **kwargs):
        if not args:
            args = (self.TABLE_TAG, )

        super().__init__(*args, **kwargs)
        self.add_rows(rows)
        self.add_cols(cols)

    def rows(self) -> int:
        return len(self.components)

    def add_rows(self, rows: int):
        row_index = self.rows() + 1
        for row in range(rows):
            index = row_index + row
            row_component = Container(self.ROW_TAG, id="{}_row_{}".format(self.id, index))
            self.add_component(row_component)

            for col in range(self.cols()):
                col_component = Container(self.COL_TAG, id="{}_row_{}_col_{}".format(self.id, index, col+1))
                row_component.add_component(col_component)

    def get_row(self, row: int) -> Container:
        return self.get_component("{}_row_{}".format(self.id, row))

    def cols(self) -> int:
        if self.rows():
            row = self.get_row(1)
            if row:
                return len(row.components)

        return 0

    def add_cols(self, cols: int):
        col_index = self.cols() + 1
        for col in range(cols):
            index = col_index + col
            for row in range(self.rows()):
                row_component = self.get_row(row+1)
                if row_component:
                    col_component = Container(self.COL_TAG, id="{}_row_{}_col_{}".format(self.id, row+1, index))
                    row_component.add_component(col_component)

    def get_col(self, row, col):
        return self.get_component("{}_row_{}_col_{}".format(self.id, row, col))
