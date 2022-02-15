"""
Defines class to display and edit topics outline of a Factsheet.

Types and Type Aliases
----------------------

.. data:: UiEditorTopics

    TBD
"""
import gi   # type: ignore[import]
import logging
import typing

from pathlib import Path

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.spec.base_s as SBASE
import factsheet.view.view_stack as VSTACK
import factsheet.view.ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib  # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango   # type: ignore[import]    # noqa: E402


UiEditorTopics = typing.Union[Gtk.Frame]

logger = logging.getLogger('Main.VTOPICS')


class EditorTopics:
    """TBD"""

    def __init__(self, p_control_sheet: CSHEET.ControlSheet) -> None:
        """Initialize topics outline, topics stack, and communication.

        Initialize topics outline.
            Get view of outline
            Make name column
            Add name to outline view as visible column
            Make title column
            Add to outline view as tooltip column
            Configure outline navigation

        Initialize topics stack
        Configuration communication between outline and stack

        """
        self._control_sheet = p_control_sheet
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_view = UI.GetUiViewByPath(p_path_ui=path_ui)
        self._ui_view = get_ui_view('ui_editor_topics')
        _actions = self._init_actions()
        self._dialog_help = get_ui_view('ui_help_outline_topics')
        self._init_outline_topics()
        site_topics = get_ui_view('ui_site_topics')
        site_topics.add(self._ui_outline_topics)
        self._init_views_topics()
        site_views = get_ui_view('ui_site_views')
        site_views.add(self._views_topics.ui_view)

    def _init_actions(self) -> Gio.SimpleActionGroup:
        """Initialize actions for buttons on topics outline toolbar."""
        actions = Gio.SimpleActionGroup()
        self._ui_view.insert_action_group('outline_topics', actions)
        handlers = {'clear-topics': self.on_clear_topics,
                    'collapse-outline': self.on_change_depth,
                    'delete-topic': self.on_delete_topic,
                    'expand-outline': self.on_change_depth,
                    'go-first-topic': self.on_go_first_topic,
                    'go-last-topic': self.on_go_last_topic,
                    'new-topic': self.on_new_topic,
                    'show-help': self.on_show_help,
                    'switch-columns': self.on_switch_columns,
                    }
        actions = self._ui_view.get_action_group('outline_topics')
        for name, handler in handlers.items():
            UI.new_action_active(
                p_group=actions, p_name=name, p_handler=handler)
        return actions

    def _init_outline_topics(self) -> None:
        """Initialize topics outline."""
        self._ui_outline_topics = self._control_sheet.new_view_topics()
        self._ui_selection = self._ui_outline_topics.get_selection()
        _id = self._ui_selection.connect('changed', self.on_changed_selection)
        self._column_name = self._new_column_name()
        self._ui_outline_topics.append_column(self._column_name)
        self._column_title = self._new_column_title()
        self._ui_outline_topics.append_column(self._column_title)

    def _init_views_topics(self) -> None:
        """Initialize stack of topic views."""
        self._views_topics = VSTACK.ViewStack()
        self._name_view_default = hex(0)
        view_default = Gtk.Label(
            label='Select a topic from the <i>Topics</i> outline.')
        view_default.set_use_markup(True)
        view_default.set_line_wrap(True)
        self._views_topics.add_view(view_default, self._name_view_default)
        self._views_topics.pin_view(self._name_view_default)

    def _markup_cell_name(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            _ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for name cell in the topics outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param _model: contains cell content (unused).
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        control_topic = self._control_sheet.get_control_topic(p_line)
        name = 'Missing'
        if control_topic is not None:
            name = control_topic.name
        p_render.set_property('markup', name)

    def _markup_cell_title(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            _ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for title cell in the topics outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param _model: contains cell content (unused).
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        control_topic = self._control_sheet.get_control_topic(p_line)
        title = 'Missing'
        if control_topic is not None:
            title = control_topic.title
        p_render.set_property('markup', title)

    def _new_column_name(self) -> Gtk.TreeViewColumn:
        """Return column for topic names."""
        column = Gtk.TreeViewColumn(title='Name')
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        column.set_cell_data_func(render, self._markup_cell_name)
        column.set_clickable(True)
        WIDTH_MIN = 12
        column.set_min_width(WIDTH_MIN)
        column.set_reorderable(True)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return column

    def _new_column_title(self) -> Gtk.TreeViewColumn:
        """Return column for topic titles."""
        column = Gtk.TreeViewColumn(title='Title')
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        column.set_cell_data_func(render, self._markup_cell_title)
        column.set_clickable(True)
        WIDTH_MIN = 12
        column.set_min_width(WIDTH_MIN)
        column.set_reorderable(True)
        column.set_visible(False)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return column

    def on_change_depth(
            self, p_action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Expand or collapse topics outline.

        :param p_action: user activated this action.
        :param _target: target of action (unused).
        """
        name = p_action.get_name()
        if 'collapse-outline' == name:
            self._ui_outline_topics.collapse_all()
        elif 'expand-outline' == name:
            self._ui_outline_topics.expand_all()
        else:
            logger.warning('Unexpected action: {} ({}.{})'
                           ''.format(name, self.__class__.__name__,
                                     self.on_change_depth.__name__))

    def on_changed_selection(self, _selection: Gtk.TreeSelection) -> None:
        """Expand outline

        :param _selection: selection that may have changed.
        """
        print('Enter on_change_selection')

    def on_clear_topics(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Remove all topics from the topics outline."""
        self._control_sheet.clear()

    def on_delete_topic(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Remove selected topic from the topics outline.

        If no topic is selected, then the topics outline is unchanged.
        """
        _model, line = self._ui_selection.get_selected()
        self._control_sheet.remove_topic(line)

    def on_go_first_topic(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Change selected topic to first topic in the outline.

        :param _action: user activated this action (unused).
        :param _target: target of action (unused).
        """
        model, _ = self._ui_selection.get_selected()
        line_first = model.get_iter_first()
        if line_first is not None:
            self._ui_selection.select_iter(line_first)

    def on_go_last_topic(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Change selected topic to last topic in the outline.

        :param _action: user activated this action (unused).
        :param _target: target of action (unused).
        """
        model, _ = self._ui_selection.get_selected()
        line_last = None
        n_children = model.iter_n_children(line_last)
        while 0 < n_children:
            line_last = model.iter_nth_child(line_last, n_children - 1)
            n_children = model.iter_n_children(line_last)
        if line_last is not None:
            path = model.get_path(line_last)
            view = self._ui_selection.get_tree_view()
            view.expand_to_path(path)
            self._ui_selection.select_iter(line_last)
            NO_COLUMN = None
            NO_ALIGN = False
            IGNORED = 0
            view.scroll_to_cell(path, NO_COLUMN, NO_ALIGN, IGNORED, IGNORED)

    def on_new_topic(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Specify a new topic and add to topic outline.

        The method queries for the placement of new topic, the template
        for the topic, and topic contents.  The user may cancel at any
        of the queries.
        """
        # Issue #249 stub
        spec = SBASE.Base(p_name='Cheese Shop',
                          p_summary='Please select any cheese in the shop!',
                          p_title='Cheese Specification')
        spec()
        return

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

    def on_show_help(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Display help dialog."""
        if self._dialog_help.get_transient_for() is None:
            parent = self._ui_view.get_toplevel()
            if parent.is_toplevel():
                self._dialog_help.set_transient_for(parent)
        _ = self._dialog_help.run()
        self._dialog_help.hide()

    def on_switch_columns(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Display help dialog."""
        visible_old = self._column_name.get_visible()
        self._column_name.set_visible(not visible_old)
        self._column_title.set_visible(visible_old)

    @property
    def ui_view(self) -> UiEditorTopics:
        """Return user interface element of topics editor."""
        return self._ui_view
