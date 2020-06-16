"""
Test fixtures for :mod:`~.factsheet_test.model` unit tests.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.view import ui as UI


@pytest.fixture
def args_infoid_stock():
    """Pytest fixture returns set of argument values to construct a
    stock InfoId object.
    """
    return dict(
        p_name='Stock InfoId Name',
        p_title='Stock InfoId Title',
        p_summary='This summarizes a stock identification.',
        )


@pytest.fixture
def interface_view_infoid(args_infoid_stock):
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
def interface_pane_topic(interface_view_infoid):
    """Pytest fixture returns stub class implementing
    :class:`.InterfacePaneTopic`.
    """
    class PatchPaneTopic(ABC_TOPIC.InterfacePaneTopic):
        def __init__(self):
            self._infoid = interface_view_infoid()

        def get_infoid(self): return self._infoid

    return PatchPaneTopic
