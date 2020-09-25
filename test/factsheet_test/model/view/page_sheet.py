"""
Defines class to display Factsheet document in a window.
"""
import gi   # type: ignore[import]
from pathlib import Path
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.control import control_sheet as CSHEET
from factsheet.control import pool as CPOOL
from factsheet.view import query_place as QPLACE
from factsheet.view import query_template as QTEMPLATE
from factsheet.view import scenes as VSCENES
from factsheet.view import view_infoid as VINFOID
from factsheet.view import form_topic as VTOPIC
from factsheet.view import types_view as VTYPES
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PageSheet(ABC_SHEET.InterfacePageSheet):
    """Displays Factsheet document and translates user actions.

    Class ``PageSheet`` maintains presentation of a Factsheet.  The
    class displays the content of a factsheet model.  It translates a
    user's actions at the user interface into requests to update the
    model and its presentation.

    :param px_app: application to which factsheet belongs.

    .. attribute:: NAME_FILE_DIALOG_DATA_LOSS_UI

       Path to user interface definition of data loss warning dialog.

    .. attribute:: NAME_FILE_SHEET_UI

       Path to user interface defintion of factsheet page.
    """

    NAME_FILE_SHEET_UI = str(UI.DIR_UI / 'sheet.ui')

    NAME_FILE_DIALOG_DATA_LOSS_UI = str(UI.DIR_UI / 'dialog_data_loss.ui')

    def __init__(self, *, px_app: Gtk.Application) -> None:
        self._control: typing.Optional[CSHEET.ControlSheet] = None
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_SHEET_UI)
        get_object = builder.get_object
        self._window = get_object('ui_sheet')
        self._window.set_application(px_app)

        # Components
        self._context_name = get_object('ui_context_name')
        self._context_summary = get_object('ui_context_summary')
        self._flip_summary = get_object('ui_flip_summary')

        self._view_topics = VTYPES.ViewOutlineTopics()
        self._view_topics.scope_search = ~ASHEET.FieldsTopic.VOID
        self._view_topics.gtk_view.set_reorderable(True)
        context_view_topics = get_object('ui_context_topics')
        context_view_topics.add(self._view_topics.gtk_view)
        self._cursor_topics = self._view_topics.gtk_view.get_selection()

        gtk_scenes_topic = get_object('ui_scenes_topic')
        self._scenes_topic = VSCENES.Scenes(
            gtk_scenes_topic, p_name_fixed='Default')

        self._dialog_data_loss, self._warning_data_loss = (
            self._init_dialog_warn())
        self._query_place: typing.Optional[QPLACE.QueryPlace] = None
        self._query_template: typing.Optional[QTEMPLATE.QueryTemplate] = None
        # self._query_template = QTEMPLATE.QueryTemplate(
        #     self._window, self._control.attach_view_topics)
        self._name_former: typing.Optional[str] = None
        self._infoid = VINFOID.ViewInfoId(get_object)

        self._close_window = False
        self._window.show_all()

        # Signals
        view_name = self._infoid.get_view_name()
        _id = view_name.connect(
            'activate', lambda _entry: self._context_name.popdown())
        _id = self._context_name.connect('closed', self.on_popdown_name)
        _id = self._cursor_topics.connect('changed', self.on_changed_cursor)
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
            self._window, 'popup-name', self.on_popup_name)
        UI.new_action_active(
            self._window, 'reset-name', self.on_reset_name)
        UI.new_action_active(
            self._window, 'flip-summary', self.on_flip_summary)
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

        # Topics Outline Toolbar
        search_bar = get_object('ui_search_bar')
        button_find = get_object('ui_find_topic')
        _binding = button_find.bind_property(
            'active', search_bar, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL)
        entry_find = get_object('ui_find_topic_entry')
        self._view_topics.gtk_view.set_search_entry(entry_find)
        UI.new_action_active(
            self._window, 'new-topic', self.on_new_topic)
        UI.new_action_active(
            self._window, 'go-first-topic', self.on_go_first_topic)
        UI.new_action_active(
            self._window, 'go-last-topic', self.on_go_last_topic)
        button_expand = get_object('ui_tool_expand_topics')
        _ = button_expand.connect(
            'clicked', lambda _b: self._view_topics.gtk_view.expand_all())
        button_collapse = get_object('ui_tool_collapse_topics')
        _ = button_collapse.connect(
            'clicked', lambda _b: self._view_topics.gtk_view.collapse_all())
        UI.new_action_active(
            self._window, 'delete-topic', self.on_delete_topic)
        UI.new_action_active(
            self._window, 'clear-topics', self.on_clear_topics)
        UI.new_action_active_dialog(
            self._window, 'show-help-topics',
            self.on_show_dialog, UI.HELP_SHEET_TOPICS)

        button_by_name = get_object('ui_find_by_name')
        _ = button_by_name.connect(
            'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.NAME)
        button_by_title = get_object('ui_find_by_title')
        _ = button_by_title.connect(
            'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.TITLE)

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

    def close_topic(self, p_id: VTYPES.TagTopic) -> None:
        """Close topic form in response to notice from model.

        Closing a topic form removes the pane from the factsheet page.

        :param p_id: identity of topic form to close.
        """
        name_scene = hex(p_id)
        self._scenes_topic.remove_scene(name_scene)

    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        return self._infoid

    def get_view_topics(self) -> ASHEET.AdaptTreeViewTopic:
        """Return view of factsheet's topic outline."""
        return self._view_topics

    @classmethod
    def link_factsheet(cls, pm_page: 'PageSheet',
                       pm_control: CSHEET.ControlSheet) -> None:
        """Initialize links between new page and new control for a
        factsheet.

        :param pm_page: new factsheet page.
        :param pm_control: new factsheet control.
        """
        pm_control.attach_page(pm_page)
        pm_page._control = pm_control
        query_view_topics = VTYPES.ViewOutlineTopics()
        pm_page._control.attach_view_topics(query_view_topics)
        pm_page._query_place = QPLACE.QueryPlace(
            pm_page._window, query_view_topics)
        pm_page._query_template = QTEMPLATE.QueryTemplate(
            pm_page._window, pm_page._control.attach_view_topics)

    def _make_dialog_file(self, p_action: Gtk.FileChooserAction
                          ) -> Gtk.FileChooserDialog:
        """Construct dialog to choose file for open or save.

        This helper method works around limitations in Glade.

        :param p_action: dialog box action (Open or Save).
        :returns: File chooser dialog.
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
        """Create factsheet with default contents and return window for it.

        :param px_app: application to which the factsheet belongs.
        :param pm_sheets_active: collection of active factsheets.
        :returns: Window for new factsheet.
        """
        page = PageSheet(px_app=px_app)
        control = CSHEET.ControlSheet.new(pm_sheets_active)
        PageSheet.link_factsheet(page, control)
        return page

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
        # id_none = self._scenes_topic.ID_NONE
        model, index = px_cursor.get_selected()
        if index is None:
            _ = self._scenes_topic.show_scene(None)
            return

        topic = AOUTLINE.get_item_gtk(model, index)
        if topic is None:
            _ = self._scenes_topic.show_scene(None)
            return

        name_topic = hex(topic.tag)
        name_visible = self._scenes_topic.show_scene(name_topic)
        if name_topic == name_visible:
            return

        control = self._control.get_control_topic(topic)
        if control is None:
            _ = self._scenes_topic.show_scene(None)
            return

        form = VTOPIC.FormTopic(p_control=control)
        self._scenes_topic.add_scene(form.gtk_pane, name_topic)
        _ = self._scenes_topic.show_scene(name_topic)

    def on_close_page(
            self, _widget: Gtk.Widget, _event: Gdk.Event) -> bool:
        """Close page guarding against data loss.

        A user may ask to close a factsheet page when there are unsaved
        changes that would be lost.  If so, the method includes checks
        to ensure the user approves.  The method closes the page
        unconditionally if no changes would be lost.  See also
        :meth:`close_page`.

        :returns: :data:`.CANCEL_GTK` or :data:`.CLOSE_GTK` to,
           respectively, cancel or continue page close.
        """
        assert self._control is not None
        if self._close_window:
            return UI.CLOSE_GTK

        effect = self._control.detach_page_safe(self)
        if effect is ABC_SHEET.EffectSafe.COMPLETED:
            return UI.CLOSE_GTK

        self._warning_data_loss.set_markup(
            'Factsheet "<b>{}</b>" contains unsaved changes.  All '
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
            return

        self._warning_data_loss.set_markup(
            'Factsheet "<b>{}</b>" contains unsaved changes.  All'
            'unsaved changes will be discarded if you close.'
            ''.format('Unnamed'))

        response = self._dialog_data_loss.run()
        self._dialog_data_loss.hide()
        if response == Gtk.ResponseType.APPLY:
            self._control.delete_force()

    def on_delete_topic(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Remove selected topic from the topics outline.

        If not topic is selected, then the topics outline is unchanged.
        """
        _model, index = self._cursor_topics.get_selected()
        if index is not None:
            assert self._control is not None
            self._control.extract_topic(index)

    def on_clear_topics(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Remove all topics from the topics outline."""
        assert self._control is not None
        self._control.clear()

    def on_flip_summary(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Flip visibility of summary pane."""
        new_state = not self._context_summary.get_visible()
        self._context_summary.set_visible(new_state)

    def on_go_first_topic(self, _action: Gio.SimpleAction,
                          _target: GLib.Variant) -> None:
        """Change selected topic to first topic."""
        gtk_model = self._view_topics.gtk_view.get_model()
        i_first = gtk_model.get_iter_first()
        if i_first is not None:
            self._cursor_topics.select_iter(i_first)

    def on_go_last_topic(self, _action: Gio.SimpleAction,
                         _target: GLib.Variant) -> None:
        """Change selected topic to last topic."""
        gtk_view = self._view_topics.gtk_view
        gtk_model = gtk_view.get_model()
        i_last = None
        n_children = gtk_model.iter_n_children(i_last)
        while 0 < n_children:
            i_last = gtk_model.iter_nth_child(i_last, n_children - 1)
            n_children = gtk_model.iter_n_children(i_last)
        if i_last is not None:
            path = gtk_model.get_path(i_last)
            gtk_view.expand_to_path(path)
            self._cursor_topics.select_iter(i_last)
            IGNORE = 0
            gtk_view.scroll_to_cell(path, None, False, IGNORE, IGNORE)

    def on_new_sheet(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Create a new factsheet with default contents."""
        assert self._control is not None
        app = self._window.get_application()
        sheets_active = self._control.sheets_active
        _page = PageSheet.new_factsheet(app, sheets_active)

    def on_new_topic(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Specify a new topic and add to topic outline.

        The method queries for the placement of new topic, the template
        for the topic, and topic contents.  The user may cancel at any
        of the queries.
        """
        gtk_model = self._view_topics.gtk_view.get_model()
        if len(gtk_model):
            assert self._query_place is not None
            placement = self._query_place()
        else:
            placement = QPLACE.Placement(None, QPLACE.Order.CHILD)
        if placement is None:
            return

        template = self._query_template()
        if template is None:
            return

        topic = template()
        if topic is None:
            return

        assert self._control is not None
        if placement.order is QPLACE.Order.AFTER:
            index, control = self._control.insert_topic_after(
                topic, placement.anchor)
        elif placement.order is QPLACE.Order.BEFORE:
            index, control = self._control.insert_topic_before(
                topic, placement.anchor)
        elif placement.order is QPLACE.Order.CHILD:
            index, control = self._control.insert_topic_child(
                topic, placement.anchor)
        else:
            raise NotImplementedError

        form = VTOPIC.FormTopic(p_control=control)
        name_topic = hex(topic.tag)
        self._scenes_topic.add_scene(form.gtk_pane, name_topic)
        path = gtk_model.get_path(index)
        self._view_topics.gtk_view.expand_to_path(path)
        self._cursor_topics.select_iter(index)

    def on_open_page(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Open another view of factsheet."""
        assert self._control is not None
        app = self._window.get_application()
        page = PageSheet(px_app=app)
        PageSheet.link_factsheet(page, self._control)

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

    def on_popdown_name(self, _popover: Gtk.Popover) -> None:
        """Hide factsheet name popover and notify control
        :class:`~.ControlSheet` when name changes."""
        assert self._control is not None
        if self._name_former != self._infoid.name:
            self._control.new_name()
        self._name_former = None

    def on_popup_name(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Show factsheet name popover and save former name."""
        self._context_name.popup()
        self._name_former = self._infoid.name

    def on_reset_name(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Reset name to value at start of name change."""
        view_name = self._infoid.get_view_name()
        view_name.set_text(self._name_former)

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
            dialog.set_current_name('factsheet.fsg')
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

    def on_toggle_search_field(self, px_button: Gtk.ToggleButton, p_field:
                               ASHEET.FieldsTopic) -> None:
        """Sets topic search to match active field buttons.

        :param px_button: button user toggled.
        :param p_field: search field of toggled button.
        """
        if px_button.get_active():
            self._view_topics.scope_search |= p_field
        else:
            self._view_topics.scope_search &= ~p_field

    @classmethod
    def open_factsheet(cls, px_app: Gtk.Application,
                       pm_sheets_active: CPOOL.PoolSheets, p_path: Path
                       ) -> typing.Optional['PageSheet']:
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
        open_time = Gtk.get_current_event_time()
        control_file = pm_sheets_active.owner_file(p_path)
        if control_file is not None:
            control_file.present_factsheet(open_time)
            return None

        page = PageSheet(px_app=px_app)
        control = CSHEET.ControlSheet.open(pm_sheets_active, p_path)
        PageSheet.link_factsheet(page, control)
        return page

    def present(self, p_time: int) -> None:
        """Make the page visible to user.

        Presents page to user even when page is an icon or covered by
        other windows.

        :param p_time: timestamp of event requesting presentation.
        """
        self._window.present_with_time(p_time)

    def set_titles(self, p_subtitle: str):
        """Set title and subtitle of page's window.

        The page's title is the factsheet name.

        :param p_subtitle: subtitle for window.
        """
        headerbar = self._window.get_titlebar()
        headerbar.set_title(self._infoid.name)
        headerbar.set_subtitle(p_subtitle)