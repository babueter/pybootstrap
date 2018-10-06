"""
HTML Component Collections
"""

from pybootstrap.core import Container, Component
from .utils import add_class_attributes


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


class Carousel(Container):
    def __init__(self, controls=False, indicators=False, interval=5000, keyboard=True, pause_on_hover=False, ride=False, wrap=True, **attributes):
        attributes["class"] = "carousel slide"
        super().__init__("div", **attributes)

        self.indicators = indicators
        self.interval = interval
        self.keyboard = keyboard
        self.ride = ride
        self.wrap = wrap

        self.add_attributes(**{"data-interval": str(interval)})
        self.add_attributes(**{"data-keyboard": str(keyboard).lower()})
        self.add_attributes(**{"data-ride": str(ride).lower()})
        self.add_attributes(**{"data-wrap": str(wrap).lower()})

        if pause_on_hover:
            self.add_attributes(**{"data-pause": "hover"})

        if indicators:
            self.indicators = Container("ol", **{"class": "carousel-indicators"})
            self.add_component(self.indicators)

        self.inner = Container("div", **{"class": "carousel-inner"})
        self.add_component(self.inner)

        if controls:
            control_prev = Container(
                "a", href="#carouselExampleIndicators", role="button",
                **{
                    "class": "carousel-control-prev",
                    "data-slide": "prev",
                },
            )
            control_prev.add_component(Component("span", inline=True, **{"class": "carousel-control-prev-icon", "aria-hidden": "true"}))
            control_prev.add_component(Component("span", inline=True, **{"class": "sr-only"}, text="Previous"))

            control_next = Container(
                "a", href="#carouselExampleIndicators", role="button",
                **{
                    "class": "carousel-control-next",
                    "data-slide": "next",
                },
            )
            control_next.add_component(Component("span", inline=True, **{"class": "carousel-control-next-icon", "aria-hidden": "true"}))
            control_next.add_component(Component("span", inline=True,**{"class": "sr-only"}, text="Next"))

            self.add_component(control_prev)
            self.add_component(control_next)

    def add_item(self, item: Component):
        item_index = str(len(self.inner.components))
        if self.indicators:
            # <li data-target="#carouselIndicators" data-slide-to="0" class="active"></li>
            indicator = Component(
                "li", inline=True,
                **{
                    "data-target": "#carouselIndicators",
                    "data-slide-to": item_index,
                },
            )
            if item_index == "0":
                add_class_attributes(indicator, "active")

            self.indicators.add_component(indicator)

        item_container = Container("div", **{"class": "carousel-item"})
        if item_index == "0":
            add_class_attributes(item_container, "active")

        item_container.add_component(item)
        self.inner.add_component(item_container)

    def __str__(self):
        self.get_attribute("data-interval").values = set((str(self.interval), ))
        self.get_attribute("data-keyboard").values = set((str(self.keyboard).lower(), ))
        self.get_attribute("data-ride").values = set((str(self.ride).lower(), ))
        self.get_attribute("data-wrap").values = set((str(self.wrap).lower(), ))

        return super().__str__()

