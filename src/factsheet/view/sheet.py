"""
factsheet.view.sheet - maintains presentation of factsheet in a window.
"""

import gi   # type: ignore[import]
import logging
import typing   # noqa

from factsheet.types_abstract import abc_sheet as ASHEET
from factsheet.control import sheet as CSHEET
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.VSHEET')
logger.debug('Imported View Sheet module.')
# logger.propagate = True


class Sheet(ASHEET.ObserverSheet):
    """Presentation window for a fact sheet.

    View class Sheet maintains presentation of a factsheet.  The
    presentation consists of the collection of topics a user selects
    along with descriptive information for the factsheet.  The class
    implements methods to maintain the presentation in response to user
    actions (such as finding a topic or going to the table of contents
    for the factsheet).

    :param px_app: application to which factsheet belongs
    """

    def __init__(self, *, px_app: Gtk.Application):
        self._control = None

        # Window elements
        builder = Gtk.Builder.new_from_file(UI.UI_DIR + 'sheet.ui')
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        self._window.set_application(px_app)
        # Signals
        _id = self._window.connect('delete-event', self.on_close_view)
        #
        self._window.show_all()

    def detach(self):
        """Stop observing model and close view.
        """
        raise NotImplementedError

    def on_close_view(self, _widget: Gtk.Widget, _event: Gdk.Event):
        """Act on request to close view.

        A user may ask to close the last factsheet view when there are
        unsaved changes.  If so, get user's approval before closing or
        cancel the request.  Close unconditionally if no changes would
        be lost.
        """
        allowed = self._control.detach_view_safe(self)
        if allowed:
            return ASHEET.CONTINUE_GTK    # Stub - unconditional close

    def on_delete_sheet(self):
        """Act on request to delete factsheet."""
        raise NotImplementedError

    def on_load_sheet(self):
        """Act on request to load a factsheet from file."""
        raise NotImplementedError

    def on_new_sheet(self):
        """Act on request to reate a new factsheet with default contents."""
        raise NotImplementedError

    def on_open_view(self):
        """Act on request to open another view of factsheet."""
        raise NotImplementedError

    @classmethod
    def open_factsheet(cls, px_app, px_path):
        """Create factsheet with model from file."""
        raise NotImplementedError

    @classmethod
    def new_factsheet(cls, px_app: Gtk.Application):
        """Create factsheet with default contents.

        :param px_app: application to which the factsheet belongs.
        """
        view = Sheet(px_app=px_app)
        control = CSHEET.Sheet.new()
        control.attach_view(view)
        view._control = control
        return control

    def update_name(self):
        """Update window title when sheet name changes."""
        raise NotImplementedError
