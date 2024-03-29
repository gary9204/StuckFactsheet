"""
Defines class to display Factsheet document in a window.
"""
import gi
import logging
from pathlib import Path
import traceback as TB
import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
# from factsheet.view import query_place as QPLACE
# from factsheet.view import query_template as QTEMPLATE
import factsheet.view.editor_topics as VTOPICS
import factsheet.view.view_markup as VMARKUP
# from factsheet.view import scenes as VSCENES
# from factsheet.view import view_infoid as VINFOID
# from factsheet.view import form_topic as VTOPIC
# from factsheet.view import types_view as VTYPES
import factsheet.view.ui as UI
from factsheet.control.control_sheet import g_control_app

# Issue #249 stub
import factsheet.spec.base_s as SBASE

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # noqa: E402
from gi.repository import Gio   # noqa: E402
from gi.repository import GLib   # noqa: E402
from gi.repository import GObject as GO  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402
# from gi.repository import Pango   # noqa: E402

logger = logging.getLogger('Main.VSHEET')


class AppFactsheet(Gtk.Application):
    """Extends GTK application for factsheets."""

    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        """Register application with GTK.

        :param args: superclass positional parameters
        :param kwargs: superclass keyword parameters
        """
        super().__init__(application_id='com.novafolks.factsheet',
                         flags=Gio.ApplicationFlags.HANDLES_OPEN,
                         *args, **kwargs)

    def do_activate(self) -> None:
        """Create and display an initial factsheet with default content.

        Log initialization failure.
        """
        ViewSheet.on_new_sheet(None, None)

    def do_open(self, p_files: typing.Tuple[Gio.File], p_n_files: int,
                p_hint: str) -> None:
        """Create and display factsheets from file names on the
        command line.

        Log initialization failures.
        """
        logger.critical('Stub for open -- command line files ignored.')
        logger.critical('Files: {}.'.format(p_files))
        logger.critical('N: {}'.format(p_n_files))
        logger.critical('Hint: "{}".'.format(p_hint))
        control_sheet = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        if control_sheet is None:
            logger.critical(
                'Failed to create initial factsheet ({}.{})'
                ''.format(self.__class__.__name__, self.do_open.__name__))
            return
        _view = ViewSheet(p_control=control_sheet)

    def do_shutdown(self) -> None:
        """Application teardown. """
        Gtk.Application.do_shutdown(self)
        logger.info('AppFactsheet application shutdown.')

    def do_startup(self) -> None:
        """Application setup. """
        Gtk.Application.do_startup(self)
        logger.info('AppFactsheet application startup.')


