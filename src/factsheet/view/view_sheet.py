"""
Defines class to display Factsheet document in a window.
"""
import gi   # type: ignore[import]
import logging
from pathlib import Path
import traceback as TB
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
# from factsheet.view import query_place as QPLACE
# from factsheet.view import query_template as QTEMPLATE
import factsheet.view.view_markup as VMARKUP
# from factsheet.view import scenes as VSCENES
# from factsheet.view import view_infoid as VINFOID
# from factsheet.view import form_topic as VTOPIC
# from factsheet.view import types_view as VTYPES
import factsheet.view.ui as UI
from factsheet.control.control_sheet import g_control_app

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
# from gi.repository import Pango   # type: ignore[import]    # noqa: E402

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

    :param px_app: application to which factsheet belongs.

    .. attribute:: NAME_FILE_DIALOG_DATA_LOSS_UI

       Path to user interface definition of data loss warning dialog.

    .. attribute:: NAME_FILE_SHEET_UI

       Path to user interface defintion of factsheet view.

    .. attribute:: ALLOW_CLOSE

        Indicates GTK should erase a factsheet view.

    .. attribute:: DENY_CLOSE

        Indicates GTK should cancel closing a factsheet view.
    """

    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    NAME_FILE_DIALOG_DATA_LOSS_UI = str(UI.DIR_UI / 'dialog_data_loss.ui')

    ALLOW_CLOSE = False
    DENY_CLOSE = not ALLOW_CLOSE

    def __init__(self, *, p_control: CSHEET.ControlSheet) -> None:
        """Initialize sheet view and show window.

        :param p_roster: roster of sheet views for factsheet.
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

        # Components
        # self._context_summary = get_object('ui_context_summary')
        # self._flip_summary = get_object('ui_flip_summary')

        # self._view_topics = VTYPES.ViewOutlineTopics()
        # self._view_topics.scope_search = ~ASHEET.FieldsTopic.VOID
        # self._view_topics.gtk_view.set_reorderable(True)
        # context_view_topics = get_object('ui_context_topics')
        # context_view_topics.add(self._view_topics.gtk_view)
        # self._cursor_topics = self._view_topics.gtk_view.get_selection()

        # gtk_scenes_topic = get_object('ui_scenes_topic')
        # self._scenes_topic = VSCENES.Scenes(
        #     gtk_scenes_topic, p_name_fixed='Default')

        # self._dialog_data_loss, self._warning_data_loss = (
        #     self._init_dialog_warn())
        # self._query_place: typing.Optional[QPLACE.QueryPlace] = None
        # self._query_template: typing.Optional[QTEMPLATE.QueryTemplate] = None
        # self._name_former: typing.Optional[str] = None
        # self._infoid = VINFOID.ViewInfoId(get_object)

        # self._close_window = False
        self._window.show_all()

        # Signals
        # view_name = self._infoid.get_view_name()
        # _id = view_name.connect(
        #     'activate', lambda _entry: self._context_name.popdown())
        # _id = self._context_name.connect('closed', self.on_popdown_name)
        # _id = self._cursor_topics.connect('changed', self.on_changed_cursor)
        _id = self._window.connect('delete-event', self.on_close_view_sheet)

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
        # search_bar = get_object('ui_search_bar')
        # button_find = get_object('ui_find_topic')
        # _binding = button_find.bind_property(
        #     'active', search_bar, 'search-mode-enabled',
        #     GO.BindingFlags.BIDIRECTIONAL)
        # entry_find = get_object('ui_find_topic_entry')
        # self._view_topics.gtk_view.set_search_entry(entry_find)
        # UI.new_action_active(
        #     self._window, 'new-topic', self.on_new_topic)
        # UI.new_action_active(
        #     self._window, 'go-first-topic', self.on_go_first_topic)
        # UI.new_action_active(
        #     self._window, 'go-last-topic', self.on_go_last_topic)
        # button_expand = get_object('ui_tool_expand_topics')
        # _ = button_expand.connect(
        #     'clicked', lambda _b: self._view_topics.gtk_view.expand_all())
        # button_collapse = get_object('ui_tool_collapse_topics')
        # _ = button_collapse.connect(
        #     'clicked', lambda _b: self._view_topics.gtk_view.collapse_all())
        # UI.new_action_active(
        #     self._window, 'delete-topic', self.on_delete_topic)
        # UI.new_action_active(
        #     self._window, 'clear-topics', self.on_clear_topics)
        # UI.new_action_active_dialog(
        #     self._window, 'show-help-topics',
        #     self.on_show_dialog, UI.HELP_SHEET_TOPICS)

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
        UI.new_action_active_dialog(self._window, 'show-intro-app',
                                    self.on_show_dialog, UI.INTRO_APP)
        UI.new_action_active_dialog(self._window, 'show-help-app',
                                    self.on_show_dialog, UI.HELP_APP)
        UI.new_action_active_dialog(self._window, 'show-about-app',
                                    self.on_show_dialog, UI.ABOUT_APP)

    def _init_factsheet_menu(self):
        """Initialize factsheet menu.

        Create an action for each factsheet menu dialog.
        """
        UI.new_action_active_dialog(self._window, 'show-help-sheet',
                                    self.on_show_dialog, UI.HELP_SHEET)

    def _init_name_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize editor for factsheet name."""
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_name = self._control.new_display_name()
        editor_name = self._control.new_editor_name()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        site_name_sheet = p_get_object('ui_site_name_sheet')
        site_name_sheet.pack_start(
            view_name.view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

        # Work around for issue #231.
        title = Gtk.Label(label='Error! please report.', use_markup=True)
        title.set_selectable(False)
        _ = display_name.bind_property(
            'label', title, 'label', GO.BindingFlags.SYNC_CREATE)
        headerbar = self._window.get_titlebar()
        headerbar.set_custom_title(title)

    def _init_summary_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize view for factsheet summary."""
        view_summary_active = self._control.new_editor_summary()
        site_summary_sheet = p_get_object('ui_site_summary_sheet')
        site_summary_sheet.add(view_summary_active)

        button_show = p_get_object('ui_button_show_summary_sheet')
        expander = p_get_object('ui_expander_summary_sheet')
        SYNC = GO.BindingFlags.BIDIRECTIONAL | GO.BindingFlags.SYNC_CREATE
        _binding = button_show.bind_property(
            'active', expander, 'visible', SYNC)

    def _init_title_sheet(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize editor for factsheet title."""
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_title = self._control.new_display_title()
        editor_title = self._control.new_editor_title()
        view_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        site_title_sheet = p_get_object('ui_site_title_sheet')
        site_title_sheet.pack_start(
            view_title.view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def erase(self) -> None:
        """Destroy visible portion of sheet view."""
        self._window.hide()
        self._window.destroy()

    def close_topic(self, p_id) -> None:
        # def close_topic(self, p_id: VTYPES.TagTopic) -> None:
        """Close topic pane in response to notice from model.

        Closing a topic pane removes the pane from the factsheet page.

        :param p_id: identity of topic pane to erase.
        """
        raise NotImplementedError
        # name_scene = hex(p_id)
        # self._scenes_topic.remove_scene(name_scene)

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

    def get_view_topics(self):  # -> ASHEET.AdaptTreeViewTopic:
        """Return view of factsheet's topic outline."""
        raise NotImplementedError
        # return self._view_topics

    @classmethod
    def link_factsheet(cls, pm_page: 'ViewSheet',
                       pm_control: CSHEET.ControlSheet) -> None:
        """Initialize links between new page and new control for a
        factsheet.

        :param pm_page: new factsheet page.
        :param pm_control: new factsheet control.
        """
        raise NotImplementedError
        # pm_control.attach_page(pm_page)
        # pm_page._control = pm_control
        # query_view_topics = VTYPES.ViewOutlineTopics()
        # pm_page._control.attach_view_topics(query_view_topics)
        # pm_page._query_place = QPLACE.QueryPlace(
        #     pm_page._window, query_view_topics)
        # pm_page._query_template = QTEMPLATE.QueryTemplate(
        #     pm_page._window, pm_page._control.attach_view_topics)

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

        return dialog

    @classmethod
    def new_factsheet(cls, px_app: Gtk.Application) -> 'ViewSheet':
        """Create factsheet with default contents and return window for it.

        :param px_app: application to which the factsheet belongs.
        :returns: Window for new factsheet.
        """
        pass
        # page = ViewSheet(px_app=px_app)
        # control = CSHEET.ControlSheet.new(pm_sheets_active)
        # ViewSheet.link_factsheet(page, control)
        # return page

    # def new_view_topics(self) -> VTYPES.ViewOutlineTopics:
    #     """Return new, unattached view of topics outline. """
    #     view_topics_new = VTYPES.ViewOutlineTopics()
    #     assert self._control is not None
    #     self._control.attach_view_topics(view_topics_new)
    #     return view_topics_new

    def on_changed_cursor(self, px_cursor: Gtk.TreeSelection) -> None:
        """Changes topic scene to match current topic.

        :param px_cursor: identifies now-current topic.
        """
        raise NotImplementedError
        # # id_none = self._scenes_topic.ID_NONE
        # model, index = px_cursor.get_selected()
        # if index is None:
        #     _ = self._scenes_topic.show_scene(None)
        #     return
        #
        # topic = AOUTLINE.get_item_gtk(model, index)
        # if topic is None:
        #     _ = self._scenes_topic.show_scene(None)
        #     return
        #
        # name_topic = hex(topic.id_topic)
        # name_visible = self._scenes_topic.show_scene(name_topic)
        # if name_topic == name_visible:
        #     return
        #
        # control = self._control.get_control_topic(topic)
        # if control is None:
        #     _ = self._scenes_topic.show_scene(None)
        #     return
        #
        # pane = VTOPIC.FormTopic(pm_control=control)
        # self._scenes_topic.add_scene(pane.gtk_pane, name_topic)
        # _ = self._scenes_topic.show_scene(name_topic)

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

    def on_delete_topic(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Remove selected topic from the topics outline.

        If not topic is selected, then the topics outline is unchanged.
        """
        raise NotImplementedError
        # _model, index = self._cursor_topics.get_selected()
        # if index is not None:
        #     assert self._control is not None
        #     self._control.extract_topic(index)

    def on_clear_topics(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Remove all topics from the topics outline."""
        raise NotImplementedError
        # assert self._control is not None
        # self._control.clear()

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

    def on_close_view_sheet(
            self, _widget: Gtk.Widget, _event: Gdk.Event) -> bool:
        """Close view of factsheet."""
        if not self._control.remove_view_is_safe():
            if ViewSheet.DENY_CLOSE == self.confirm_close():
                return ViewSheet.DENY_CLOSE

        self._control.remove_view(self)
        return ViewSheet.ALLOW_CLOSE

    def on_flip_summary(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Flip visibility of summary pane."""
        raise NotImplementedError
        # new_state = not self._context_summary.get_visible()
        # self._context_summary.set_visible(new_state)

    def on_go_first_topic(self, _action: Gio.SimpleAction,
                          _target: GLib.Variant) -> None:
        """Change selected topic to first topic."""
        raise NotImplementedError
        # gtk_model = self._view_topics.gtk_view.get_model()
        # i_first = gtk_model.get_iter_first()
        # if i_first is not None:
        #     self._cursor_topics.select_iter(i_first)

    def on_go_last_topic(self, _action: Gio.SimpleAction,
                         _target: GLib.Variant) -> None:
        """Change selected topic to last topic."""
        raise NotImplementedError
        # gtk_view = self._view_topics.gtk_view
        # gtk_model = gtk_view.get_model()
        # i_last = None
        # n_children = gtk_model.iter_n_children(i_last)
        # while 0 < n_children:
        #     i_last = gtk_model.iter_nth_child(i_last, n_children - 1)
        #     n_children = gtk_model.iter_n_children(i_last)
        # if i_last is not None:
        #     path = gtk_model.get_path(i_last)
        #     gtk_view.expand_to_path(path)
        #     self._cursor_topics.select_iter(i_last)
        #     IGNORE = 0
        #     gtk_view.scroll_to_cell(path, None, False, IGNORE, IGNORE)

    @classmethod
    def on_new_sheet(cls, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Create a new factsheet with default contents."""
        control_sheet = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=Gtk.get_current_event_time())
        if control_sheet is None:
            logger.critical('Failed to create new factsheet ({}.{})'
                            ''.format(cls.__name__,
                                      cls.on_new_sheet.__name__))
            return

        _view = ViewSheet(p_control=control_sheet)

    def on_new_topic(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Specify a new topic and add to topic outline.

        The method queries for the placement of new topic, the template
        for the topic, and topic contents.  The user may cancel at any
        of the queries.
        """
        raise NotImplementedError
        # gtk_model = self._view_topics.gtk_view.get_model()
        # if len(gtk_model):
        #     assert self._query_place is not None
        #     placement = self._query_place()
        # else:
        #     placement = QPLACE.Placement(None, QPLACE.Order.CHILD)
        # if placement is None:
        #     return
        #
        # template = self._query_template()
        # if template is None:
        #     return
        #
        # topic = template()
        # if topic is None:
        #     return
        #
        # assert self._control is not None
        # if placement.order is QPLACE.Order.AFTER:
        #     index, control = self._control.insert_topic_after(
        #         topic, placement.anchor)
        # elif placement.order is QPLACE.Order.BEFORE:
        #     index, control = self._control.insert_topic_before(
        #         topic, placement.anchor)
        # elif placement.order is QPLACE.Order.CHILD:
        #     index, control = self._control.insert_topic_child(
        #         topic, placement.anchor)
        # else:
        #     raise NotImplementedError
        #
        # pane = VTOPIC.FormTopic(pm_control=control)
        # name_topic = hex(topic.id_topic)
        # self._scenes_topic.add_scene(pane.gtk_pane, name_topic)
        # path = gtk_model.get_path(index)
        # self._view_topics.gtk_view.expand_to_path(path)
        # self._cursor_topics.select_iter(index)

    def on_open_view_sheet(self, _action: Gio.SimpleAction,
                           _target: GLib.Variant) -> None:
        """Open another view of factsheet."""
        _view_new = ViewSheet(p_control=self._control)

    def on_open_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Create a factsheet with contents from file."""
        time = Gtk.get_current_event_time()
        path = self.get_path(Gtk.FileChooserAction.OPEN, None)
        if path is not None:
            control = g_control_app.open_factsheet(p_path=path, p_time=time)
            if control is not None:
                _view = ViewSheet(p_control=control)

    def on_save_sheet(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Persist factsheet contents to file."""
        path_update = None
        if self._control.path is None:
            path_update = self.get_path(Gtk.FileChooserAction.SAVE, None)
            if path_update is None:
                return

        self.save_sheet(path_update)

    def on_save_as_sheet(self, _action: Gio.SimpleAction,
                         _target: GLib.Variant) -> None:
        """Persist factsheet contents to file at new path."""
        path_update = self.get_path(
            Gtk.FileChooserAction.SAVE, self._control.path)
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

    @classmethod
    def open_factsheet(cls, px_app: Gtk.Application, p_path: Path
                       ) -> typing.Optional['ViewSheet']:
        """Create factsheet with contents from file and return the new
        factsheet page.

        If a factsheet with the given file is active already, show all
        the pages corresponding to that factsheet file.  Return None in
        this case.

        :param px_app: application to which the factsheet belongs.
        :param pm_sheets_active: collection of factsheets.
        :param p_path: path to file containing factsheet contents.
        :returns: New page if one is created or None otherwise.
        """
        raise NotImplementedError
        # open_time = Gtk.get_current_event_time()
        # control_file = pm_sheets_active.owner_file(p_path)
        # if control_file is not None:
        #     control_file.present_factsheet(open_time)
        #     return None
        #
        # page = ViewSheet(px_app=px_app)
        # control = CSHEET.ControlSheet.open(pm_sheets_active, p_path)
        # ViewSheet.link_factsheet(page, control)
        # return page

    def present(self, p_time: BUI.TimeEvent) -> None:
        """Make sheet view visible to user.

        Make view visible even when it is an icon or covered by other
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

    def set_titles(self, p_subtitle: str):
        """Set title and subtitle of page's window.

        The page's title is the factsheet name.

        :param p_subtitle: subtitle for window.
        """
        raise NotImplementedError
        # headerbar = self._window.get_titlebar()
        # headerbar.set_title(self._infoid.name)
        # headerbar.set_subtitle(p_subtitle)

    @property
    def window(self) -> Gtk.ApplicationWindow:
        """Return visual element for sheet view."""
        return self._window


g_app = AppFactsheet()
