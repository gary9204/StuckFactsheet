"""
Defines classes to represent a collection of views.

Factsheet uses outlines containing topics and facts.  Scenes provides
a collection to contain and display views of items in an
outline.  Scenes presents one view at a time.
"""
import gi   # type: ignore[import]
import logging
import typing

from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.view.scenes')


GenericId = typing.TypeVar('GenericId', UI.IdTopic, int)


class Scenes(typing.Generic[GenericId]):
    """Displays one scene at a time from a collection of scenes.

    A scene is a display element for an item.  You associate an item
    identifier with a scene when you add the scene to the collection.
    You use the item identifier to show or remove a scene.

    :param px_scenes: pre-defined scene collection.  If None, ``Scenes``
        creates an empty collection.

    .. attribute:: ID_NONE

    Value distinct from all item identifiers.  Used, for example, to
    indicate no item has a visible scene.

    .. attribute:: NAME_NONE

    Value distinct from all scene names.  May be used, for example, to
    identify a blank scene when no item scene is visible.
    """

    NAME_NONE = 'None'
    ID_NONE = None

    def __init__(self, px_scenes: Gtk.Stack = None) -> None:
        self._gtk_stack = px_scenes if px_scenes else Gtk.Stack()

    def add_scene(self, pm_scene: Gtk.Widget, p_id_item: GenericId) -> None:
        """Add a scene to the collection.

        Log a warning when the item already has a scene in the
        collection.

        :param pm_scene: scene to add.
        :param p_id_item: item identifier for scene.  An item may have
            at most one scene in the collection.
        """
        name = self._id_to_name(p_id_item)
        child = self._gtk_stack.get_child_by_name(name)
        if child is not None:
            logger.warning(
                'Duplicate scene of item {}: {} ({}.{})'
                ''.format(name, pm_scene, self.__class__.__name__,
                          self.add_scene.__name__))
            return

        pm_scene.show()
        self._gtk_stack.add_named(pm_scene, name)

    def get_scene_visible(self) -> typing.Optional[GenericId]:
        """Return item identifier of visible scene or ID_NONE when no
        scene is visible.
        """
        name = self._gtk_stack.get_visible_child_name()
        if name is None:
            return self.ID_NONE

        id_item = self._name_to_id(name)
        return typing.cast(GenericId, id_item)

    def _id_to_name(self, p_id: typing.Optional[GenericId]) -> str:
        """Return name corresponding to item identifier.

        :param p_id: item identifier to convert.
        """
        if p_id is self.ID_NONE:
            return self.NAME_NONE

        try:
            return hex(p_id)
        except TypeError:
            return self.NAME_NONE

    def _name_to_id(self, p_name: str) -> typing.Optional[GenericId]:
        """Return item identifier corresponding to name.

        :param p_id: name to convert.
        """
        try:
            return typing.cast(GenericId, int(p_name, base=0))
        except (TypeError, ValueError):
            return typing.cast(GenericId, self.ID_NONE)

    def remove_scene(self, p_id_item: GenericId) -> None:
        """Remove a scene from the collection.

        Log a warning when the item does not have a scene in the
        collection.

        :param p_id_item: item identifier of the scene to remove.
        """
        name = self._id_to_name(p_id_item)
        item = self._gtk_stack.get_child_by_name(name)
        if item is None:
            logger.warning(
                'Missing scene for item {} ({}.{})'.format(
                    name, self.__class__.__name__,
                    self.remove_scene.__name__))
            return

        self._gtk_stack.remove(item)

    def show_scene(self, p_id_item: typing.Optional[GenericId]
                   ) -> typing.Optional[GenericId]:
        """Attempt to show a scene and return item identifier of
        resulting visible scene.

        :param p_id_item: item identifier for scene to show to show.
        """
        name = self._id_to_name(p_id_item)
        item = self._gtk_stack.get_child_by_name(name)
        if item is not None:
            self._gtk_stack.set_visible_child(item)

        name_visible = self._gtk_stack.get_visible_child_name()
        id_visible = self._name_to_id(name_visible)
        return id_visible
