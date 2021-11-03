"""
Defines bridge classes to encapsulate widget toolkit outline classes.

An outline is an ordered list analogous to a bulleted list in a print
document.  An outline contains lines, each of which identifies an item.
Lines and items are analogous to bullets and text in a bulleted list.
Like a bulleted list, an outline may be either single-level or multi-
level.

Constants and Type Hints
========================

.. data:: ChooserOutline

    Type hint for GTK element to view an outline and choose a line.
    See `Gtk.ComboBox`_.

.. _`Gtk.ComboBox`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ComboBox.html

.. data:: ItemOpaque

    Placeholder type hint for an item at a line.

.. data:: LineOutline

    Type hint for GTK element to store a line.  See `Gtk.Treeiter`_.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html

.. data:: PersistOutline

    Type hint for outline representation suitable for persistent
    storage.

.. data:: UiModelOutlineMulti

    Type hint for GTK element to store a multi-level outline.  See
    `Gtk.TreeStore`_.

.. _`Gtk.TreeStore`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeStore.html

.. data:: UIModelOutlineSingle

    Type hint for GTK element to store a single-level outline.  See
    `Gtk.ListStore`_ .

.. _`Gtk.ListStore`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ListStore.html

.. data:: ViewOutline

    Type hint for GTK element to view an outline in columnar format.
    See `Gtk.TreeView`_.

.. _`Gtk.TreeView`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeView.html

Classes and Functions
=====================
    """
import abc
import gi   # type: ignore[import]
import typing

from . import bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


ChooserOutline = typing.Union[Gtk.ComboBox]
ItemOpaque = typing.TypeVar('ItemOpaque')
LineOutline = typing.Union[Gtk.TreeIter]
PersistOutline = typing.MutableMapping[str, ItemOpaque]
UiModelOutlineMulti = typing.Union[Gtk.TreeStore]
UiModelOutlineSingle = typing.Union[Gtk.ListStore]
UiModelOutline = typing.TypeVar(
    'UiModelOutline', UiModelOutlineMulti, UiModelOutlineSingle)
ViewOutline = typing.Union[Gtk.TreeView]


class FactoryChooserOutline(BBASE.FactoryUiViewAbstract[UiModelOutline],
                            typing.Generic[UiModelOutline, ItemOpaque]):
    """Chooser factory for an outline.

    A call to the factory takes no arguments and returns
    :data:`.ChooserOutline`.
    """

    def __init__(self, p_model_outline:
                 'ModelOutline[UiModelOutline, ItemOpaque]') -> None:
        """Initialize outline for choosers.

        :param p_model_outline: outline model.
        """
        self._ui_model = p_model_outline.ui_model

    def __call__(self) -> ChooserOutline:
        """Return chooser for outline."""
        chooser = Gtk.ComboBox(model=self._ui_model)
        return chooser


class FactoryViewOutline(BBASE.FactoryUiViewAbstract[UiModelOutline],
                         typing.Generic[UiModelOutline, ItemOpaque]):
    """View factory for an outline.

    A call to the factory takes no arguments and returns :data:`.ViewOutline`.
    """

    def __init__(self, p_model_outline:
                 'ModelOutline[UiModelOutline, ItemOpaque]') -> None:
        """Initialize outline for views.

        :param p_model_outline: outline model.
        """
        self._ui_model = p_model_outline.ui_model

    def __call__(self) -> ViewOutline:
        """Return view for outline."""
        chooser = Gtk.TreeView(model=self._ui_model)
        return chooser


