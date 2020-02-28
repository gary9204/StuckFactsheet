"""
Unit tests for GTK-based View classes that implement abstract View
classes.

See :mod:`.adapt_view`.
"""

import gi   # type: ignore[import]

from factsheet.adapt_gtk import adapt_view as AVIEW

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestAdaptEntry:
    """Unit tests for :data:`.AdaptEntry` implementation of
    :class:`.AbstractTextModel`.
    """

    def test_adapt_entry(self):
        """Confirm definition of :data:`.AdaptEntry`."""
        # Setup
        # Test
        assert AVIEW.AdaptEntry is Gtk.Entry


class TestAdaptTextView:
    """Unit tests for :data:`.AdaptTextView` implementation of
    :class:`.AbstractTextModel`."""

    def test_adapt_text_view(self):
        """Confirm definition of :data:`.AdaptTextView`."""
        # Setup
        # Test
        assert AVIEW.AdaptTextView is Gtk.TextView
