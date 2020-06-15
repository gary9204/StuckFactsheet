"""
Defines classes to represent a collection of views.

Factsheet uses outlines containing topics and facts.  Scenes provides
a collection to contain and display views of items in an
outline.  Scenes presents one view at a time.
"""
import gi   # type: ignore[import]
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.view.scenes')


class Scenes:
    """Displays a view from a collection of views.

    :param px_views: pre-defined view collection.  If None, ``Scenes``
        creates an empty collection.
    """

    def __init__(self, px_views: Gtk.Stack = None) -> None:
        self._stack = px_views if px_views else Gtk.Stack()

    def add_scene(self, pm_view: Gtk.Widget, p_id_item: int) -> None:
        """Add a view to the collection.

        Log a warning when the item already has a view in the
        collection.

        :param pm_view: view to add
        :param p_id_item: identifies item corresponding to view.  An
            item may have at most one view in the collection.
        """
        name = str(hex(p_id_item))
        child = self._stack.get_child_by_name(name)
        if child is not None:
            logger.warning(
                'Duplicate view of item {}: {} ({}.{})'
                ''.format(name, pm_view, self.__class__.__name__,
                          self.add_scene.__name__))
            return

        pm_view.show()
        self._stack.add_named(pm_view, name)

    def remove_scene(self, p_id_item: int):
        """Remove a view from the collection.

        Log a warning when the item does not have a view in the
        collection.

        :param p_id_item: identifies item corresponding to view to
            remove.
        """
        name = str(hex(p_id_item))
        item = self._stack.get_child_by_name(name)
        if item is None:
            logger.warning(
                'Missing view for item {} ({}.{})'.format(
                    name, self.__class__.__name__,
                    self.remove_scene.__name__))
            return

        self._stack.remove(item)

    def show_scene(self, p_id_item: int):
        """Make a view visible.

        Log a warning when the item does not have a view in the
        collection.

        :param p_id_item: identifies the item corrseponding to the view
            to show.
        """
        name = str(hex(p_id_item))
        item = self._stack.get_child_by_name(name)
        if item is None:
            logger.warning(
                'Missing view for item {} ({}.{})'.format(
                    name, self.__class__.__name__, self.show_scene.__name__))
            return

        self._stack.set_visible_child(item)
