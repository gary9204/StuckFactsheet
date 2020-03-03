"""
Unit tests for class to display page identification information.

See :mod:`.page_head`.
"""
from pathlib import Path
# import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_view as AVIEW
from factsheet.view import page_head as VHEAD


class TestPageHead:
    """Unit tests for :class:`.PageHead`."""

    PATH_DIR_TEST = Path(__file__).parent
    PATH_UI_FILE = PATH_DIR_TEST / 'test_page_head.ui'
    NAME_UI_FILE = str(PATH_UI_FILE)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        text_title_ui = 'Page title'
        # Test
        target = VHEAD.PageHead(self.NAME_UI_FILE)
        assert isinstance(target._title, AVIEW.AdaptEntry)
        assert text_title_ui == target._title.get_text()

    def test_get_title(self):
        """Confirm return is title display element."""
        # Setup
        target = VHEAD.PageHead(self.NAME_UI_FILE)
        # Test
        assert target.get_title() is target._title