def new_dialog_warn_loss(p_parent: Gtk.ApplicationWindow, p_name: str
                         ) -> Gtk.Dialog:
    """Return Data Loss Warning dialog.

    :param p_parent: window running dialog.
    :param p_name: name of factsheet that might lose data.

    .. note::
       There are limitations in Glade and Python bindings for GTK.
       Glade does not recognize use-header-bar property of GtkDialog.
       Gtk.Dialog() does not recognize flag
       Gtk.DialogFlags.USE_HEADER_BAR.

        To replace hard-coded ui definition with a Glade file, Manually
        add the following to GtkDialog section of the Glade file:

           `<property name="use-header-bar">1</property>`
    """

    form_dialog = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.22.1 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkDialog" id="ui_dialog_data_loss">
            <property name="use-header-bar">1</property>
            <property name="can_focus">False</property>
            <property name="title"
                translatable="yes">Data Loss Warning</property>
            <property name="modal">True</property>
            <property name="default_width">500</property>
            <property name="icon_name">dialog-warning</property>
            <property name="type_hint">dialog</property>
            <child type="titlebar">
              <placeholder/>
            </child>
            <child internal-child="vbox">
              <object class="GtkBox">
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <property name="spacing">2</property>
                <child internal-child="action_area">
                  <object class="GtkButtonBox">
                    <property name="can_focus">False</property>
                    <property name="layout_style">end</property>
                    <child>
                      <placeholder/>
                    </child>
                    <child>
                      <placeholder/>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkBox">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="margin_left">12</property>
                    <property name="margin_right">12</property>
                    <property name="margin_top">6</property>
                    <property name="margin_bottom">6</property>
                    <property name="orientation">vertical</property>
                    <property name="spacing">12</property>
                    <child>
                      <object class="GtkLabel" id="ui_warning">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label"
                            translatable="yes">Oops!</property>
                        <property name="use_markup">True</property>
                        <property name="justify">fill</property>
                        <property name="wrap">True</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkLabel">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="valign">start</property>
                        <property name="label"translatable="yes">{}</property>
                        <property name="use_markup">True</property>
                        <property name="justify">center</property>
                        <property name="wrap">True</property>
                      </object>
                      <packing>
                        <property name="expand">True</property>
                        <property name="fill">True</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
        </interface>
        """

    text_direct = ('&lt;i&gt;Cancel close, or continue to close and'
                   ' discard changes?&lt;/i&gt;'
                   )
    ui_dialog = form_dialog.format(text_direct)

    builder = Gtk.Builder.new_from_string(ui_dialog, len(ui_dialog))
    dialog = builder.get_object('ui_dialog_data_loss')
    dialog.set_transient_for(p_parent)
    dialog.set_destroy_with_parent(True)
    form_warn = ('Factsheet {} contains unsaved changes.  All unsaved'
                 ' changes will be discarded if you close.'
                 )
    text_warn = form_warn.format(p_name)
    warning = builder.get_object('ui_warning')
    warning.set_markup(text_warn)

    dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
    button_c = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
    style_c = button_c.get_style_context()
    style_c.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    dialog.add_button('Discard', Gtk.ResponseType.APPLY)
    button_d = dialog.get_widget_for_response(Gtk.ResponseType.APPLY)
    style_d = button_d.get_style_context()
    style_d.add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)

    return dialog


class ViewSheet(CSHEET.ObserverControlSheet):
    """Displays Factsheet document and translates user actions.

    Class :class:`~.ViewSheet` maintains presentation of a Factsheet.  The
    class displays the content of a factsheet model.  It translates a
    user's actions at the user interface into requests to update the
    model and its presentation.

    .. attribute:: NAME_FILE_DIALOG_DATA_LOSS_UI

       Path to user interface definition of data loss warning dialog.

    .. attribute:: NAME_FILE_SHEET_UI

       Path to user interface defintion of factsheet window.

    .. attribute:: ALLOW_CLOSE

        Indicates GTK should close a factsheet window.

    .. attribute:: DENY_CLOSE

        Indicates GTK should cancel closing a factsheet window.
    """

    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    NAME_FILE_DIALOG_DATA_LOSS_UI = str(UI.DIR_UI / 'dialog_data_loss.ui')

    ALLOW_CLOSE = False
    DENY_CLOSE = not ALLOW_CLOSE

    def __init__(self, *, p_control: CSHEET.ControlSheet) -> None:
        """Initialize sheet view and show window.

        :param p_control: control for factsheet to display.
        """
        self._control = p_control
        self._control.add_view(self)
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_SHEET_UI)
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        global g_app
        self._window.set_application(g_app)

        self._init_name_sheet(get_object)
        self._init_summary_sheet(get_object)
        self._init_title_sheet(get_object)
        self._init_topics(get_object)

        # Components
        # self._context_summary = get_object('ui_context_summary')
        # self._flip_summary = get_object('ui_flip_summary')

        # self._dialog_data_loss, self._warning_data_loss = (
        #     self._init_dialog_warn())
        # self._query_place: typing.Optional[QPLACE.QueryPlace] = None
        # self._query_template: typing.Optional[QTEMPLATE.QueryTemplate] = None
        # self._name_former: typing.Optional[str] = None
        # self._infoid = VINFOID.ViewInfoId(get_object)

        # self._close_window = False
        self._window.show_all()

        # Signals
        _id = self._window.connect('delete-event', self.on_close_view_sheet)

        # Application Title
        UI.new_action_active(self._window, 'open-sheet', self.on_open_sheet)
        UI.new_action_active(self._window, 'new-sheet', self.on_new_sheet)
        UI.new_action_active(self._window, 'save-sheet', self.on_save_sheet)
        UI.new_action_active(
            self._window, 'save-as-sheet', self.on_save_as_sheet)

        # Application Menu
        self._init_app_menu()
        self._init_factsheet_menu()

        # Factsheet Menu
        # UI.new_action_active_dialog(
        #     self._window, 'show-help-sheet',
        #     self.on_show_dialog, UI.HELP_SHEET)

        # Factsheet Display Menu
        # UI.new_action_active(
        #     self._window, 'flip-summary', self.on_flip_summary)
        UI.new_action_active(self._window, 'close-view-sheet',
                             lambda _a, _p: self._window.close())
        UI.new_action_active(self._window, 'open-view-sheet',
                             self.on_open_view_sheet)
        # UI.new_action_active_dialog(
        #     self._window, 'show-help-sheet-display',
        #     self.on_show_dialog, UI.HELP_SHEET_DISPLAY)

        # Factsheet File Menu
        UI.new_action_active(
            self._window, 'delete-sheet', self.on_delete_sheet)
        # UI.new_action_active_dialog(
        #     self._window, 'show-help-sheet-file',
        #     self.on_show_dialog, UI.HELP_SHEET_FILE)

        # Topics Outline Toolbar
        # Issue #249 stub
        search_bar = get_object('ui_search_bar')
        # button_find = get_object('ui_find_topic')
        # _binding = button_find.bind_property(
        #     'active', search_bar, 'search-mode-enabled',
        #     GO.BindingFlags.BIDIRECTIONAL)
        # entry_find = get_object('ui_find_topic_entry')
        # self._view_topics.gtk_view.set_search_entry(entry_find)

        # button_by_name = get_object('ui_find_by_name')
        # _ = button_by_name.connect(
        #     'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.NAME)
        # button_by_title = get_object('ui_find_by_title')
        # _ = button_by_title.connect(
        #     'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.TITLE)

    def _init_app_menu(self):
        """Initialize application menu.

        Create an action for each application menu dialog.
        """
        UI.new_action_active_dialog(
            self._window, 'show-intro-app', self.on_show_dialog, UI.INTRO_APP)
        UI.new_action_active_dialog(
            self._window, 'show-help-app', self.on_show_dialog, UI.HELP_APP)
        UI.new_action_active_dialog(
            self._window, 'show-about-app', self.on_show_dialog, UI.ABOUT_APP)

    def _init_factsheet_menu(self):
        """Initialize factsheet menu.

        Create an action for each factsheet menu dialog.
        """
        UI.new_action_active_dialog(self._window, 'show-help-sheet',
                                    self.on_show_dialog, UI.HELP_SHEET)

    def _init_name_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize editor for factsheet name.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_name = self._control.new_display_name()
        editor_name = self._control.new_editor_name()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        site_name_sheet = p_get_object('ui_site_name_sheet')
        site_name_sheet.pack_start(
            view_name.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

        # Work around for issue #231.
        title = Gtk.Label(label='Error! please report.', use_markup=True)
        title.set_selectable(False)
        _ = display_name.bind_property(
            'label', title, 'label', GO.BindingFlags.SYNC_CREATE)
        headerbar = self._window.get_titlebar()
        headerbar.set_custom_title(title)

    def _init_summary_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize view for factsheet summary.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        editor_summary = self._control.new_editor_summary()
        site_summary_sheet = p_get_object('ui_site_summary_sheet')
        site_summary_sheet.add(editor_summary)

        button_show = p_get_object('ui_button_show_summary_sheet')
        expander = p_get_object('ui_expander_summary_sheet')
        SYNC = GO.BindingFlags.BIDIRECTIONAL | GO.BindingFlags.SYNC_CREATE
        _binding = button_show.bind_property(
            'active', expander, 'visible', SYNC)

    def _init_title_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize editor for factsheet title.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_title = self._control.new_display_title()
        editor_title = self._control.new_editor_title()
        view_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        site_title_sheet = p_get_object('ui_site_title_sheet')
        site_title_sheet.pack_start(
            view_title.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def _init_topics(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize editor for topics outline.

        :param p_get_object: method to get visual element from user
            interface description.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 0

        site_topics = p_get_object('ui_site_topics')
        editor_topics = VTOPICS.EditorTopics(p_control_sheet=self._control)
        site_topics.pack_start(
            editor_topics.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def confirm_close(self):
        """Return :data:`ALLOW_CLOSE` when user approves closing view.
        Otherwise, return :data:`DENY_CLOSE`."""
        name = self._control.name
        dialog_warn = new_dialog_warn_loss(self._window, name)
        response = dialog_warn.run()
        dialog_warn.hide()
        if Gtk.ResponseType.APPLY == response:
            return ViewSheet.ALLOW_CLOSE
        else:
            return ViewSheet.DENY_CLOSE

    def erase(self) -> None:
        """Destroy visible portion of sheet view."""
        self._window.hide()
        self._window.destroy()

    def get_path(self, p_action: Gtk.FileChooserAction,
                 p_suggest: Path = None) -> typing.Optional[Path]:
        """Return path to factsheet file or None if user cancels.

        :param p_action: dialog box action (Open, Save, etc.).
        :param p_suggest: path to suggest to user.
        """
        dialog = self._make_file_chooser(p_action)
        if p_suggest is not None:
            _ = dialog.set_filename(str(p_suggest))
        elif Gtk.FileChooserAction.SAVE == p_action:
            dialog.set_current_name('factsheet.fsg')
        response = dialog.run()
        dialog.hide()
        path_new = None
        if response == Gtk.ResponseType.APPLY:
            path_new = Path(dialog.get_filename())
        del dialog
        return path_new

    def _make_file_chooser(self, p_action: Gtk.FileChooserAction
                           ) -> Gtk.FileChooserDialog:
        """Construct dialog to choose file for open or save.

        This helper method works around limitations in Glade.

        :param p_action: dialog box action (Open, Save, etc.).
        :returns: File chooser dialog.
        """

        dialog = Gtk.FileChooserDialog(action=p_action)
        dialog.set_transient_for(self._window)
        dialog.set_destroy_with_parent(True)
        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)

        if p_action == Gtk.FileChooserAction.SAVE:
            label = 'Save'
            dialog.set_do_overwrite_confirmation(True)
        elif p_action == Gtk.FileChooserAction.OPEN:
            label = 'Open'
        elif p_action == Gtk.FileChooserAction.CREATE_FOLDER:
            label = 'Create'
        else:
            label = 'Select'
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

        # Partial work around for issue #235.
        content_area = dialog.get_content_area()
        # print('Content: {}'.format(content_area))
        chooser_widget = content_area.get_children()[0]
        # print('Chooser: {}'.format(chooser_widget))
        action_bar = chooser_widget.get_children()[1]
        # print('Action bar: {}'.format(action_bar))
        filter_box = action_bar.get_children()[1]
        # print('Filter box: {}'.format(filter_box))
        filter_combo = filter_box.get_children()[0]
        # print('Filter combo: {}'.format(filter_combo))
        # print('\tHas tooltip: {}'.format(filter_combo.get_has_tooltip()))
        # print('\tTooltip: {}'.format(filter_combo.get_tooltip_text()))
        filter_combo.set_tooltip_text(None)
        # print('Clear tooltip')
        # print('\tHas tooltip: {}'.format(filter_combo.get_has_tooltip()))

        return dialog

    def on_close_view_sheet(
            self, _widget: Gtk.Widget, _event: Gdk.Event) -> bool:
        """Close view of factsheet."""
        if not self._control.remove_view_is_safe():
            if ViewSheet.DENY_CLOSE == self.confirm_close():
                return ViewSheet.DENY_CLOSE

        self._control.remove_view(self)
        return ViewSheet.ALLOW_CLOSE

    def on_delete_sheet(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Delete factsheet guarding against data loss.

        A user may ask to delete a factsheet when there are unsaved
        changes.  If so, the method includes checks to ensure the user
        approves.  The method deletes the factsheet unconditionally if
        no changes would be lost.
        """
        if self._control.is_stale():
            if ViewSheet.DENY_CLOSE == self.confirm_close():
                return

        CSHEET.g_control_app.close_factsheet(p_control=self._control)

    @classmethod
    def on_new_sheet(cls, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Create a new factsheet with default contents."""
        control_sheet = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=Gtk.get_current_event_time())
        if control_sheet is None:
            logger.critical(
                'Failed to create new factsheet ({}.{})'
                ''.format(cls.__name__, cls.on_new_sheet.__name__))
            return

        _view = ViewSheet(p_control=control_sheet)

    def on_open_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Create a factsheet with contents from file."""
        time = Gtk.get_current_event_time()
        path = self.get_path(Gtk.FileChooserAction.OPEN, None)
        if path is not None:
            control = g_control_app.open_factsheet(p_path=path, p_time=time)
            if control is not None:
                _view = ViewSheet(p_control=control)

    def on_open_view_sheet(self, _action: Gio.SimpleAction,
                           _target: GLib.Variant) -> None:
        """Open another view of factsheet."""
        _view_new = ViewSheet(p_control=self._control)

    def on_save_as_sheet(self, _action: Gio.SimpleAction,
                         _target: GLib.Variant) -> None:
        """Persist factsheet contents to file at new path."""
        path_update = self.get_path(
            Gtk.FileChooserAction.SAVE, self._control.path)
        if path_update is None:
            return

        self.save_sheet(path_update)

    def on_save_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Persist factsheet contents to file."""
        path_update = None
        if self._control.path is None:
            path_update = self.get_path(Gtk.FileChooserAction.SAVE, None)
            if path_update is None:
                return

        self.save_sheet(path_update)

    def on_show_dialog(self, _action: Gio.SimpleAction,
                       _target: GLib.Variant, p_dialog: Gtk.Dialog
                       ) -> None:
        """Display informational dialog.

        :param p_dialog: informational dialog.
        """
        p_dialog.set_transient_for(self._window)
        _ = p_dialog.run()
        p_dialog.hide()
        p_dialog.set_transient_for(None)

    def on_toggle_search_field(self, px_button: Gtk.ToggleButton, p_field
                               ) -> None:
        # ASHEET.FieldsTopic) -> None:
        """Sets topic search to match active field buttons.

        :param px_button: button user toggled.
        :param p_field: search field of toggled button.
        """
        raise NotImplementedError
        # if px_button.get_active():
        #     self._view_topics.scope_search |= p_field
        # else:
        #     self._view_topics.scope_search &= ~p_field

    def present(self, p_time: BUI.TimeEvent) -> None:
        """Make sheet view window visible to user.

        Make window visible even when it is an icon or covered by other
        windows.

        :param p_time: time stamp to order multiple requests.
        """
        self._window.present_with_time(p_time)

    def _report_error_sheet(self, p_err: Exception, p_message: str) -> None:
        """Display error dialog to user and log error details.

        :param p_err: error to display.
        :param p_message: primary text for error dialog.
        """
        logger.error(p_message)
        for line in TB.format_exception(
                type(p_err), p_err, p_err.__traceback__):
            logger.error(line)
        dialog = Gtk.MessageDialog(
            transient_for=self.window, message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK)
        dialog.set_markup(p_message)
        text_cause = 'Error source is Factsheet.'
        cause = p_err.__cause__
        if cause is not None:
            text_cause = 'Error source is {}: {}'.format(
                type(cause).__name__, cause)
        dialog.format_secondary_text(text_cause)
        dialog.run()
        dialog.destroy()

    def save_sheet(self, p_path_update: typing.Optional[Path] = None) -> None:
        """Save factsheet to file with basic error handling."""
        try:
            self._control.save(p_path_update)
        except CSHEET.BackupFileError as err:
            text_prime = 'Factsheet not saved! could not make backup.'
            self._report_error_sheet(err, text_prime)
        except CSHEET.DumpFileError as err:
            text_prime = 'Factsheet not saved! could not write file.'
            self._report_error_sheet(err, text_prime)
        except CSHEET.NoFileError as err:
            text_prime = 'Factsheet not saved! no file selected.'
            self._report_error_sheet(err, text_prime)
        except CSHEET.OpenFileError as err:
            text_prime = 'Factsheet not saved! could not open file.'
            self._report_error_sheet(err, text_prime)
        except Exception as err:
            text_prime = 'Factsheet not saved! Application is broken!'
            self._report_error_sheet(err, text_prime)

    @property
    def window(self) -> Gtk.ApplicationWindow:
        """Return visual element for sheet view."""
        return self._window


g_app = AppFactsheet()
