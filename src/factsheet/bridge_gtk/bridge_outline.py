"""
Defines bridge classes to encapsulate widget toolkit outline classes.

An outline is an ordered list analogous to a bulleted list in a print
document.  An outline contains lines, each of which identifies an item.
Lines and items are analogous to bullets and text in a bulleted list.
Like a bulleted list, an outline may be either single-level or multi-
level.

.. data:: ItemOpaque

    Placeholder type hint for an item at a line.

.. data:: LineOpaque

    Placeholder type hint for a line in an outline.

.. data:: LineOutline

    Type hint for GTK element to store a line.  See `Gtk.Treeiter`_.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html

.. data:: ModelOutline

    Type hint for GTK element to store a an outline.  See
    :data:`ModelOutlineSingle`, :data:`ModelOutlineMulti`, and
    `Gtk.TreeModel`_.

.. _`Gtk.TreeModel`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeModel.html

.. data:: ModelOutlineMulti

    Type hint for GTK element to store a multi-level outline.  See
    `Gtk.TreeStore`_.

.. _`Gtk.TreeStore`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeStore.html

.. data:: ModelOutlineSingle

    Type hint for GTK element to store a single-level outline.  See
    `Gtk.ListStore`_ .

.. _`Gtk.ListStore`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ListStore.html

.. data:: OutlineOpaque

    Placeholder type hint for an outline.

.. data:: PersistOutline

    Type hint for outline representation suitable for persistent
    storage.

.. data:: ViewOutlineColumnar

    Type hint for GTK element to view an outline in columnar format.
    See `Gtk.TreeView`_.

.. _`Gtk.TreeView`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeView.html

.. data:: ViewOutlineOpaque

    Type hint for GTK element to view an outline.  See
    :data:`ViewOutlineColumnar` and :data:`ViewOutlineSelect`.

.. data:: ViewOutlineSelect

    Type hint for GTK element to view an outline as a selection.
    See `Gtk.ComboBox`_.

.. _`Gtk.ComboBox`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ComboBox.html
    """
import abc
import gi   # type: ignore[import]
import typing

from . import bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

ItemOpaque = typing.TypeVar('ItemOpaque')

ChooserItem = typing.Union[Gtk.ComboBox]
LineOutline = typing.Union[Gtk.TreeIter]
PersistOutline = typing.MutableMapping[str, ItemOpaque]
# UiModelOutline = typing.Union[Gtk.TreeModel]
UiModelOutlineMulti = typing.Union[Gtk.TreeStore]
UiModelOutlineSingle = typing.Union[Gtk.ListStore]
UiModelOutline = typing.TypeVar(
    'UiModelOutline', UiModelOutlineMulti, UiModelOutlineSingle)
ViewOutline = typing.Union[Gtk.TreeView]

# LineOpaque = typing.TypeVar('LineOpaque')
# ModelOutline = typing.Union[Gtk.TreeModel]
# ModelOutlineMulti = typing.Union[Gtk.TreeStore]
# ModelOutlineSingle = typing.Union[Gtk.ListStore]
# ViewOutlineOpaque = typing.TypeVar(
#     'ViewOutlineOpaque', ViewOutlineColumnar, ViewOutlineSelect)