class ModelOutline(BBASE.BridgeBase[UiModelOutline, PersistOutline],
                   typing.Generic[UiModelOutline, ItemOpaque]):
    """Common ancestor of bridge classes for outlines.

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
    """

    _C_ITEM = 0

    def clear(self) -> None:
        """Remove all items from outline."""
        self._ui_model.clear()

    def get_item(self, p_line: LineOutline) -> typing.Optional[ItemOpaque]:
        """Return item at given line or None when no item at line.

        :param p_line: line of desired item.
        """
        return self.get_item_direct(self._ui_model, p_line)

    @classmethod
    def get_item_direct(cls, p_model: UiModelOutline, p_line: LineOutline
                        ) -> typing.Optional[ItemOpaque]:
        """Return item at given line directly from outline storage element.

        :param p_model: outline storage element.
        :param p_line: line containing desired item.
        """
        return p_model.get_value(p_line, cls._C_ITEM)

    def _get_persist(self) -> PersistOutline:
        """Return outline in form suitable for persistent storage."""
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
    """

    def insert_after(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline after given line.

        If line is None, prepend item at beginning of outline.

        :param p_item: new item to add.
        :param p_line: line to precede new line.
        :returns: line of newly-added item.
        """
        return self._ui_model.insert_after(p_line, [p_item])

    def insert_before(self, p_item: ItemOpaque,
                      p_line: LineOutline = None) -> LineOutline:
        """Add item to outline before given line.

        If line is None, append item at end of outline.

        :param p_item: new item to add.
        :param p_line: line to follow new line.
        :returns: line of newly-added item.
        """
        return self._ui_model.insert_before(p_line, [p_item])

    def lines(self) -> typing.Iterator[LineOutline]:
        """Return iterator over lines in outline."""
        line = self._ui_model.get_iter_first()
        while line is not None:
            yield line
            line = self._ui_model.iter_next(line)

    def _new_ui_model(self) -> UiModelOutlineSingle:
        """Return toolkit-specific outline storage element."""
        return UiModelOutlineSingle(GO.TYPE_PYOBJECT)

    def _set_persist(self, p_persist: PersistOutline) -> None:
        """Set outline storage element from content in persistent form.

        :param p_persist: persistent form for outline content.
        """
        for path_str, item in (p_persist.items()):
            position = int(path_str)
            self._ui_model.insert(position, [item])


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
        PARENT = None
        return self._ui_model.insert_after(PARENT, p_line, [p_item])

    def insert_before(self, p_item: ItemOpaque,
                      p_line: LineOutline = None) -> LineOutline:
        """Add item to outline before given line.

        If line is None, append item at end of outline.

        :param p_item: new item to add.
        :param p_line: line to follow new line.
        :returns: line of newly-added item.
        """
        PARENT = None
        return self._ui_model.insert_before(PARENT, p_line, [p_item])

    def insert_child(self, p_item: ItemOpaque,
                     p_line: LineOutline = None) -> LineOutline:
        """Add item to outline as child of given line.

        Add line after all existing children.  If line is None, append
        item at end of outline.

        :param p_item: new item to add.
        :param p_line: line of parent of new line.
        :returns: line of newly-added item.
        """
        return self._ui_model.append(p_line, [p_item])

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
        if p_line_section is None:
            it_to = p_line_parent
        else:
            item = p_other.get_item(p_line_section)
            it_to = self._ui_model.append(p_line_parent, [item])
        line = p_other._ui_model.iter_children(p_line_section)
        while line is not None:
            self.insert_section(p_other, it_to, line)
            line = p_other._ui_model.iter_next(line)

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
        if p_line is not None:
            yield p_line
        line = self._ui_model.iter_children(p_line)
        while line is not None:
            yield from self.lines_section(line)
            line = self._ui_model.iter_next(line)

    def _new_ui_model(self) -> UiModelOutlineMulti:
        """Return toolkit-specific outline storage element."""
        return UiModelOutlineMulti(GO.TYPE_PYOBJECT)

    def _set_persist(self, p_persist: PersistOutline) -> None:
        """Set outline storage element from content in persistent form.

        :param p_persist: persistent form for outline content.
        """
        TOP_LEVEL = 1
        for path_str, item in (p_persist.items()):
            path = Gtk.TreePath(path_str)
            if TOP_LEVEL == path.get_depth():
                i_parent = None
            else:
                _ = path.up()
                i_parent = self._ui_model.get_iter(path)
            self._ui_model.append(i_parent, [item])
