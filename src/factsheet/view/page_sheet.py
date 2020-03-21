"""
Defines class to display Factsheet document in a window.
"""
import gi   # type: ignore[import]
from pathlib import Path
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import sheet as CSHEET
from factsheet.control import pool as CPOOL
from factsheet.view import view_infoid as VINFOID
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PageSheet(ABC_SHEET.InterfacePageSheet):
    """Displays Factsheet document and translates user actions.

    Class `PageSheet` maintains presentation of a Factsheet.  The class
    displays the content of a factsheet model.  It translates a user's
    actions at the user interface into requests to update the model and
    its presentation.

    :param px_app: application to which factsheet belongs

    .. attribute:: NAME_FILE_DIALOG_DATA_LOSS_UI

       Path to user interface definition of data loss warning dialog.

    .. attribute:: NAME_FILE_SHEET_UI

       Path to user interface defintion of factsheet page.
    """
    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    NAME_FILE_DIALOG_DATA_LOSS_UI = str(UI.DIR_UI / 'dialog_data_loss.ui')

    def __init__(self, *, px_app: Gtk.Application) -> None:
#                  pm_sheets_active: CPOOL.PoolSheets) -> None:
        self._control: typing.Optional[CSHEET.Sheet] = None
#         self._sheets_active = pm_sheets_active
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_SHEET_UI)
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        self._window.set_application(px_app)

        self._dialog_data_loss, self._warning_data_loss = (
            self._init_dialog_warn())

        self._infoid = VINFOID.ViewInfoId(get_object)

        self._close_window = False
        self._window.show_all()

        _id = self._window.connect('delete-event', self.on_close_page)

        # Application Title
        UI.new_action_active(
            self._window, 'open-sheet', self.on_open_sheet)
        UI.new_action_active(
            self._window, 'new-sheet', self.on_new_sheet)
        UI.new_action_active(
            self._window, 'save-sheet', self.on_save_sheet)
        UI.new_action_active(
            self._window, 'save-as-sheet', self.on_save_as_sheet)

        # Application Menu
        UI.new_action_active_dialog(self._window, 'show-intro-app',
                                    self.on_show_dialog, UI.INTRO_APP)
        UI.new_action_active_dialog(self._window, 'show-help-app',
                                    self.on_show_dialog, UI.HELP_APP)
        UI.new_action_active_dialog(self._window, 'show-about-app',
                                    self.on_show_dialog, UI.ABOUT_APP)

        # Factsheet Menu
        UI.new_action_active_dialog(
            self._window, 'show-help-sheet',
            self.on_show_dialog, UI.HELP_SHEET)

        # Factsheet Display Menu
        UI.new_action_active(
            self._window, 'open-page-sheet', self.on_open_page)
        UI.new_action_active(self._window, 'close-page-sheet',
                             lambda _w, _e: self._window.close())
        UI.new_action_active_dialog(
            self._window, 'show-help-sheet-display',
            self.on_show_dialog, UI.HELP_SHEET_DISPLAY)

        # Factsheet File Menu
        UI.new_action_active(
            self._window, 'delete-sheet', self.on_delete_sheet)
        UI.new_action_active_dialog(
            self._window, 'show-help-sheet-file',
            self.on_show_dialog, UI.HELP_SHEET_FILE)

    def _init_dialog_warn(self) -> typing.Tuple[Gtk.Dialog, Gtk.Label]:
        """Construct Data Loss Warning dialog.

        This method works around limitations in Glade and
        Python bindings for GTK.  Glade does not recognize
        use-header-bar property of GtkDialog.  Gtk.Dialog() does not
        recognize flag Gtk.DialogFlags.USE_HEADER_BAR.

        Manually add the following to GtkDialog section of
        dialog_data_loss.ui:

               `<property name="use-header-bar">1</property>`
        """
        builder = Gtk.Builder.new_from_file(
            self.NAME_FILE_DIALOG_DATA_LOSS_UI)
        get_object = builder.get_object
        dialog = get_object('ui_dialog_data_loss')
        dialog.set_transient_for(self._window)
        dialog.set_destroy_with_parent(True)
        warning = get_object('ui_warning_data_loss')

        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        button_c = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
        style_c = button_c.get_style_context()
        style_c.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        dialog.add_button('Discard', Gtk.ResponseType.APPLY)
        button_d = dialog.get_widget_for_response(Gtk.ResponseType.APPLY)
        style_d = button_d.get_style_context()
        style_d.add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)

        return dialog, warning

    def close_page(self) -> None:
        """Close page unconditionally.

        This method provides direct means to clase a page, for example
        when closing all pages of a factsheet.
        """
        self._window.hide()
        self._close_window = True
        self._window.close()

    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        return self._infoid

    @classmethod
    def link_factsheet(cls, pm_page, pm_control) -> None:
        """Initialize links between new page and new control for a
        factsheet.
        """
        pm_control.attach_page(pm_page)
        pm_page._control = pm_control
