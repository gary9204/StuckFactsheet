"""
test fixtures for Model classes.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.view import ui as UI


@pytest.fixture
def args_infoid_stock():
    return dict(
        p_aspect='section',
        p_name='Stock InfoId Name',
        p_title='Stock InfoId Title',
        # p_summary='This summarizes a stock identification.',
        )


@pytest.fixture
def patch_class_view_infoid(args_infoid_stock):
    class PatchViewInfoId(ABC_INFOID.InterfaceViewInfoId):
        def __init__(self):
            self._name = UI.FACTORY_INFOID.new_view_name()
            self._name.set_text(args_infoid_stock['p_name'])
            self._title = UI.FACTORY_INFOID.new_view_title()
            self._title.set_text(args_infoid_stock['p_title'])

        def get_view_name(self): return self._name

        def get_view_title(self): return self._title

        @property
        def name(self): return self._name.get_text()

        @property
        def title(self): return self._title.get_text()

    return PatchViewInfoId


@pytest.fixture
def patch_class_page_sheet(patch_class_view_infoid):
    class PatchPageSheet(ABC_SHEET.InterfacePageSheet):
        def __init__(self):
            self._infoid = patch_class_view_infoid()
            self.called_close = False
            self.called_present = False
            self.called_set_titles = False
            self.subtitle = None

        def close_page(self): self.called_close = True

        def get_infoid(self): return self._infoid

        def present(self, _time): self.called_present = True

        def set_titles(self, p_subtitle):
            self.called_set_titles = True
            self.subtitle = p_subtitle

    return PatchPageSheet
