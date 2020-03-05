"""
Defines class to display identification information for Factsheet pages.
"""


import gi   # type: ignore[import]

from factsheet.adapt_gtk import adapt_view as AVIEW

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PageHead:
    """Provides display elements for page identification information.

    The identification information is common to `factesheet`, `topic`,
    and `fact` pages.  The class provides display element for a page's
    name, title, and summary.

    :param p_name_ui_file: name of file containing user interface
        definitions.
    """

    #: ID in user interface file for element to display page title.
    UI_ID_TITLE = 'ui_title_page_head'

    def __init__(self, p_name_ui_file: str):
        builder = Gtk.Builder.new_from_file(p_name_ui_file)
        get_object = builder.get_object

        self._title = get_object(self.UI_ID_TITLE)

    def get_title(self) -> AVIEW.AdaptEntry:
        """Return page's title display element."""
        return self._title