#         pm_page._sheets_active.add(pm_control)

    def _make_dialog_file(self, p_action: Gtk.FileChooserAction
                          ) -> Gtk.FileChooserDialog:
        """Construct dialog to choose file for open or save.

        This helper method works around limitations in Glade.

        :param p_action: dialog box action (Open or Save).
        """
        dialog = Gtk.FileChooserDialog(action=p_action)
        dialog.set_transient_for(self._window)
        dialog.set_destroy_with_parent(True)
        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)

        label = 'Open'
        if p_action == Gtk.FileChooserAction.SAVE:
            label = 'Save'
            dialog.set_do_overwrite_confirmation(True)
        dialog.add_button(label, Gtk.ResponseType.APPLY)
        button_d = dialog.get_widget_for_response(
            Gtk.ResponseType.APPLY)
        style_d = button_d.get_style_context()
        style_d.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        filter_alpha = Gtk.FileFilter()
        filter_alpha.add_pattern('*.fsg')
        filter_alpha.set_name('Factsheet')
        dialog.add_filter(filter_alpha)

        filter_any = Gtk.FileFilter()
        filter_any.add_pattern('*')
        filter_any.set_name('Any')
        dialog.add_filter(filter_any)

        return dialog

    @classmethod
    def new_factsheet(cls, px_app: Gtk.Application,
                      pm_sheets_active: CPOOL.PoolSheets) -> 'PageSheet':
        """Create factsheet with default contents.

        :param px_app: application to which the factsheet belongs.
        :param pm_sheets_active: collection of active factsheets.
        """
        page = PageSheet(px_app=px_app)
        control = CSHEET.Sheet.new(pm_sheets_active)
        PageSheet.link_factsheet(page, control)
        return page

    def on_close_page(
            self, _widget: Gtk.Widget, _event: Gdk.Event) -> bool:
        """Close page guarding against data loss.

        A user may ask to close a factsheet page when there are unsaved
        changes that would be lost.  If so, the method includes checks
        to ensure the user approves.  The method closes the page
        unconditionally if no changes would be lost.  See also
        :meth:`close_page`.

        :returns: :data:`CANCEL_GTK` when user cancels page close.
        :returns: :data:`CLOSE_GTK` when user approves page close.
        """
        assert self._control is not None
        if self._close_window:
            return UI.CLOSE_GTK

        effect = self._control.detach_page_safe(self)
        if effect is ABC_SHEET.EffectSafe.COMPLETED:
            return UI.CLOSE_GTK

        self._warning_data_loss.set_markup(
            'Factsheet "<b>{}</b>" contains unsaved changes.  All'
            'unsaved changes will be discarded if you close.'
            ''.format('Unnamed'))

        response = self._dialog_data_loss.run()
        self._dialog_data_loss.hide()
        if response == Gtk.ResponseType.APPLY:
            self._control.detach_page_force(self)
            return UI.CLOSE_GTK

        return UI.CANCEL_GTK

    def on_delete_sheet(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Delete factsheet guarding against data loss.

        A user may ask to delete a factsheet when there are unsaved
        changes.  If so, the method includes checks to ensure the user
        approves.  The method deletes the factsheet unconditionally if
        no changes would be lost.
        """
        assert self._control is not None
        effect = self._control.delete_safe()
        if effect is ABC_SHEET.EffectSafe.COMPLETED:
#             self._sheets_active.remove(self._control)
            return

        self._warning_data_loss.set_markup(
            'Factsheet "<b>{}</b>" contains unsaved changes.  All'
            'unsaved changes will be discarded if you close.'
            ''.format('Unnamed'))

        response = self._dialog_data_loss.run()
        self._dialog_data_loss.hide()
        if response == Gtk.ResponseType.APPLY:
#             self._sheets_active.remove(self._control)
            self._control.delete_force()

    def on_new_sheet(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Create a new factsheet with default contents."""
        assert self._control is not None
        app = self._window.get_application()
        sheets_active = self._control.sheets_active
        _page = PageSheet.new_factsheet(app, sheets_active)

    def on_open_page(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Open another view of factsheet."""
        assert self._control is not None
        app = self._window.get_application()
        page = PageSheet(px_app=app)
        page._control = self._control
        page._control.attach_page(page)

    def on_open_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Create a factsheet with contents from file."""
        dialog = self._make_dialog_file(Gtk.FileChooserAction.OPEN)
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.APPLY:
            path_new = Path(dialog.get_filename())
            app = self._window.get_application()
            assert self._control is not None
            sheets_active = self._control.sheets_active
            _page = PageSheet.open_factsheet(app, sheets_active, path_new)
        del dialog

    def on_save_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Persist factsheet contents to file."""
        assert self._control is not None
        if self._control.path is None:
            self.on_save_as_sheet(None, None)
        else:
            self._control.save()

    def on_save_as_sheet(self, _action: Gio.SimpleAction,
                         _target: GLib.Variant) -> None:
        """Persist factsheet contents to file at new path."""
        assert self._control is not None
        path_old = self._control.path
        dialog = self._make_dialog_file(Gtk.FileChooserAction.SAVE)
        if path_old:
            _ = dialog.set_filename(str(path_old))
        else:
            dialog.set_current_name('Untitled.fsg')
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.APPLY:
            path_new = Path(dialog.get_filename())
            self._control.save_as(path_new)
        del dialog

    def on_show_dialog(self, _action: Gio.SimpleAction,
                       _target: GLib.Variant, px_dialog: Gtk.Dialog
                       ) -> None:
        """Display informational dialog.

        :param px_dialog: informational dialog.
        """
        px_dialog.set_transient_for(self._window)
        _ = px_dialog.run()
        px_dialog.hide()

    @classmethod
    def open_factsheet(cls, px_app: Gtk.Application,
                       pm_sheets_active: CPOOL.PoolSheets, p_path: Path
                       ) -> 'PageSheet':
        """Create factsheet with contents from file.

        :param px_app: application to which the factsheet belongs.
        :param p_path: path to file containing factsheet contents.
        """
        page = PageSheet(px_app=px_app)
        control = CSHEET.Sheet.open(pm_sheets_active, p_path)
        PageSheet.link_factsheet(page, control)
        return page

    def update_name(self):
        """Update window title when sheet name changes."""
        raise NotImplementedError
