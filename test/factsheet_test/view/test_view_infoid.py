"""
Unit tests for class to display page identification information.

See :mod:`.view_infoid`.
"""
import gi   # type: ignore[import]
from pathlib import Path
# import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_view as AVIEW
from factsheet.view import view_infoid as VINFOID

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestInfoId:
    """Unit tests for :class:`.ViewInfoId`."""

    PATH_TEST_DIR_UI = Path(__file__).parent
    NAME_TEST_FILE_UI = str(PATH_TEST_DIR_UI / 'test_view_infoid.ui')

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TEXT_TITLE_UI = 'Page title'
        builder = Gtk.Builder.new_from_file(self.NAME_TEST_FILE_UI)
        get_object = builder.get_object
        # Test
        target = VINFOID.ViewInfoId(get_object)
        assert isinstance(target._view_title, AVIEW.AdaptEntry)
        assert TEXT_TITLE_UI == target._view_title.get_text()

    def test_get_title(self):
        """Confirm return is title display element."""
        # Setup
        builder = Gtk.Builder.new_from_file(self.NAME_TEST_FILE_UI)
        get_object = builder.get_object
        target = VINFOID.ViewInfoId(get_object)
        # Test
        assert target.get_view_title() is target._view_title
