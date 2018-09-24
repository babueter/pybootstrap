"""
HTML Component Collections
"""

from pybootstrap.core import Container


class ProgressBar(Container):
    def __init__(self, text: str = None, valuenow: int = 0, valuemin: int = 0, valuemax: int = 100, **attributes):
        attributes["class"] = "progress"
        super().__init__("div", **attributes)

        self.valuenow = valuenow
        self.valuemin = valuemin
        self.valuemax = valuemax

        progressbar = Container(
            "div",
            role="progressbar",
            style="width: {}%".format(valuenow),
            id="{}-progressbar".format(self.id),
            **{"class": "progress-bar"}
        )
        self.add_component(progressbar)

    def html_body(self):
        progressbar = self.get_component("{}-progressbar".format(self.id))
        progressbar.del_attribute("aria-valuenow")
        progressbar.del_attribute("aria-valuemin")
        progressbar.del_attribute("aria-valuemax")
        progressbar.del_attribute("style")

        progressbar.add_attributes(**{
            "aria-valuenow": str(self.valuenow),
            "aria-valuemin": str(self.valuemin),
            "aria-valuemax": str(self.valuemax),
            "style": "width: {}%".format(self.valuenow),
        })
        return super().html_body()


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