class ModelOutline(BBASE.BridgeBase[UiModelOutline, PersistOutline],
                   typing.Generic[UiModelOutline, ItemOpaque]):
    """
    Common ancestor of bridge classes for outlines.

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
    """

    _ui_model: UiModelOutline
    _C_ITEM = 0

    def __init__(self, **kwargs: typing.Any) -> None:
        """Initialize instance.

        Subclasses must define attributes for name, summary, and title
        before calling :meth:`.IdCore.__init__`.

        :param kwargs: superclass keyword parameters.
        """
        # if kwargs:
        #     raise TypeError('{}.__init__() called with extra argument(s): '
        #                     '{}'.format(type(self).__name__, kwargs))
        # type_hints = typing.get_type_hints(self.__class__)
        # for name, hint in type_hints.items():
        #     if not hasattr(self, name):
        #         raise AttributeError(
        #             '{}: ModelOutline subclasses must define {} '
        #             'attribute with type {} and then call '
        #             'super().__init__()'.format(
        #                 self.__class__.__name__, name, hint))
        self._set_persist(dict())

    def clear(self) -> None:
        """Remove all items from outline."""
        raise NotImplementedError
        self._ui_model.clear()

    def get_item(self, p_line: LineOutline) -> typing.Optional[ItemOpaque]:
        """Return item at given line or None when no item at line.

        :param p_line: line of desired item.
        """
        raise NotImplementedError
        return self.get_item_direct(self._ui_model, p_line)

    @classmethod
    def get_item_direct(cls, p_model: UiModelOutline, p_line: LineOutline
                        ) -> typing.Optional[ItemOpaque]:
        """Return item at given line directly from outline storage element.

        :param p_model: outline storage element.
        :param p_line: line containing desired item.
        """
        raise NotImplementedError
        return p_model.get_value(p_line, cls._C_ITEM)

    def _get_persist(self) -> PersistOutline:
        """Return outline in form suitable for persistent storage."""
        raise NotImplementedError
        persist: PersistOutline = dict()
        for line in self.lines():
            path = self._ui_model.get_string_from_iter(line)
            item = self.get_item(line)
            persist[path] = item
        return persist

    @abc.abstractmethod
    def insert_after(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline after given line.

        If line is None, prepend item at beginning of outline.

        :param p_item: new item to add.
        :param p_line: line to precede new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def insert_before(self, p_item: ItemOpaque,
                      p_line: LineOutline = None) -> LineOutline:
        """Add item to outline before given line.

        If line is None, append item at end of outline.

        :param p_item: new item to add.
        :param p_line: line to follow new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError

    def items(self) -> typing.Iterator[typing.Optional[ItemOpaque]]:
        """Return iterator over items in outline."""
        for line in self.lines():
            yield self.get_item(line)

    @abc.abstractmethod
    def lines(self) -> typing.Iterator[LineOutline]:
        """Return iterator over lines in outline."""
        raise NotImplementedError

    def remove(self, p_line: typing.Optional[LineOutline]) -> None:
        """Remove item at given line from outline.

        :param p_line: line to remove along with all descendants.  If
            line is None, remove no items.
        """
        raise NotImplementedError
        if p_line is not None:
            _ = self._ui_model.remove(p_line)

    @abc.abstractmethod
    def _set_persist(self, p_persist: PersistOutline) -> None:
        """Set outline storage element from content in persistent form.

        :param p_persist: persistent form for outline content.
        """
        raise NotImplementedError


class ModelOutlineSingle(ModelOutline[UiModelOutlineSingle, ItemOpaque],
                         typing.Generic[ItemOpaque]):
    """
    Encapsulate widget toolkit class for a single-level outline.

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
        Transient aspects of the outlines (like views) are not compared
        and may be different.
    """

    _C_ITEM = 0

    def clear(self) -> None:
        """Remove all items from outline."""
        raise NotImplementedError
        self._model.clear()

    def get_item(self, p_line: LineOutline) -> typing.Optional[ItemOpaque]:
        """Return item at given line or None when no item at line.

        :param p_line: line of desired item.
        """
        raise NotImplementedError
        return self.get_item_direct(self._model, p_line)

    @classmethod
    def get_item_direct(cls, p_model: ModelOutline, p_line: LineOutline
                        ) -> typing.Optional[ItemOpaque]:
        """Return item at given line directly from outline storage element.

        :param p_model: outline storage element.
        :param p_line: line containing desired item.
        """
        raise NotImplementedError
        return p_model.get_value(p_line, cls._C_ITEM)

    def _get_persist(self) -> PersistOutline:
        """Return outline in form suitable for persistent storage."""
        raise NotImplementedError
        persist: PersistOutline = dict()
        for line in self.lines():
            path = self._model.get_string_from_iter(line)
            item = self.get_item(line)
            persist[path] = item
        return persist

    def insert_after(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline after given line.

        If line is None, prepend item at beginning of outline.

        :param p_item: new item to add.
        :param p_line: line to precede new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError
        return self._model.insert_after(p_line, [p_item])

    def insert_before(self, p_item: ItemOpaque,
                      p_line: LineOutline = None) -> LineOutline:
        """Add item to outline before given line.

        If line is None, append item at end of outline.

        :param p_item: new item to add.
        :param p_line: line to follow new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError
        return self._model.insert_before(p_line, [p_item])

    def items(self) -> typing.Iterator[typing.Optional[ItemOpaque]]:
        """Return iterator over items in outline."""
        for line in self.lines():
            yield self.get_item(line)

    def lines(self) -> typing.Iterator[LineOutline]:
        """Return iterator over lines in outline."""
        raise NotImplementedError
        line = self._model.get_iter_first()
        while line is not None:
            yield line
            line = self._model.iter_next(line)

    def _new_model(self) -> UiModelOutlineSingle:
        """Return toolkit-specific outline storage element."""
        return UiModelOutlineSingle(GO.TYPE_PYOBJECT)

    def remove(self, p_line: typing.Optional[LineOutline]) -> None:
        """Remove item at given line from outline.

        :param p_line: line to remove along with all descendants.  If
            line is None, remove no items.
        """
        raise NotImplementedError
        if p_line is not None:
            _ = self._model.remove(p_line)

    def _set_persist(self, p_persist: PersistOutline) -> None:
        """Set outline storage element from content in persistent form.

        :param p_persist: persistent form for outline content.
        """
        raise NotImplementedError
        for path_str, item in (p_persist.items()):
            position = int(path_str)
            self._model.insert(position, [item])


class ModelOutlineMulti(ModelOutline[UiModelOutlineMulti, ItemOpaque],
                        typing.Generic[ItemOpaque]):
    """
    Encapsulate widget toolkit class for a multi-level outline.

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
        Transient aspects of the outlines (like views) are not compared
        and may be different.
    """

    def insert_after(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline after given line.

        If line is None, prepend item at beginning of outline.

        :param p_item: new item to add.
        :param p_line: line to precede new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError
        PARENT = None
        return self._model.insert_after(PARENT, p_line, [p_item])

    def insert_before(self, p_item: ItemOpaque,
                      p_line: LineOutline = None) -> LineOutline:
        """Add item to outline before given line.

        If line is None, append item at end of outline.

        :param p_item: new item to add.
        :param p_line: line to follow new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError
        PARENT = None
        return self._model.insert_before(PARENT, p_line, [p_item])

    def insert_child(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline as child of given line.

        Add line after all existing children.  If line is None, append
        item at end of outline.

        :param p_item: new item to add.
        :param p_line: line of parent of new line.
        :returns: line of newly-added item.
        """
        raise NotImplementedError
        return self._model.append(p_line, [p_item])

    def insert_section(self, p_other: 'ModelOutlineMulti',
                       p_line_parent: LineOutline = None,
                       p_line_section: LineOutline = None) -> None:
        """Insert section into outline from other outline.

        Copy section of other outline under given line after all
        existing children.  If given line is None, append section at end
        of outline.  If line in other outline is None, copy all of other
        outline.

        .. note:: The new section is a shallow copy of the other
           outline's section.

        :param p_other: outline that contains section to copy.
        :param p_line_parent: line of parent for section copy.  Default
            is top level after existing top-level items.
        :param p_line_section: line to copy along with all descendants.
            Default is to copy all lines.
        """
        raise NotImplementedError
        if p_line_section is None:
            it_to = p_line_parent
        else:
            item = p_other.get_item(p_line_section)
            it_to = self._model.append(p_line_parent, [item])
        line = p_other._model.iter_children(p_line_section)
        while line is not None:
            self.insert_section(p_other, it_to, line)
            line = p_other._model.iter_next(line)

    def items_section(self, p_line: LineOutline = None
                      ) -> typing.Iterator[typing.Optional[ItemOpaque]]:
        """Return iterator over items in section at given line.

        :param p_line: parent line of section.  Default iterates over
            entire outline.
        """
        for line in self.lines_section(p_line):
            yield self.get_item(line)

    def lines(self) -> typing.Iterator[LineOutline]:
        """Return iterator over lines in outline.

        Iteration is depth first.
        """
        return self.lines_section()

    def lines_section(self, p_line: LineOutline = None
                      ) -> typing.Iterator[LineOutline]:
        """Return iterator over lines in section at given line.

        Iteration is depth first.

        :param p_line: parent line of section.  Default iterates over
            entire outline.
        """
        raise NotImplementedError
        if p_line is not None:
            yield p_line
        line = self._model.iter_children(p_line)
        while line is not None:
            yield from self.lines_section(line)
            line = self._model.iter_next(line)

    def _new_model(self) -> UiModelOutlineMulti:
        """Return toolkit-specific outline storage element."""
        return UiModelOutlineMulti(GO.TYPE_PYOBJECT)

    def _set_persist(self, p_persist: PersistOutline) -> None:
        """Set outline storage element from content in persistent form.

        :param p_persist: persistent form for outline content.
        """
        raise NotImplementedError
        TOP_LEVEL = 1
        for path_str, item in (p_persist.items()):
            path = Gtk.TreePath(path_str)
            if TOP_LEVEL == path.get_depth():
                i_parent = None
            else:
                _ = path.up()
                i_parent = self._model.get_iter(path)
            self._model.append(i_parent, [item])


# ======================================================================
# ======================================================================
# ======================================================================
# ======================================================================
# ======================================================================

class InterfaceOutline(abc.ABC, typing.Generic[
        ItemOpaque]):
    """Specifies methods of model clases that encapsulate toolkit
    storage elements for single-level outlines.
    """

    pass


class InterfaceOutlineMulti(abc.ABC, typing.Generic[ItemOpaque]):
    """Specifies methods of model clases that encapsulate toolkit
    storage elements for multi-level outlines.
    """

    pass


# class BridgeOutlineColumnar(BridgeOutline[
#         ItemOpaque, ViewOutlineColumnar], typing.Generic[ItemOpaque]):
#     """Encapsulate widget toolkit classes for columnar view of a
#     single-level outline.
#     """
#
#     def new_view(self) -> ViewOutlineColumnar:
#         """Return toolkit-specific columnar view element."""
#         raise NotImplementedError
#         view = ViewOutlineColumnar()
#         view.set_model(self._model)
#         return view


# class BridgeOutlineSelect(BridgeOutline[
#         ItemOpaque, ViewOutlineSelect], typing.Generic[ItemOpaque]):
#     """Encapsulate widget toolkit classes for selection view of a
#     single-level outline.
#     """
#
#     def new_view(self) -> ViewOutlineSelect:
#         """Return toolkit-specific selection element."""
#         raise NotImplementedError
#         view = ViewOutlineSelect()
#         view.set_model(self._model)
#         return view


# class BridgeOutlineMultiColumnar(BridgeOutlineMulti[
#         ItemOpaque, ViewOutlineColumnar], typing.Generic[ItemOpaque]):
#     """Encapsulate widget toolkit classes for a columnal view of a
#     multi-level outline.
#     """
#
#     def new_view(self) -> ViewOutlineColumnar:
#         """Return toolkit-specific columnar element."""
#         raise NotImplementedError
#         view = ViewOutlineColumnar()
#         view.set_model(self._model)
#         return view


# class BridgeOutlineMultiSelect(BridgeOutlineMulti[
#         ItemOpaque, ViewOutlineSelect], typing.Generic[ItemOpaque]):
#     """Encapsulate widget toolkit classes for a selction view of a
#     multi-level outline.
#     """
#
#     def new_view(self) -> ViewOutlineSelect:
#         """Return toolkit-specific selection element."""
#         raise NotImplementedError
#         view = ViewOutlineSelect()
#         view.set_model(self._model)
#         return view
