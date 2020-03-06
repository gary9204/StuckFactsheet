"""
Defines class to display Factsheet document in a window.
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

from factsheet.control import sheet as CSHEET
from factsheet.view import view_infoid as VINFOID
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.VSHEET')
logger.debug('Imported View Sheet module.')
# logger.propagate = True


# class PageSheet(VINFOID.ViewInfoId):

class PageSheet:
    """Displays Factsheet document and translates user actions.

    Class `PageSheet` maintains presentation of a Factsheet.  The class
    displays the content of a factsheet model.  It translates a user's
    actions at the user interface into requests to update the model and
    its presentation.

    :param px_app: application to which factsheet belongs
    :param kwargs: superclass keyword parameters
    """
    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    def __init__(self, *, px_app: Gtk.Application):
        self._control = None
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_SHEET_UI)
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        self._window.set_application(px_app)
        self._infoid = VINFOID.ViewInfoId(get_object)
        self._window.show_all()

        _id = self._window.connect('delete-event', self.on_close_view)

        UI.new_action_active_dialog(self._window, 'show_about_app',
                                    self.on_show_dialog, UI.ABOUT_APP)
        UI.new_action_active_dialog(self._window, 'show_help_app',
                                    self.on_show_dialog, UI.HELP_APP)
        UI.new_action_active_dialog(self._window, 'show_intro_app',
                                    self.on_show_dialog, UI.INTRO_APP)

    def detach(self):
        """Stop observing model and close view.
        """
        raise NotImplementedError

    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        return self._infoid

    def on_close_view(self, _widget: Gtk.Widget, _event: Gdk.Event):
        """Act on request to close view.

        A user may ask to close the last factsheet view when there are
        unsaved changes.  If so, get user's approval before closing or
        cancel the request.  Close unconditionally if no changes would
        be lost.
        """
        raise NotImplementedError
        assert self._control is not None
        allowed = self._control.detach_view_safe(self)
        if allowed:
            return not UI.CANCEL_GTK    # Stub - unconditional close

    def on_delete_sheet(self):
        """Act on request to delete factsheet."""
        raise NotImplementedError

    def on_load_sheet(self):
        """Act on request to load a factsheet from file."""
        raise NotImplementedError

    def on_new_sheet(self):
        """Act on request to create a new factsheet with default contents."""
        raise NotImplementedError

    def on_open_view(self):
        """Act on request to open another view of factsheet."""
        raise NotImplementedError

    def on_show_dialog(self, _action: Gio.SimpleAction,
                       _target: GLib.Variant, px_dialog: Gtk.Dialog):
        """Display informational dialog.

        :param px_dialog: informational dialog.
        """
        app = self._window.get_application()
        px_dialog.set_transient_for(app.get_windows()[0])
        _ = px_dialog.run()
        px_dialog.hide()

    @classmethod
    def open_factsheet(cls, px_app, px_path):
        """Create factsheet with model from file."""
        raise NotImplementedError

    @classmethod
    def new_factsheet(cls, px_app: Gtk.Application):
        """Create factsheet with default contents.

        :param px_app: application to which the factsheet belongs.
        """
        view = PageSheet(px_app=px_app)
        control = CSHEET.Sheet.new()
        control.attach_view(view)
        view._control = control
        return control

    def update_name(self):
        """Update window title when sheet name changes."""
        raise NotImplementedError
