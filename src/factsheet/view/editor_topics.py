"""
Defines class to display and edit topics outline of a Factsheet.

Types and Type Aliases
----------------------

.. data:: UiEditorTopics

    TBD
"""
import gi   # type: ignore[import]
import typing

from pathlib import Path

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.view.ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


UiEditorTopics = typing.Union[Gtk.Frame]


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
        self._ui_outline_topics = self._control_sheet.new_view_topics()
        site_topics = get_ui_view('ui_site_topics')
        site_topics.add(self._ui_outline_topics)
        column_name = self._new_column_name()
        self._ui_outline_topics.append_column(column_name)
        column_title = self._new_column_title()
        self._ui_outline_topics.append_column(column_title)
        self._init_buttons_depth(get_ui_view)

    def _init_buttons_depth(self, p_get_ui_view: UI.GetUiView) -> None:
        """Initialize buttons to expand and collapse the topics outline.

        :param p_get_ui_view: method to get user interface element.
        """
        button_collapse = p_get_ui_view('ui_tool_collapse_outline')
        _ = button_collapse.connect(
            'clicked', lambda _button: self._ui_outline_topics.collapse_all())
        button_expand = p_get_ui_view('ui_tool_expand_outline')
        _ = button_expand.connect(
            'clicked', lambda _button: self._ui_outline_topics.expand_all())

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
        column.set_resizable(True)
        column.set_reorderable(True)
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
        column.set_resizable(True)
        column.set_reorderable(True)
        return column

    @property
    def ui_view(self) -> UiEditorTopics:
        """Return user interface element of topics editor."""
        return self._ui_view
