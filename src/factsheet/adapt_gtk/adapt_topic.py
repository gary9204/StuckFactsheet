"""
Defines GTK-based classes implementing abstract topic component classes.
See :mod:`.abc_topic`.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html
"""
import enum
import gi   # type: ignore[import]
import typing

import factsheet.abc_types.abc_fact as ABC_FACT
import factsheet.adapt_gtk.adapt_outline as AOUTLINE
# import factsheet.model.fact as MFACT

from factsheet.adapt_gtk.adapt_outline import IndexGtk as IndexFact

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class AdaptTreeStoreFact(
        AOUTLINE.AdaptTreeStore[ABC_FACT.AbstractFact]):
    """Specializes :class:`.AdaptTreeStore` with :class:`.Fact` items."""

    def find_name(self, p_target: str, p_i_after: IndexFact = None
                  ) -> typing.Optional[IndexFact]:
        """Return index of first fact where the target value equals the
        fact name or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param p_target: search for this name.
        :param p_i_after: start search immediately after fact at this
            index. Default starts search at top fact in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            p_target, p_i_after, lambda fact: fact.name)

    def find_title(self, p_target: str,
                   p_i_after: IndexFact = None
                   ) -> IndexFact:
        """Return index of first fact where the target value equals the
        fact title or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param p_target: search for this title.
        :param p_i_after: start search immediately after fact at this
            index. Default starts search at top fact in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            p_target, p_i_after, lambda fact: fact.title)


class AdaptTreeViewFact(AOUTLINE.AdaptTreeView):
    """Specializes :class:`.AdaptTreeView` with name, title, and status
    columns for :class:`.AbstractFact` items.
    """

    def __init__(self):
        super().__init__()
        self._gtk_view.set_search_equal_func(self._test_field_ne, None)
        self._scope_search = FieldsFact.VOID

        self._gtk_view.set_search_column(AdaptTreeStoreFact.N_COLUMN_ITEM)
        self._gtk_view.set_enable_search(True)

        name = Gtk.TreeViewColumn(title='Name')
        self._gtk_view.append_column(name)
        name.set_clickable(True)
        name.set_resizable(True)
        # _ = name.get_button().get_preferred_size()
        render_name = Gtk.CellRendererText()
        name.set_cell_data_func(render_name, self._fill_name, None)
        name.pack_start(render_name, expand=False)

        status = Gtk.TreeViewColumn(title='Status')
        self._gtk_view.append_column(status)
        status.set_clickable(True)
        status.set_resizable(True)
        # _ = status.get_button().get_preferred_size()
        render_status = Gtk.CellRendererText()
        status.set_cell_data_func(render_status, self._fill_status, None)
        status.pack_start(render_status, expand=False)

        title = Gtk.TreeViewColumn(title='Title')
        self._gtk_view.append_column(title)
        title.set_clickable(True)
        title.set_resizable(True)
        # _ = name.get_button().get_preferred_size()
        render_title = Gtk.CellRendererText()
        title.set_cell_data_func(render_title, self._fill_title, None)
        title.pack_start(render_title, expand=False)

        pad = Gtk.TreeViewColumn(title=' ')
        self._gtk_view.append_column(pad)
        pad.set_expand(True)

    def _fill_name(self, _column: Gtk.TreeViewColumn,
                   p_render: Gtk.CellRenderer, p_store: Gtk.TreeStore,
                   p_i_row: IndexFact) -> None:
        """Adapter to diaplay fact name in a `Gtk.TreeIter`_ column.

        :param p_render: cell renderer to display fact name.
        :param p_store: store containing the fact.
        :param p_i_row: index of current row in store.
        """
        fact = AOUTLINE.get_item_gtk(p_store, p_i_row)
        assert fact is not None
        p_render.set_property('markup', fact.name)

    def _fill_status(self, _column: Gtk.TreeViewColumn,
                     p_render: Gtk.CellRenderer, p_store: Gtk.TreeStore,
                     p_i_row: IndexFact) -> None:
        """Adapter to display fact title in a `Gtk.TreeIter`_ column.

        :param p_render: cell renderer to display fact name.
        :param p_store: store containing the fact.
        :param p_i_row: index of current row in store.
        """
        fact = AOUTLINE.get_item_gtk(p_store, p_i_row)
        assert fact is not None
        p_render.set_property('markup', fact.status.name)

    def _fill_title(self, _column: Gtk.TreeViewColumn,
                    p_render: Gtk.CellRenderer, p_store: Gtk.TreeStore,
                    p_i_row: IndexFact) -> None:
        """Adapter to display fact title in a `Gtk.TreeIter`_ column.

        :param p_render: cell renderer to display fact name.
        :param p_store: store containing the fact.
        :param p_i_row: index of current row in store.
        """
        fact = AOUTLINE.get_item_gtk(p_store, p_i_row)
        assert fact is not None
        p_render.set_property('markup', fact.title)

    def _test_field_ne(self, p_model: Gtk.TreeModel, p_n_column: int,
                       p_value: str, p_index: Gtk.TreeIter, _user_data):
        """Return True when value is not equal to the contents of the
        active search field.

        Implements `Gtk.TreeViewSearchEqualFunc`_ for name and title
        search.

        .. _`Gtk.TreeViewSearchEqualFunc`::

            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        if not self._scope_search:
            return True

        fact = p_model[p_index][p_n_column]
        if self._scope_search & FieldsFact.NAME:
            if fact.name.startswith(p_value):
                return False

        if self._scope_search & FieldsFact.TITLE:
            if fact.title.startswith(p_value):
                return False

        if self._scope_search & FieldsFact.STATUS:
            if fact.status.name.startswith(p_value):
                return False

        path = p_model.get_path(p_index)
        _ = self._gtk_view.expand_row(path, False)
        return True

    @property
    def scope_search(self) -> 'FieldsFact':
        """Scope of facts outline search.

        The scope of search can be by fact name, by fact title, by
        fact status, or by any combination of the three.  The scope can
        be read or set, but not deleted.
        """
        return self._scope_search

    @scope_search.setter
    def scope_search(self, p_scope: 'FieldsFact') -> None:
        self._scope_search = p_scope


class FieldsFact(enum.Flag):
    """Identifies fact fields, which may be combined.

    .. data:: NAME

       Denotes fact name field.

    .. data:: STATUS

       Denotes fact status field.

    .. data:: TITLE

       Denotes fact title field.

    .. data:: VOID

       Denotes no field.
    """
    VOID = 0
    NAME = enum.auto()
    STATUS = enum.auto()
    TITLE = enum.auto()
