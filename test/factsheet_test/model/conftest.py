"""
Test fixtures for :mod:`~.factsheet_test.content.section` unit tests.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.view import ui as UI


@pytest.fixture
def args_infoid_stock():
    """Pytest fixture returns set of argument values to construct a
    stock InfoId object.
    """
    return dict(
        p_aspect='section',
        p_name='Stock InfoId Name',
        p_title='Stock InfoId Title',
        p_summary='This summarizes a stock identification.',
        )


@pytest.fixture
def patch_class_view_infoid(args_infoid_stock):
    """Pytest fixture returns stub class implementing
    :class:`.InterfaceViewInfoId`.
     """
    class PatchViewInfoId(ABC_INFOID.InterfaceViewInfoId):
        ALL_TEXT = -1
        INCLUDE_HIDDEN = True

        def __init__(self):
            self._name = UI.FACTORY_INFOID.new_view_name()
            self._name.set_text(args_infoid_stock['p_name'])
            self._summary = UI.FACTORY_INFOID.new_view_summary()
            buffer_summary = self._summary.get_buffer()
            buffer_summary.set_text(
                args_infoid_stock['p_summary'], self.ALL_TEXT)
            self._title = UI.FACTORY_INFOID.new_view_title()
            self._title.set_text(args_infoid_stock['p_title'])

        def get_view_name(self): return self._name

        def get_view_summary(self): return self._summary

        def get_view_title(self): return self._title

        @property
        def name(self): return self._name.get_text()

        @property
        def summary(self):
            text = AINFOID.str_adapt_textview(self.get_view_summary())
            return text

        @property
        def title(self): return self._title.get_text()

    return PatchViewInfoId


@pytest.fixture
def patch_class_view_topics():
    """Pytest fixture returns stub class implementing
    :class:`.InterfacePaneTopic`.
    """
    class PatchViewTopics(ABC_OUTLINE.AbstractViewOutline):
        def __init__(self):
            self.called_get_selected = False
            self.called_select = False
            self.called_set_model = False
            self.called_unselect_all = False

        def get_selected(self): self.called_get_selected = True

        def select(self): self.called_select = True

        def unselect_all(self): self.called_unselect_all = True

    return PatchViewTopics


@pytest.fixture
def patch_class_page_sheet(patch_class_view_infoid):
    """Pytest fixture returns stub class implementing
    :class:`.InterfacePageSheet`.
    """
    class PatchPageSheet(ABC_SHEET.InterfacePageSheet):
        def __init__(self):
            self._infoid = patch_class_view_infoid()
            self._topics = UI.FACTORY_SHEET.new_view_outline_topics()
            self.called_close = False
            self.called_present = False
            self.called_set_titles = False
            self.subtitle = None

        def close_page(self): self.called_close = True

        def get_infoid(self): return self._infoid

        def get_view_topics(self): return self._topics

        def present(self, _time): self.called_present = True

        def set_titles(self, p_subtitle):
            self.called_set_titles = True
            self.subtitle = p_subtitle

    return PatchPageSheet
