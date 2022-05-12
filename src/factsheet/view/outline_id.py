"""
Defines classes for visual elements of outline contining items with
identity information.
"""
import gi
from gi.repository import Gio
from gi.repository import GLib

import factsheet.bridge_ui as BUI
import factsheet.view.ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


UiDisplayOutlineId = Gtk.TreeView
UiSelectionOutlineId = Gtk.TreeSelection


class DisplayOutlineId:
    """Displays identity information for items in outline."""

    def __init__(self, p_ui_view: UiDisplayOutlineId) -> None:
        """Initialize visual element of outline.

        :param p_ui_view: visual element of outline to tailor.
        """
        self._ui_view = p_ui_view
        self._ui_selection = self._ui_view.get_selection()
        self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
        self._ui_view.append_column(self._column_name)
        self._column_title = UI.new_column_stock(
            'Title', self._markup_cell_title)
        self._ui_view.append_column(self._column_title)

    def add_actions_to_group(self, p_action_group: Gio.SimpleActionGroup
                             ) -> None:
        """Add display actions to the given group.

        :param p_action_group: group of outline's visual element actions.
        """
        handlers = {'collapse-outline': self.on_change_depth,
                    'expand-outline': self.on_change_depth,
                    'go-first': self.on_go_first_item,
                    'go-last': self.on_go_last_item,
                    'switch-columns': self.on_switch_columns,
                    }
        for name, handler in handlers.items():
            UI.new_action_active(
                p_group=p_action_group, p_name=name, p_handler=handler)
        return

    def _markup_cell_name(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for name cell in the outline's visual element.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param p_ui_model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
        name = 'Missing'
        if item_id is not None:
            name = item_id.name.text
        p_render.set_property('markup', name)

    def _markup_cell_title(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for title cell in the outline visual element.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param p_ui_model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
        title = 'Missing'
        if item_id is not None:
            title = item_id.title.text
        p_render.set_property('markup', title)

    def on_change_depth(
            self, p_action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Expand or collapse outline.

        :param p_action: user activated this action.
        :param _target: target of action (unused).
        """
        name = p_action.get_name()
        if 'collapse-outline' == name:
            self._ui_view.collapse_all()
        elif 'expand-outline' == name:
            self._ui_view.expand_all()
        else:
            self._ui_view.expand_all()

    def on_go_first_item(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the first item in the outline the selected item.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        # model, _ = self._ui_selection.get_selected()
        model = self._ui_view.get_model()
        line_first = model.get_iter_first()
        if line_first is not None:
            self._ui_selection.select_iter(line_first)

    def on_go_last_item(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the last item in the outline the selected item.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """

        model = self._ui_view.get_model()
        line_last = None
        n_children = model.iter_n_children(line_last)
        while 0 < n_children:
            line_last = model.iter_nth_child(line_last, n_children - 1)
            n_children = model.iter_n_children(line_last)
        if line_last is not None:
            path = model.get_path(line_last)
            self._ui_view.expand_to_path(path)
            self._ui_selection.select_iter(line_last)
            NO_COLUMN = None
            NO_ALIGN = False
            IGNORED = 0
            self._ui_view.scroll_to_cell(
                path, NO_COLUMN, NO_ALIGN, IGNORED, IGNORED)

    def on_switch_columns(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Switch between showing name column, title column, and both.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        if not self._column_name.get_visible():
            self._column_name.set_visible(True)
        elif self._column_title.get_visible():
            self._column_title.set_visible(False)
        else:
            self._column_name.set_visible(False)
            self._column_title.set_visible(True)

    @property
    def ui_selection(self) -> UiSelectionOutlineId:
        """Return visual element of outline display."""
        return self._ui_selection

    @property
    def ui_view(self) -> UiDisplayOutlineId:
        """Return visual element of outline display."""
        return self._ui_view
