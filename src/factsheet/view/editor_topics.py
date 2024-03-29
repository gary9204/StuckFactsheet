"""
Defines class to display and edit topics outline of a Factsheet.

Types and Type Aliases
----------------------

.. data:: UiDisplayTopicsId

    Type alias for visual element for :class:`.DisplayTopicsId`.

.. data:: UiEditorTopics

    Type alias for visual element for :class:`.EditorTopics`.

.. data:: UiTopicSelection

    Type alias for element that selects current topic in
    :class:`.DisplayTopicsId`.

Classes
-------
"""
import gi   # type: ignore[import]
from gi.repository import Gio   # type: ignore[import]
from gi.repository import GLib   # type: ignore[import]
from gi.repository import GObject as GO   # type: ignore[import]
import logging
import typing

from pathlib import Path

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.view.id as VID
import factsheet.view.outline_id as VOUTLINE_ID
import factsheet.view.select_spec as VSELECT_SPEC
import factsheet.view.view_stack as VSTACK
import factsheet.view.view_topic as VTOPIC
import factsheet.view.ui as UI

# Stub Issue #264
import factsheet.model.topic as MTOPIC

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


UiActionMap = typing.Union[Gio.ActionMap]
UiDisplayTopicsId = typing.Union[Gtk.TreeView]
UiEditorTopics = typing.Union[Gtk.Frame]
UiTopicSelection = typing.Union[Gtk.TreeSelection]

logger = logging.getLogger('Main.VTOPICS')


