"""
Defines classes to represent a collection of views.

Factsheet uses outlines containing topics and facts.  ViewStack provides
a collection to contain and display views of items in an
outline.  ViewStack presents one view at a time.
"""
import gi   # type: ignore[import]
import logging
import typing

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.VSTACK')

NameView = str
UiViewStack = typing.Union[Gtk.Stack]
ViewItem = typing.Union[Gtk.Widget]


class ViewStack:
    """Displays view at a time from a collection of views.

    Each view is a presentation element for an item (such as a topic,
    fact, or fact value).  Each item view is identified by a name.
    Methods use view name to add, show, pin, or remove the item view.
    The class supports pinning names. When a name is pinned, the
    corresponding view cannot be removed.
    """

    def __init__(self) -> None:
        """Initilize collection of item views."""
        self._ui_view = Gtk.Stack()
        self._pinned: typing.MutableSequence[NameView] = list()

    def add_view(self, p_view: ViewItem, p_name: NameView) -> None:
        """Add an item view with the given name to the collection.

        When the collection contains a view with the given name,  log a
        warning and do not change the collection.

        :param p_view: item view to add.
        :param p_name: name of view.  A name may appear at most once in
            the collection.
        """
        child = self._ui_view.get_child_by_name(p_name)
        if child is not None:
            logger.warning(
                'Duplicate view \'{}\' for name {} ({}.{})'
                ''.format(p_view, p_name, type(self).__name__,
                          self.add_view.__name__))
            return

        self._ui_view.add_named(p_view, p_name)
        p_view.show()

    def clear(self) -> None:
        """Remove all unpinned item views from collection."""
        for view in self._ui_view:
            name = self._ui_view.child_get_property(view, 'name')
            self.remove_view(name)

    def __contains__(self, p_name: typing.Any) -> bool:
        """Return True when collection contains item view with given name."""
        if not isinstance(p_name, str):
            return False

        child = self._ui_view.get_child_by_name(p_name)
        if child is None:
            return False

        return True

    def get_name_visible(self) -> typing.Optional[NameView]:
        """Return name of visible item view or None when no view is visible."""
        return self._ui_view.get_visible_child_name()

    def pin_view(self, p_name: NameView) -> None:
        """Pin an item view name so that the view cannot be removed.

        When the name does correspond to an item view in the collection
        or when the named view is pinned, log a warning.

        :param p_name: name of the item view to pin.
        """
        view = self._ui_view.get_child_by_name(p_name)
        if view is None:
            logger.warning('No view named \'{}\' ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.pin_view.__name__))
            return

        if p_name in self._pinned:
            logger.warning('View named \'{}\' already pinned ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.pin_view.__name__))
            return

        self._pinned.append(p_name)

    def remove_view(self, p_name: NameView) -> None:
        """Remove an item view from the collection.

        Log a warning when the name does correspond to an item view in
        the collection or when the named view is pinned..

        :param p_name: name of the item view to remove.
        """
        if p_name in self._pinned:
            logger.warning('Pinned item view named \'{}\' cannot be removed '
                           '({}.{})'.format(p_name, type(self).__name__,
                                            self.remove_view.__name__))
            return

        view_item = self._ui_view.get_child_by_name(p_name)
        if view_item is None:
            logger.warning('No item view named \'{}\' ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.remove_view.__name__))
            return

        self._ui_view.remove(view_item)

    def show_view(self, p_name: NameView) -> typing.Optional[NameView]:
        """Attempt to show an item view and return name of visible view.

        Log a warning when no item view has given name.

        :param p_name: name of item view to show.
        """
        item = self._ui_view.get_child_by_name(p_name)
        if item is not None:
            self._ui_view.set_visible_child(item)
        else:
            logger.warning('No item view named \'{}\' ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.show_view.__name__))
        name_visible = self._ui_view.get_visible_child_name()
        return name_visible

    @property
    def ui_view(self) -> UiViewStack:
        """Return user interface element of stack."""
        return self._ui_view

    def unpin_view(self, p_name: NameView) -> None:
        """Unpin an item view so that it can be removed.

        Log a warning when the named view is not pinned..

        :param p_name: name of the item view to unpin.
        """
        try:
            self._pinned.remove(p_name)
        except ValueError:
            logger.warning('View named \'{}\' not pinned ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.unpin_view.__name__))
