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
ViewItem = typing.Union[Gtk.Widget]


class ViewStack:
    """Displays view at a time from a collection of views.

    Each view is a presentation element for an item (such as a topic,
    fact, or fact value).  Each view is identified by a name,
    which methods use to show or remove the view.  The class supports
    pinning names so that the corresponding views cannot be replaced
    or removed.
    """

    def __init__(self) -> None:
        """Initilize collection of item views.

        :param p_views: pre-defined collection of item views.  If None,
            :class:`.ViewStack` creates an empty collection.
        """
        self._ui_stack = Gtk.Stack()
        self._pinned: typing.MutableSequence[NameView] = list()

    def add_view_item(self, p_view: ViewItem, p_name: NameView) -> None:
        """Add an item view to the collection.

        Do not change the collection and log a warning when the
        collection contains a view with the given name.

        :param p_view: item view to add.
        :param p_name: name of view.  A name may appear at most once in
            the collection.
        """
        child = self._ui_stack.get_child_by_name(p_name)
        if child is not None:
            logger.warning(
                'Duplicate name \'{}\' with view {} ({}.{})'
                ''.format(p_name, p_view, type(self).__name__,
                          self.add_view_item.__name__))
            return

        self._ui_stack.add_named(p_view, p_name)
        p_view.show()

    def clear(self) -> None:
        """Remove all item views from collection."""
        print('Enter: clear')
        # for view in self._ui_stack:
        #     self._ui_stack.remove(view)

    def get_name_visible(self) -> typing.Optional[NameView]:
        """Return name of visible item view or None when no view is visible."""
        print('Enter: get_name_visible')
        # return self._ui_stack.get_visible_child_name()

    def pin_view_item(self, p_name: NameView) -> None:
        """Pin an item view so that it cannot be replaced or removed.

        Log a warning when the name does correspond to an item view in
        the collection or when the named view is pinned..

        :param p_name: name of the item view to pin.
        """
        view = self._ui_stack.get_child_by_name(p_name)
        if view is None:
            logger.warning('No view named \'{}\' ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.pin_view_item.__name__))
            return

        if p_name in self._pinned:
            logger.warning('View named \'{}\' already pinned ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.pin_view_item.__name__))
            return

        self._pinned.append(p_name)

    def remove_view_item(self, p_name: NameView) -> None:
        """Remove an item view from the collection.

        Log a warning when the name does correspond to an item view in
        the collection or when the named view is pinned..

        :param p_name: name of the item view to remove.
        """
        if p_name in self._pinned:
            logger.warning('Pinned item view named \'{}\' cannot be removed '
                           '({}.{})'.format(p_name, type(self).__name__,
                                            self.remove_view_item.__name__))
            return

        view_item = self._ui_stack.get_child_by_name(p_name)
        if view_item is None:
            logger.warning('No item view named \'{}\' ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.remove_view_item.__name__))
            return

        self._ui_stack.remove(view_item)

    def show_view_item(self, p_name: NameView) -> typing.Optional[NameView]:
        """Attempt to show an item view and return item name of
        resulting visible view.

        :param p_name: name of item view to show to show.
        """
        print('Enter: show_view_item')
        # name = p_name if p_name else self._name_fixed
        # if name is not None:
        #     item = self._ui_stack.get_child_by_name(name)
        #     if item is not None:
        #         self._ui_stack.set_visible_child(item)

        # name_visible = self._ui_stack.get_visible_child_name()
        # return name_visible

    def unpin_view_item(self, p_name: NameView) -> None:
        """Unpin an item view so that it can be replaced or removed.

        Log a warning when the named view is not pinned..

        :param p_name: name of the item view to unpin.
        """
        try:
            self._pinned.remove(p_name)
        except ValueError:
            logger.warning('View named \'{}\' not pinned ({}.{})'
                           ''.format(p_name, type(self).__name__,
                                     self.unpin_view_item.__name__))
