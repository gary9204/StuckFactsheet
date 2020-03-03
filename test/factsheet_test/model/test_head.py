"""
Unit tests for model component identification information class.

See :mod:`.head`.
"""


import copy
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_head as AHEAD
from factsheet.model import head as MHEAD
from factsheet.view import page_head as VHEAD
from factsheet.view import ui as VUI


@pytest.fixture
def stock_args():
    return dict(
        name='Stock Head Name',
        title='Stock Head Title',
        summary='This summarizes a stock identification.',
        aspect='section',
        )


class TestHead:
    """Unit tests for :class:`.Head`."""

    def test_eq(self, stock_args):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: title difference.
        #. Case: aspect difference.
        #. Case: equivalent
        """
        # Setup
        source = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test: type difference.
        assert not source.__eq__('Something completely different')
        # Test: aspect difference.
        target = copy.deepcopy(source)
        target._aspect = 'Something completely different'
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target._title._buffer.set_text('Something completely different', -1)
        assert not source.__eq__(target)
        # Test: equivalent
        target = copy.deepcopy(source)
        target._stale = True
        view = VUI.FACTORY_HEAD.new_title_view()
        target._title.attach_view(view)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, stock_args):
        """Confirm initialization."""
        # Setup
        # Test
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])

        assert stock_args['aspect'] == target._aspect
        assert id(target) == target._id
        assert not target._stale

        assert isinstance(target._title, AHEAD.AbstractTextModel)
        assert stock_args['title'] == str(target._title)

    def test_init_default(self, stock_args):
        """Confirm initialization with default arguments."""
        # Setup
        # Test
        target = MHEAD.Head(p_aspect=stock_args['aspect'])
        assert '' == str(target._title)

    def test_attach_page(self, stock_args):
        """Confirm page addition."""
        # Setup
        text_title_ui = 'Page title'
        PATH_DIR_TEST = Path(__file__).parent
        PATH_UI_NAME = PATH_DIR_TEST.parent / 'view' / 'test_page_head.ui'
        NAME_UI_FILE = str(PATH_UI_NAME)
        page_head = VHEAD.PageHead(NAME_UI_FILE)
        assert text_title_ui == page_head._title.get_text()
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test
        target.attach_page(page_head)
        assert page_head._title.get_text() == str(target._title)

    def test_detach_page(self, stock_args):
        """Confirm page removal."""
        # Setup
        text_title_ui = 'Page title'
        PATH_DIR_TEST = Path(__file__).parent
        PATH_UI_NAME = PATH_DIR_TEST.parent / 'view' / 'test_page_head.ui'
        NAME_UI_FILE = str(PATH_UI_NAME)
        page_head = VHEAD.PageHead(NAME_UI_FILE)
        assert text_title_ui == page_head._title.get_text()
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        target.attach_page(page_head)
        assert page_head._title.get_text() == str(target._title)
        # Test
        target.detach_page(page_head)
        assert stock_args['title'] == str(target._title)
        assert '' == page_head._title.get_text()

    def test_get_id(self, stock_args):
        """Confirm returns ID attribute."""
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test
        assert target.get_id() == target._id

    def test_get_aspect(self, stock_args):
        """Confirm returns aspect attribute."""
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test
        assert target.get_aspect() == target._aspect

    def test_is_fresh(self, stock_args):
        """Confirm return is accurate.

        #. Case: Head stale, title fresh
        #. Case: Head fresh, title stale
        #. Case: Head fresh, title fresh
        """
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test: Head stale, title fresh
        target._stale = True
        target._title.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: Head fresh, title stale
        target._stale = False
        target._title.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: Head fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        assert target.is_fresh()
        assert not target._stale

    def test_is_stale(self, stock_args):
        """Confirm return is accurate.

        #. Case: Head stale, title fresh
        #. Case: Head fresh, title stale
        #. Case: Head fresh, title fresh
        """
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test: Head stale, title fresh
        target._stale = True
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Head fresh, title stale
        target._stale = False
        target._title.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Head fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_set_fresh(self, stock_args):
        """Confirm all attributes set.

        #. Case: Head fresh, title fresh
        #. Case: Head stale, title fresh
        #. Case: Head fresh, title stale
        #. Case: Head stale, title stale
         """
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test: Head fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Head stale, title fresh
        target._stale = True
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Head fresh, title stale
        target._stale = False
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Head stale, title stale
        target._stale = True
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()

    def test_set_stale(self, stock_args):
        """Confirm all attributes set.

        #. Case: Head fresh, title fresh
        #. Case: Head stale, title fresh
        #. Case: Head fresh, title stale
        #. Case: Head stale, title stale
         """
        # Setup
        target = MHEAD.Head(
            p_aspect=stock_args['aspect'], p_title=stock_args['title'])
        # Test: Head fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._title.is_fresh()
        # Test: Head stale, title fresh
        target._stale = True
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._title.is_fresh()
        # Test: Head fresh, title stale
        target._stale = False
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._title.is_stale()
        # Test: Head stale, title stale
        target._stale = True
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._title.is_stale()
