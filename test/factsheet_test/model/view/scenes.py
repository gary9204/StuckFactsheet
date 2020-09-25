"""
Defines classes to represent a collection of views.

Factsheet uses outlines containing topics and facts.  Scenes provides
a collection to contain and display views of items in an
outline.  Scenes presents one view at a time.
"""
import gi   # type: ignore[import]
import logging
import typing

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.view.scenes')


class Scenes:
    """Displays one scene at a time from a collection of scenes.

    A scene is a presentation element for an item (such as a topic form,
    fact block, or fact aspect).  Each scene is identified by a name,
    which methods use to show or remove the scene.  The class supports
    fixing one name so that the corresponding scene cannot be replaced
    or removed.

    :param p_scenes: pre-defined scene collection.  If None, ``Scenes``
        creates an empty collection.
    :param p_name_fixed: name of a scene that cannot be replaced or
        removed.
    :param p_scene_fixed: scene that cannot be replaced or removed.
    """

    def __init__(self, p_scenes: Gtk.Stack = None, p_name_fixed: str = None,
                 p_scene_fixed: Gtk.Widget = None) -> None:
        self._stack_gtk = p_scenes if p_scenes else Gtk.Stack()
        self._name_fixed = p_name_fixed
        if self._name_fixed is not None and p_scene_fixed is not None:
            self.add_scene(p_scene_fixed, self._name_fixed)

    def add_scene(self, p_scene: Gtk.Widget, p_name: str) -> None:
        """Add a scene to the collection.

        Do not change the collection and log a warning when the
        collection contains a scene with the given name.

        :param p_scene: scene to add.
        :param p_name: name of scene.  An item may have
            at most one scene in the collection.
        """
        child = self._stack_gtk.get_child_by_name(p_name)
        if child is not None:
            logger.warning(
                'Duplicate name \'{}\' with scene {} ({}.{})'
                ''.format(p_name, p_scene, self.__class__.__name__,
                          self.add_scene.__name__))
            return

        p_scene.show()
        self._stack_gtk.add_named(p_scene, p_name)

    def clear(self) -> None:
        """Remove all scenes from collection."""
        # for scene in self._stack_gtk.get_children():
        for scene in self._stack_gtk:
            self._stack_gtk.remove(scene)

    def get_scene_visible(self) -> typing.Optional[str]:
        """Return name of visible scene or None when no scene is visible."""
        return self._stack_gtk.get_visible_child_name()

    def remove_scene(self, p_name: str) -> None:
        """Remove a scene from the collection.

        Log a warning when the item does not have a scene in the
        collection.

        :param p_name: name of the scene to remove.
        """
        if p_name == self._name_fixed:
            logger.warning(
                'Fixed scene \'{}\' cannot be removed. ({}.{})'.format(
                    p_name, self.__class__.__name__,
                    self.remove_scene.__name__))
            return

        item = self._stack_gtk.get_child_by_name(p_name)
        if item is None:
            logger.warning(
                'Missing scene named \'{}\' ({}.{})'.format(
                    p_name, self.__class__.__name__,
                    self.remove_scene.__name__))
            return

        self._stack_gtk.remove(item)

    def show_scene(self, p_name: typing.Optional[str]
                   ) -> typing.Optional[str]:
        """Attempt to show a scene and return item name of resulting
        visible scene.

        :param p_name: name of scene to show to show.
        """
        name = p_name if p_name else self._name_fixed
        if name is not None:
            item = self._stack_gtk.get_child_by_name(name)
            if item is not None:
                self._stack_gtk.set_visible_child(item)

        name_visible = self._stack_gtk.get_visible_child_name()
        return name_visible