class EditorTopics:
    """Displays topics outline along with current topic for editing."""

    def __init__(self, p_control_sheet: CSHEET.ControlSheet) -> None:
        """Initialize topics outline, topics stack, and communication.

        :param p_control_sheet: control for factsheet content to display.
        """
        self._control_sheet = p_control_sheet
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_element = UI.GetUiElementByPath(p_path_ui=path_ui)
        self._ui_view = get_ui_element('ui_editor_topics')
        PREFIX_ACTIONS_TOPICS = 'outline'
        actions = Gio.SimpleActionGroup()
        self._ui_view.insert_action_group(PREFIX_ACTIONS_TOPICS, actions)
        self.add_actions_to_group(p_action_group=actions)
        self._dialog_help = get_ui_element('ui_help_outline_topics')
        self._ui_topics = self._control_sheet.new_view_topics()
        # _ = VOUTLINE_ID.SetupUiDisplayOutlineId(
        #     p_ui_view=self._ui_topics, p_action_group=actions)
        _id = self._ui_topics.get_selection().connect(
            'changed', self.on_changed_selection)
        site_topics = get_ui_element('ui_site_topics')
        site_topics.add(self._ui_topics)
        self._init_views_topics()
        site_views = get_ui_element('ui_site_views')
        site_views.add(self._views_topics.ui_view)

        # Stub Issue #264
        _ = VOUTLINE_ID.InitColumnsOutlineId(self._ui_topics, actions)
        _ = VOUTLINE_ID.InitMotionOutlineId(self._ui_topics, actions)
        ui_search_id = Gtk.SearchBar(
            search_mode_enabled=True, show_close_button=True)
        site_search_id = get_ui_element('ui_site_find')
        site_search_id.add(ui_search_id)
        button_search = get_ui_element('ui_button_search')
        _binding = button_search.bind_property(
            'active', ui_search_id, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL | GO.BindingFlags.SYNC_CREATE)
        _ = VOUTLINE_ID.InitSearchOutlineId(self._ui_topics, ui_search_id)

        topic = MTOPIC.Topic(
            p_name='Topic 0', p_summary='Summary 0', p_title='Title 0')
        line_0 = self._control_sheet.insert_topic_after(
            p_topic=topic, p_line=None)
        topic = MTOPIC.Topic(
            p_name='Topic 0.0', p_summary='Summary 0.0', p_title='Title 0.0')
        line_x = self._control_sheet.insert_topic_child(
            p_topic=topic, p_line=line_0)
        topic = MTOPIC.Topic(
            p_name='Topic 0.0.0', p_summary='Summary 0.0.0', p_title='Title 0.0.0')
        _ = self._control_sheet.insert_topic_child(
            p_topic=topic, p_line=line_x)
        topic = MTOPIC.Topic(
            p_name='Topic 1', p_summary='Summary 1', p_title='Title 1')
        line_x = self._control_sheet.insert_topic_after(
            p_topic=topic, p_line=line_0)
        topic = MTOPIC.Topic(
            p_name='Topic 2', p_summary='Summary 2', p_title='Title 2')
        line_x = self._control_sheet.insert_topic_after(
            p_topic=topic, p_line=line_x)
        topic = MTOPIC.Topic(
            p_name='Topic 3', p_summary='Summary 3', p_title='Title 3')
        line_x = self._control_sheet.insert_topic_after(
            p_topic=topic, p_line=line_x)
        self._control_sheet._model.set_fresh()

    def _match_ne(
            self, _model: Gtk.TreeModel, _n_column: int, p_match_key: str,
            p_line: BUI.LineOutline, _extra: None):
        """Return False when given key is found with scope of search.

        Implements `Gtk.TreeViewSearchEqualFunc`_. Search scope can
        include any combination of spec name, summary, or title.

        :param _model: storage for spec outline visual element (unused).
        :param _n_column: model column to match (unused).
        :param p_match_key: key to match within search field(s).
        :param p_line: line to check for key.
        :param _extra: optional extra parameter (unused)

        .. _`Gtk.TreeViewSearchEqualFunc`::
            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        return False

    def add_actions_to_group(self, p_action_group: Gio.SimpleActionGroup
                             ) -> None:
        """Add editor actions to the given group.

        :param p_action_group: group of topic outline editor actions.
        """
        handlers = {'clear-topics': self.on_clear_topics,
                    'delete-topic': self.on_delete_topic,
                    'new-item': self.on_new_topic,
                    'show-help': self.on_show_help,
                    }
        for name, handler in handlers.items():
            UI.new_action_active(
                p_group=p_action_group, p_name=name, p_handler=handler)
        return

    def _init_views_topics(self) -> None:
        """Initialize stack of topic views."""
        self._views_topics = VSTACK.ViewStack()
        self._name_view_default = self.name_tag(CSHEET.TagTopic(0))
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

    @classmethod
    def name_tag(cls, p_tag: CSHEET.TagTopic) -> VSTACK.NameView:
        """Return view name corresponding to topic tag.

        :param p_tag: tag of topic to name.
        """
        return hex(p_tag)

    def on_changed_selection(self, p_selection: Gtk.TreeSelection) -> None:
        """Update item view shown when topics outline selection chenges.

        :param p_selection: selection that may have changed.
        """
        _model, line_current = p_selection.get_selected()
        # _model, line_current = self._ui_topics.get_selection().get_selected()
        if line_current is None:
            self._views_topics.show_view(self._name_view_default)
            return

        control_topic = self._control_sheet.get_control_topic(line_current)
        if control_topic is None:
            self._views_topics.show_view(self._name_view_default)
            logger.critical('Topic control roster inconsistent with '
                            'model topics outline. ({}.{})'
                            ''.format(self.__class__.__name__,
                                      self.on_changed_selection.__name__))
            return

        name_topic = self.name_tag(control_topic.tag)
        if name_topic not in self._views_topics:
            view_topic = VTOPIC.ViewTopic(p_control=control_topic)
            self._views_topics.add_view(view_topic.ui_view, name_topic)
        _ = self._views_topics.show_view(name_topic)
        return

    def on_clear_topics(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Remove all topics from the topics outline.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        self._control_sheet.clear()

    def on_delete_topic(self, _action: Gio.SimpleAction,
                        _target: GLib.Variant) -> None:
        """Remove selected topic from the topics outline.

        If no topic is selected, then the topics outline is unchanged.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        _model, line = self._ui_topics.get_selection().get_selected()
        self._control_sheet.remove_topic(line)

    def on_go_first_topic(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the first topic in the outline the selected topic.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        pass
        # model, _ = self._selection_topic.get_selected()
        # line_first = model.get_iter_first()
        # if line_first is not None:
        #     self._selection_topic.select_iter(line_first)

    def on_go_last_topic(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the last topic in the outline the selected topic.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        pass
        # model, _ = self._selection_topic.get_selected()
        # line_last = None
        # n_children = model.iter_n_children(line_last)
        # while 0 < n_children:
        #     line_last = model.iter_nth_child(line_last, n_children - 1)
        #     n_children = model.iter_n_children(line_last)
        # if line_last is not None:
        #     path = model.get_path(line_last)
        #     view = self._selection_topic.get_tree_view()
        #     view.expand_to_path(path)
        #     self._selection_topic.select_iter(line_last)
        #     NO_COLUMN = None
        #     NO_ALIGN = False
        #     IGNORED = 0
        #     view.scroll_to_cell(path, NO_COLUMN, NO_ALIGN, IGNORED, IGNORED)

    def on_new_topic(self, _action: Gio.SimpleAction,
                     _target: GLib.Variant) -> None:
        """Specify a new topic and add to topic outline.

        The method queries for the placement of new topic, the template
        for the topic, and topic contents.  The user may cancel at any
        of the queries.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        parent = self.ui_view.get_toplevel()
        select_spec = VSELECT_SPEC.SelectSpec(parent)
        spec = select_spec()
        if spec is not None:
            spec(self._control_sheet)
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
        # name_topic = self.name_tag(topic.id_topic)
        # self._scenes_topic.add_scene(pane.gtk_pane, name_topic)
        # path = gtk_model.get_path(index)
        # self._view_topics.gtk_view.expand_to_path(path)
        # self._cursor_topics.select_iter(index)

    def on_show_help(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Display help dialog.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        if self._dialog_help.get_transient_for() is None:
            parent = self._ui_view.get_toplevel()
            if parent.is_toplevel():
                self._dialog_help.set_transient_for(parent)
        _ = self._dialog_help.run()
        self._dialog_help.hide()

    def on_switch_columns(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Switch between showing name column and title column.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        pass
        # visible_old = self._column_name.get_visible()
        # self._column_name.set_visible(not visible_old)
        # self._column_title.set_visible(visible_old)

    @property
    def ui_view(self) -> UiEditorTopics:
        """Return visual element of topics editor."""
        return self._ui_view
