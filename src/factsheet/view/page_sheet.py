"""
Defines class to display Factsheet document in a window.
"""
import gi   # type: ignore[import]
import logging
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
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

class PageSheet(ABC_SHEET.InterfacePageSheet):
    """Displays Factsheet document and translates user actions.

    Class `PageSheet` maintains presentation of a Factsheet.  The class
    displays the content of a factsheet model.  It translates a user's
    actions at the user interface into requests to update the model and
    its presentation.

    :param px_app: application to which factsheet belongs
    :param kwargs: superclass keyword parameters
    """
    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    def __init__(self, *, px_app: Gtk.Application) -> None:
        self._control = None
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_SHEET_UI)
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        self._window.set_application(px_app)
        self._infoid = VINFOID.ViewInfoId(get_object)
        self._window.show_all()

        self._dialog_warn = get_object('ui_dialog_warn_data_loss')
        self._warning = get_object('ui_warning_data_loss')

        _id = self._window.connect('delete-event', self.on_close_page)

        UI.new_action_active(self._window, 'close_page_sheet',
                             lambda _w, _e: self._window.close())
        UI.new_action_active(
            self._window, 'new_sheet', self.on_new_sheet)
        UI.new_action_active(
            self._window, 'open_page_sheet', self.on_open_page)

        UI.new_action_active_dialog(self._window, 'show_about_app',
                                    self.on_show_dialog, UI.ABOUT_APP)
        UI.new_action_active_dialog(self._window, 'show_help_app',
                                    self.on_show_dialog, UI.HELP_APP)
        UI.new_action_active_dialog(self._window, 'show_intro_app',
                                    self.on_show_dialog, UI.INTRO_APP)

    def detach(self) -> None:
        """Stop observing model and close view.
        """
        raise NotImplementedError

    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        return self._infoid

    def on_close_page(
            self, _widget: Gtk.Widget, _event: Gdk.Event) -> bool:
        """Act on request to close view.

        A user may ask to close the last factsheet page when there are
        unsaved changes.  If so, the method gets user's approval before
        closing or cancels the request.  The method closes the page
        unconditionally if no changes would be lost.

        :returns: :data:`CANCEL_GTK` when user cancels page close.
        :returns: :data:`CLOSE_GTK` when user approves page close.
        """
        assert self._control is not None
        effect = self._control.detach_page_safe(self)
        if effect is ABC_SHEET.EffectSafe.COMPLETED:
            return UI.CLOSE_GTK

        self._warning.set_markup(
            'Factsheet "<b>{}</b>" contains unsaved changes.  All unsaved '
            'changes will be discarded if you close.'
            ''.format('Unnamed'))
        response = self._dialog_warn.run()
        self._dialog_warn.hide()
        if response == Gtk.ResponseType.APPLY:
            self._control.detach_page_force(self)
            return UI.CLOSE_GTK

        return UI.CANCEL_GTK

    def on_delete_sheet(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Act on request to delete factsheet.

        A user may ask to close a factsheet when there are unsaved
        changes.  If so, the method gets user's approval before closing
        or cancels the request.  The method closes the factsheet
        unconditionally if no changes would be lost.
        """
        raise NotImplementedError

    def on_load_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Act on request to load a factsheet from file."""
        raise NotImplementedError

    def on_new_sheet(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Act on request to create a new factsheet with default contents."""
        app = self._window.get_application()
        _control = PageSheet.new_factsheet(px_app=app)

    def on_open_page(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Act on request to open another view of factsheet."""
        assert self._control is not None
        app = self._window.get_application()
        page = PageSheet(px_app=app)
        self._control.attach_page(page)
        page._control = self._control

    def on_show_dialog(self, _action: Gio.SimpleAction,
                       _target: GLib.Variant, px_dialog: Gtk.Dialog
                       ) -> None:
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
    def new_factsheet(cls, px_app: Gtk.Application) -> CSHEET.Sheet:
        """Create factsheet with default contents.

        :param px_app: application to which the factsheet belongs.
        """
        page = PageSheet(px_app=px_app)
        control = CSHEET.Sheet.new()
        control.attach_page(page)
        page._control = control
        return control

    def update_name(self):
        """Update window title when sheet name changes."""
        raise NotImplementedError
