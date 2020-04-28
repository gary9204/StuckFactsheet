"""
Defines GTK-based classes implementing abstract factsheet component
classes.

See :mod:`.abc_sheet`.
"""
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class AdaptTreeStoreTemplate(
        AOUTLINE.AdaptTreeStore[ABC_SHEET.AbstractTemplate]):
    """Specializes :class:`.AdaptTreeStore` with
    :class:`.AbstractTemplate` items.
    """

    def find_name(self, px_target: str,
                  px_i_after: AOUTLINE.AdaptIndex = None
                  ) -> AOUTLINE.AdaptIndex:
        """Return index of next item where the target value equals the
        template name, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this name.
        :param px_i_after: start search immediately after item at this
            index. Default starts search at top item in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda item: item.name)

    def find_title(self, px_target: str,
                   px_i_after: AOUTLINE.AdaptIndex = None
                   ) -> AOUTLINE.AdaptIndex:
        """Return index of next item where the target value equals the
        template title, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this title.
        :param px_i_after: start search immediately after item at this
            index. Default starts search at top item in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda item: item.title)


class AdaptTreeViewTemplate(AOUTLINE.AdaptTreeView):
    """TBD"""

    def __init__(self):
        """Initialize view for topic hierarchy."""
        self._view = Gtk.TreeView()

    def set_model(   # type: ignore[override]
            self, px_outline: AdaptTreeStoreTemplate):
        """Set model along with columns and renderers for topic hierarchy."""
        self._view.set_model(px_outline._model)

        name = Gtk.TreeViewColumn(title='Name')
        self._view.append_column(name)
        name.set_clickable(True)
        name.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_name = Gtk.CellRendererText()
        name.set_cell_data_func(render_name, self._name_cell_data, None)
        name.pack_start(render_name, expand=False)

        title = Gtk.TreeViewColumn(title='Title')
        self._view.append_column(title)
        title.set_clickable(True)
        title.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_title = Gtk.CellRendererText()
        title.set_cell_data_func(render_title, self._title_cell_data, None)
        title.pack_start(render_title, expand=False)

        pad = Gtk.TreeViewColumn(title=' ')
        pad.set_expand(True)
        self._view.append_column(pad)

    def _name_cell_data(self, _column: Gtk.TreeViewColumn,
                        pm_renderer: Gtk.CellRenderer,
                        px_store: Gtk.TreeStore,
                        px_index: AOUTLINE.AdaptIndex,
                        _data: typing.Any = None) -> None:
        """Adapter to diaplay topic name in a tree view column.

        Formal Parameters
            _column: tree view column to display name.
            pm_renderer: cell renderer to display topic name.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        C_ITEM = 0
        template = px_store[px_index][C_ITEM]
        pm_renderer.set_property('markup', template.name)

    def _title_cell_data(self, _column: Gtk.TreeViewColumn,
                         pm_renderer: Gtk.CellRenderer,
                         px_store: Gtk.TreeStore,
                         px_index: AOUTLINE.AdaptIndex,
                         _data: typing.Any = None) -> None:
        """Adapter to display topic title in a tree view column.

        Formal Parameters
            _column: tree view column to display name.
            pm_renderer: cell renderer to display topic title.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        C_ITEM = 0
        template = px_store[px_index][C_ITEM]
        pm_renderer.set_property('markup', template.title)
