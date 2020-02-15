"""
factsheet.view.sheet - maintains presentation of factsheet in a window.
"""

import typing
import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class Sheet(Gtk.ApplicationWindow):
    """Presentation window for a fact sheet.

    View class Sheet maintains presentation of a factsheet.  The
    presentation consists of the collection of topics a user selects
    along with descriptive information for the factsheet.  The view
    includes both instance topics the user creates and template topics.
    Each instance topic has an information page.  The class implements
    methods to maintain the presentation in response to user actions
    (such as finding a topic or going to the table of contents for the
    factsheet).
    """

    def __init__(self, px_app):
        pass

    def on_close_view(self):
        """Close view of factsheet."""
        pass

    def on_delete_sheet(self):
        """Release control and close.
        Usage conflict: 1) user request and 2) notice from model
        """
        pass

    def on_new_sheet(self):
        """Create a new factsheet."""
        pass

    def on_open_view(self):
        """Open another view of factsheet."""
        pass
