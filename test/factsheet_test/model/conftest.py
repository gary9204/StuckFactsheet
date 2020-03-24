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
        # p_name='Stock InfoId Name',
        p_title='Stock InfoId Title',
        # p_summary='This summarizes a stock identification.',
        )


@pytest.fixture
def patch_class_view_infoid(args_infoid_stock):
    class PatchViewInfoId(ABC_INFOID.InterfaceViewInfoId):
        def __init__(self):
            self._title = UI.FACTORY_INFOID.new_view_title()
            self._title.set_text(args_infoid_stock['p_title'])

        def get_view_title(self): return self._title

        @property
        def title(self): return self._title.get_text()

    return PatchViewInfoId


@pytest.fixture
def patch_class_page_sheet(patch_class_view_infoid):
    class PatchPageSheet(ABC_SHEET.InterfacePageSheet):
        def __init__(self):
            self._infoid = patch_class_view_infoid()
            self.called_close = False
            self.called_update_name = False

        def close_page(self): self.called_close = True

        def get_infoid(self): return self._infoid

    #     def present(self): pass

        def update_name(self): self.called_update_name = True

    return PatchPageSheet
