"""
Defines generic, GTK-based classes implementing abstract outline
classes.  See :mod:`.abc_outline`.

Other classes specialize :class:`.AdaptTreeStore` and
:class:`.AdaptTreeView` for template, topic, form, and fact content.

.. data:: IndexGtk

    GTK type for index of an item within an outline.
    See `Gtk.TreeIter`_.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html

.. data:: ItemOpaque

    Generic type for an item within an outline.
"""
import collections as COL
import gi   # type: ignore[import]
import itertools as IT
import logging
import typing

import factsheet.abc_types.abc_outline as ABC_OUTLINE

from factsheet.abc_types.abc_outline import ItemOpaque

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.adapt.outline')

IndexGtk = typing.Union[Gtk.TreeIter]
# ItemOpaque = typing.TypeVar('ItemOpaque')


class AdaptTreeView(ABC_OUTLINE.AbstractViewOutline[IndexGtk]):
    """Implements abstract :class:`.AbstractViewOutline`.

    ``AdaptTreeView`` implements a outline view using `Gtk.TreeView`_
    for presentation, :class:`.AdaptTreeStore` for storage, and
    `Gtk.TreeIter`_ for index.

    .. _Gtk.TreeView:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        TreeView.html#Gtk.TreeView
    """

    def __init__(self):
        self._gtk_view = Gtk.TreeView()
        self._selection = self._gtk_view.get_selection()
        self._selection.set_mode(Gtk.SelectionMode.BROWSE)

    def get_selected(self) -> typing.Optional[IndexGtk]:
        """Return the index of the selected item or None when no item
        selected.
        """
        _model, index = self._selection.get_selected()
        return index

    @property
    def gtk_view(self) -> Gtk.TreeView:
        """Return underlying presentation element."""
        return self._gtk_view

    def select(self, px_i: IndexGtk = None) -> None:
        """Select the item at the given index.

        :param px_i: index of new selection.  If None, then no item is
            selected.
        """
        if px_i is None:
            self._selection.unselect_all()
        else:
            self._selection.select_iter(px_i)

    def unselect_all(self) -> None:
        """Clear selection so that no item is selected."""
        self._selection.unselect_all()


