"""
Unit tests for helper function to access GTK widget content.  See
:mod:`.gtk_helper`.
"""
import gi   # type: ignore[import]

from factsheet.content import gtk_helper as XHELPER

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestGtkSpec:
    """Unit test for :func:`.textbuffer_get_text`."""

    def test_textbuffer_get_text(self):
        """ """
        # Setup
        ALL = -1
        BLANK = ''
        TEXT = "Something completely different."
        target = Gtk.TextBuffer()
        # Test
        assert BLANK == XHELPER.textbuffer_get_text(target)
        target.set_text(TEXT, ALL)
        assert TEXT == XHELPER.textbuffer_get_text(target)
