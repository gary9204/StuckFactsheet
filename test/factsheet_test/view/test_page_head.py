"""
Unit tests for class to display page identification information.

See :mod:`.page_head`.
"""
import os.path
# import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_view as AVIEW
from factsheet.view import page_head as VHEAD


class TestPageHead:
    """Unit tests for :class:`.PageHead`."""

    UI_DIR = os.path.abspath(os.path.dirname(__file__))
    NAME_UI_FILE = UI_DIR + '/test_page_head.ui'

    def test_init(self):
        """Confirm initialization."""
        # Setup
        text = 'Page title'
        # Test
        target = VHEAD.PageHead(self.NAME_UI_FILE)
        assert isinstance(target._title, AVIEW.AdaptEntry)
        assert text == target._title.get_text()

    def test_get_title(self):
        """Confirm return is title display element."""
        # Setup
        target = VHEAD.PageHead(self.NAME_UI_FILE)
        # Test
        assert target.get_title() is target._title
