"""
Defines generic, GTK-based classes implementing abstract outline
classes.  See :mod:`.abc_outline`.

Other classes specialize :class:`.AdaptTreeStore` and
:class:`.AdaptTreeView` for template, topic, form, and fact content.

.. data:: AdaptIndex

    GTK type for index of an item within an outline.
    See `Gtk.TreeIter`_.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html

.. data:: GenericItem

    Generic type for an item within an outline.
"""
import collections as COL
import copy
import gi   # type: ignore[import]
import itertools as IT
import logging
import typing

from factsheet.abc_types import abc_outline as ABC_OUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.adapt.outline')

AdaptIndex = typing.Union[Gtk.TreeIter]
GenericItem = typing.TypeVar('GenericItem')


class AdaptTreeStore(ABC_OUTLINE.AbstractOutline[
        AdaptIndex, GenericItem, 'AdaptTreeStore']):
    """Implements abstract :class:`.AbstractOutline` with generic item.

    ``AdaptTreeStore`` implements a generic outline using
    `Gtk.TreeStore`_ for storage and `Gtk.TreeIter`_ for index.

    .. _Gtk.TreeStore:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        TreeStore.html#Gtk.TreeStore

    .. data:: C_ITEM

        Identifies column containing items.
    """
    C_ITEM = 0

    def __init__(self) -> None:
        self._model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True if other is an outline with same structure and
        content as self.  Otherwise, return False.

        :param px_other: other object to compare to self.
        """
        if not isinstance(px_other, AdaptTreeStore):
            return False

        n_columns = self._model.get_n_columns()
        if n_columns != px_other._model.get_n_columns():
            return False

        for i in range(n_columns):
            if (self._model.get_column_type(i)
                    != px_other._model.get_column_type(i)):
                return False

        index_pairs = IT.zip_longest(self.indices(), px_other.indices())
        for i_self, i_other in index_pairs:
            if not i_self or not i_other:
                return False

            if self._model.get_string_from_iter(i_self) != (
                    px_other._model.get_string_from_iter(i_other)):
                return False

            if list(self._model[i_self]) != list(px_other._model[i_other]):
                return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return outline in form pickle can persist.

        Each item must support pickling.
        """
        state: typing.Dict[str, typing.Any] = self.__dict__.copy()
        ex_model = COL.OrderedDict()
        for index in self.indices():
            path_str = self._model.get_string_from_iter(index)
            ex_model[path_str] = self.get_item(index)
        state['ex_model'] = ex_model
        del state['_model']
        return state

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
        self._model = model
        del self.ex_model  # type: ignore[attr-defined]

    def deepcopy_section_child(self,
                               px_source: 'AdaptTreeStore',
                               px_i_source: AdaptIndex = None,
                               px_i_target: AdaptIndex = None) -> None:
        """Deepcopy section of another outline under given item.

        Method ``deepcopy_section_child`` copies the section after all
        existing children.  If index is None, it copies section at end
        of outline.  The method makes a deep copy of the section and
        each of its descendants.

        :param px_source: outline that contains section to copy.
        :param px_i_source: index of item to copy along with all
            descendents.  Default is to copy all items.
        :param px_i_target: index to copy section under.  Default
                is top level after existing top-level items.
        """
        if px_i_source is None:
            i_to = px_i_target
        else:
            row = [copy.deepcopy(e) for e in px_source._model[px_i_source]]
            i_to = self._model.append(px_i_target, row)

        i_from = px_source._model.iter_children(px_i_source)
        while i_from is not None:
            self.deepcopy_section_child(
                px_source=px_source, px_i_source=i_from, px_i_target=i_to)
            i_from = px_source._model.iter_next(i_from)

    def extract_section(self, px_i: AdaptIndex) -> None:
        """Remove section from outline.

        :param px_i: index of parent item to remove along with all
            descendants.  If index is None, remove all items.s
        """
        if px_i is None:
            self._model.clear()
        else:
            _ = self._model.remove(px_i)

    def find_next(self, px_target: typing.Any, px_i_after: AdaptIndex = None,
                  px_derive: typing.Callable[[typing.Any], typing.Any] = (
                      lambda v: v)) -> AdaptIndex:
        """Return index of next item where the target value equals value
        derived from item's content in given field, or None if no match.

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
            s_after = self._model.get_string_from_iter(px_i_after)
            for n, i in enumerate(indices):
                if s_after == self._model.get_string_from_iter(i):
                    break
            n_next = n + 1
            indices = indices[n_next:] + indices[:n_next]

        for i in indices:
            if px_target == px_derive(self._model[i][self.C_ITEM]):
                return i

        return None

    def get_item(self, px_i: AdaptIndex) -> typing.Optional[GenericItem]:
        """Returns item at given index or None when no item at index.

        Logs warning when index is None.
        :param px_i: index of desired item.
        """
        if px_i is None:
            logger.warning(
                'Invalid item index (None): ({}.{})'.format(
                    self.__class__.__name__, self.get_item.__name__))
            return None

        return self._model[px_i][self.C_ITEM]

    def indices(self, px_index: AdaptIndex = None
                ) -> typing.Iterator[AdaptIndex]:
        """Return iterator over indices of items in a section.

        The iterator is recursive (that is, includes items from sections
        within a section).

        :param px_index: index of parent item of section.  Default
            iterates over entire outline.
        """
        if px_index is None:
            index = self._model.get_iter_first()
        else:
            yield px_index
            index = self._model.iter_children(px_index)
        while index is not None:
            yield from self.indices(index)
            index = self._model.iter_next(index)

    def insert_after(self, px_item: GenericItem,
                     px_i: AdaptIndex) -> AdaptIndex:
        """Adds item to outline after item at given index.

        If index is None, adds item at beginning of outline.

        :param px_item: new item to add.
        :param px_i: index of item to precede new item.
        """
        PARENT = None
        return self._model.insert_after(PARENT, px_i, [px_item])

    def insert_before(self, px_item: GenericItem,
                      px_i: AdaptIndex) -> AdaptIndex:
        """Adds item to outline before item at given index.

        If index is None, adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of item to follow new item.
        """
        PARENT = None
        return self._model.insert_before(PARENT, px_i, [px_item])

    def insert_child(self, px_item: GenericItem,
                     px_i: AdaptIndex) -> AdaptIndex:
        """Adds item to outline as child of item at given index.

        Method adds item after all existing children.  If index is None,
        it adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of parent item for new item.
        """
        return self._model.append(px_i, [px_item])

    @property
    def model(self) -> Gtk.TreeStore:
        """Return outline model."""
        return self._model


class AdaptTreeView(ABC_OUTLINE.AbstractViewOutline[
        AdaptIndex, AdaptTreeStore[GenericItem]]):
    """Implements abstract :class:`.AbstractViewOutline`.

    ``AdaptTreeView`` implements a outline view using `Gtk.TreeView`_
    for presentation, :class:`.AdaptTreeStore` for storage, and
    `Gtk.TreeIter`_ for index.

    .. _Gtk.TreeView:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        TreeView.html#Gtk.TreeView
    """

    def __init__(self):
        self._view = Gtk.TreeView()
        self._selection = self._view.get_selection()
        self._selection.set_mode(Gtk.SelectionMode.BROWSE)

    def get_selected(self) -> typing.Optional[AdaptIndex]:
        """Return the index of the selected item or None when no item
        selected.
        """
        _model, index = self._selection.get_selected()
        return index

    def select(self, px_i: AdaptIndex = None) -> None:
        """Select the item at the given index.

        :param px_i: index of new selection.  If None, then no item is
            selected.
        """
        if px_i is None:
            self._selection.unselect_all()
        else:
            self._selection.select_iter(px_i)

    def set_model(self, pm_model: AdaptTreeStore[GenericItem]) -> None:
        """Associate given model with view.

        :param pm_model: outline model for view.
        """
        self._view.set_model(pm_model.model)

    def unselect_all(self) -> None:
        """Clear selection so that no item is selected."""
        self._selection.unselect_all()