class AdaptTreeStore(ABC_OUTLINE.AbstractOutline[
        IndexGtk, ItemOpaque, 'AdaptTreeStore', AdaptTreeView]):
    """Implements abstract :class:`.AbstractOutline` with generic item.

    ``AdaptTreeStore`` implements a generic outline using
    `Gtk.TreeStore`_ for storage and `Gtk.TreeIter`_ for index.

    .. _Gtk.TreeStore:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        TreeStore.html#Gtk.TreeStore

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
        Transient aspects of the outlines (like views) are not compared
        and may be different.

    .. data:: N_COLUMN_ITEM

        Identifies column containing items.
    """
    N_COLUMN_ITEM = 0

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True if other is an outline with same structure and
        content as self.  Otherwise, return False.

        :param px_other: other object to compare to self.
        """
        if not isinstance(px_other, AdaptTreeStore):
            return False

        n_columns = self._gtk_model.get_n_columns()
        if n_columns != px_other._gtk_model.get_n_columns():
            return False

        for i in range(n_columns):
            if (self._gtk_model.get_column_type(i)
                    != px_other._gtk_model.get_column_type(i)):
                return False

        index_pairs = IT.zip_longest(self.indices(), px_other.indices())
        for i_self, i_other in index_pairs:
            if not i_self or not i_other:
                return False

            if self._gtk_model.get_string_from_iter(i_self) != (
                    px_other._gtk_model.get_string_from_iter(i_other)):
                return False

            if list(self._gtk_model[i_self]) != (
                    list(px_other._gtk_model[i_other])):
                return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return outline in form pickle can persist.

        Each item must support pickling.
        """
        state: typing.Dict[str, typing.Any] = self.__dict__.copy()
        ex_model = COL.OrderedDict()
        for index in self.indices():
            path_str = self._gtk_model.get_string_from_iter(index)
            ex_model[path_str] = self.get_item(index)
        state['ex_model'] = ex_model
        del state['_gtk_model']
        del state['_views']

        return state

    def __init__(self) -> None:
        self._gtk_model = Gtk.TreeStore(GO.TYPE_PYOBJECT)
        self._views: typing.Dict[int, AdaptTreeView] = dict()

    def __ne__(self, px_other: typing.Any) -> bool:
        """Return False if other is an outline with same structure and
        content as self.  Otherwise, return True.

        :param px_other: other object to compare to self.
        """
        return not self.__eq__(px_other)

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct outline from state pickle loads.

        Each item must support unpickling.

        :param px_state: unpickled state of stored outline.
        """
        self.__dict__.update(px_state)
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)
        for path_str, item in (
                self.ex_model.items()):  # type: ignore[attr-defined]
            path = Gtk.TreePath(path_str)
            if path.get_depth() < 2:
                i_parent = None
            else:
                _ = path.up()
                i_parent = model.get_iter(path)
            model.append(i_parent, [item])
        self._gtk_model = model
        del self.ex_model  # type: ignore[attr-defined]
        self._views = dict()

    def attach_view(self, pm_view_outline: AdaptTreeView):
        """Add view to update display when outline changes.

        :param pm_view: view to add.
        """
        id_view_outline = id(pm_view_outline)
        if id_view_outline in self._views:
            logger.warning(
                'Duplicate view: {} ({}.{})'.format(
                    hex(id_view_outline),
                    self.__class__.__name__, self.attach_view.__name__))
            return

        pm_view_outline._gtk_view.set_model(self._gtk_model)
        self._views[id_view_outline] = pm_view_outline

    def clear(self) -> None:
        """Remove all sections from outline."""
        self._gtk_model.clear()

    def detach_view(self, pm_view_outline: AdaptTreeView) -> None:
        """Remove view of changes to outline.

        :param pm_view: view to remove.
        """
        id_view_outline = id(pm_view_outline)
        try:
            view = self._views.pop(id_view_outline)
            view.gtk_view.set_model(None)
        except KeyError:
            logger.warning(
                'Missing view: {} ({}.{})'.format(
                    hex(id_view_outline),
                    self.__class__.__name__, self.detach_view.__name__))

    def extract_section(self, px_i: IndexGtk) -> None:
        """Remove section from outline.

        :param px_i: index of parent item to remove along with all
            descendants.  If index is None, remove no items.
        """
        if px_i is not None:
            _ = self._gtk_model.remove(px_i)

    def find_next(self, px_target: typing.Any, px_i_after: IndexGtk = None,
                  px_derive: typing.Callable[[typing.Any], typing.Any] = (
                      lambda v: v)) -> IndexGtk:
        """Return index of next item where the target value equals value
        derived from item's content in given field or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this value.
        :param px_i_after: start search immediately after item at this
            index.  Default starts search at top item in outline.
        :param px_derive: function to derive value to compare to target
                value.  Function takes input from given field.  Default
                uses field content unaltered.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        indices = list(self.indices())

        if px_i_after is not None:
            s_after = self._gtk_model.get_string_from_iter(px_i_after)
            for n, i in enumerate(indices):
                if s_after == self._gtk_model.get_string_from_iter(i):
                    break
            n_next = n + 1
            indices = indices[n_next:] + indices[:n_next]

        for i in indices:
            if px_target == px_derive(
                    self._gtk_model[i][self.N_COLUMN_ITEM]):
                return i

        return None

    def get_item(self, px_i: IndexGtk) -> typing.Optional[ItemOpaque]:
        """Return item at given index or None when no item at index.

        Logs warning when no item at index.

        :param px_i: index of desired item.
        """
        return get_item_gtk(self._gtk_model, px_i)

    def indices(self, px_index: IndexGtk = None
                ) -> typing.Iterator[IndexGtk]:
        """Return iterator over indices of items in a section.

        The iterator is recursive (that is, includes items from sections
        within a section).

        :param px_index: index of parent item of section.  Default
            iterates over entire outline.
        """
        if px_index is None:
            index = self._gtk_model.get_iter_first()
        else:
            yield px_index
            index = self._gtk_model.iter_children(px_index)
        while index is not None:
            yield from self.indices(index)
            index = self._gtk_model.iter_next(index)

    def insert_after(self, px_item: ItemOpaque,
                     px_i: IndexGtk) -> IndexGtk:
        """Adds item to outline after item at given index.

        If index is None, adds item at beginning of outline.

        :param px_item: new item to add.
        :param px_i: index of item to precede new item.
        :returns: index of newly-added item.
        """
        PARENT = None
        return self._gtk_model.insert_after(PARENT, px_i, [px_item])

    def insert_before(self, px_item: ItemOpaque,
                      px_i: IndexGtk) -> IndexGtk:
        """Adds item to outline before item at given index.

        If index is None, adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of item to follow new item.
        :returns: index of newly-added item.
        """
        PARENT = None
        return self._gtk_model.insert_before(PARENT, px_i, [px_item])

    def insert_child(self, px_item: ItemOpaque,
                     px_i: IndexGtk) -> IndexGtk:
        """Adds item to outline as child of item at given index.

        Method adds item after all existing children.  If index is None,
        it adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of parent item for new item.
        :returns: index of newly-added item.
        """
        return self._gtk_model.append(px_i, [px_item])

    def insert_section(self, px_source: 'AdaptTreeStore',
                       px_i_source: IndexGtk = None,
                       px_i_target: IndexGtk = None) -> None:
        """Copy section of another outline under given item.

        Method ``insert_section`` copies the section after all existing
        children.  If px_i_target is None, it copies section at end of
        outline.  The method makes a shallow copy of the section and
        each of its descendants.

        .. note:: This method makes a shallow copy.  The outlines share
            the templates after the copy.

        :param px_source: outline that contains section to copy.
        :param px_i_source: index of item to copy along with all
            descendents.  Default is to copy all items.
        :param px_i_target: index to copy section under.  Default
                is top level after existing top-level items.
        """
        if px_i_source is None:
            i_to = px_i_target
        else:
            row = list(px_source._gtk_model[px_i_source])
            i_to = self._gtk_model.append(px_i_target, row)

        i_from = px_source._gtk_model.iter_children(px_i_source)
        while i_from is not None:
            self.insert_section(
                px_source=px_source, px_i_source=i_from, px_i_target=i_to)
            i_from = px_source._gtk_model.iter_next(i_from)


def get_item_gtk(px_model: Gtk.TreeModel, px_i: IndexGtk
                 ) -> typing.Optional[ItemOpaque]:
    """Return item at given index in GTK-model of outline model or None.

    Return None when no item at index and logs warning.

    .. warning:: Expects GTK model to have structure defined in
        :class:`.AdaptTreeStore`.

    :param px_model: GTK model of an outline model
    :param px_i: index of desired item.
    """
    item = None
    try:
        item = px_model[px_i][AdaptTreeStore.N_COLUMN_ITEM]
    except TypeError:
        id_index = hex(id(px_i)) if px_i else 'None'
        logger.warning(
            'Invalid item index ({}): ({})'
            ''.format(id_index, get_item_gtk.__name__))

    return item
