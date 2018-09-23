"""
HTML Component Collections
"""

from pybootstrap.core import Container


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
