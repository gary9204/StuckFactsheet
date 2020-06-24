"""
Unit tests for class for collection of presentations.
See :mod:`.scenes`.
"""
import logging
import pytest   # type: ignore[import]

from factsheet.view import scenes as VSCENES
from factsheet.view import ui as UI

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestScenes:
    """Unit tests for :class:`Scenes`."""

    def test_constants(self):
        """Confirm class constants defined."""
        # Setup
        target = VSCENES.Scenes[UI.IdTopic]
        # Test
        assert hasattr(target, 'NAME_NONE')
        assert hasattr(target, 'ID_NONE')

    def test_init(self):
        """| Confirm initialization.
        | Case: pre-defined collection.
        """
        # Setup
        STACK = Gtk.Stack()
        # Test
        target = VSCENES.Scenes[UI.IdTopic](STACK)
        assert isinstance(target._gtk_stack, Gtk.Stack)
        assert target._gtk_stack is STACK

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default collection.
        """
        # Setup
        N_EMPTY = 0
        # Test
        target = VSCENES.Scenes[UI.IdTopic]()
        assert isinstance(target._gtk_stack, Gtk.Stack)
        assert N_EMPTY == len(target._gtk_stack)

    def test_add_scene(self):
        """| Confirm view added to collection.
        | Case: view not in collection.
        """
        # Setup
        VIEW = Gtk.Label(label='Parrot')
        VIEW.hide()
        ID_ITEM = UI.IdTopic(42)
        target = VSCENES.Scenes[UI.IdTopic]()
        NAME = target._id_to_name(ID_ITEM)
        # Test
        target.add_scene(VIEW, ID_ITEM)
        child = target._gtk_stack.get_child_by_name(NAME)
        assert child is VIEW
        assert child.get_visible()

    def test_add_scene_present(self, PatchLogger, monkeypatch):
        """| Confirm view added to collection.
        | Case: view in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_PRESENT = 1
        name_dup = target._id_to_name(ID_PRESENT)
        view_dup = scenes[ID_PRESENT]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate scene of item {}: {} (Scenes.add_scene)'
            ''.format(name_dup, view_dup))

        class PatchAddNamed:
            def __init__(self): self.called = False

            def add_named(self, _v, _n): self.called = True

        patch_add = PatchAddNamed()
        monkeypatch.setattr(
            Gtk.Stack, 'add_named', patch_add.add_named)
        # Test
        target.add_scene(view_dup, ID_PRESENT)
        assert len(scenes) == len(target._gtk_stack)
        assert not patch_add.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_get_scene_visible(self):
        """| Confirm return of visible scene.
        | Case: a scene is visible.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_VISIBLE = UI.IdTopic(1)
        scene_visible = scenes[ID_VISIBLE]
        target._gtk_stack.set_visible_child(scene_visible)

        # Test
        assert ID_VISIBLE == target.get_scene_visible()

    def test_get_scene_visible_none(self):
        """| Confirm return of visible scene.
        | Case: no scene is visible.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)
            scenes[i].hide()
        # Test
        assert target.get_scene_visible() is target.ID_NONE

    @pytest.mark.parametrize('ID, NAME', [
        (42, '0x2a'),
        (None, VSCENES.Scenes[UI.IdTopic].NAME_NONE)
        ])
    def test_id_to_name(self, ID, NAME):
        """Confirm translation.
        | Case: ID is item identifier.
        """
        # Setup
        target = VSCENES.Scenes[UI.IdTopic]()
        # Test
        assert NAME == target._id_to_name(ID)

    @pytest.mark.parametrize('NAME, ID', [
        ('0x2a', 42),
        (VSCENES.Scenes[UI.IdTopic].NAME_NONE, None),
        (dict(), None),
        ])
    def test_name_to_id(self, NAME, ID):
        """Confirm translation."""
        # Setup
        target = VSCENES.Scenes[UI.IdTopic]()
        # Test
        assert ID == target._name_to_id(NAME)

    def test_remove_scene(self):
        """| Confirm view removed from collection.
        | Case: view in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_REMOVE = 1
        _ = scenes.pop(ID_REMOVE)
        # Test
        target.remove_scene(ID_REMOVE)
        assert len(scenes) == len(target._gtk_stack)
        for key, item in scenes.items():
            name = target._id_to_name(key)
            assert item is target._gtk_stack.get_child_by_name(name)

    def test_remove_scene_absent(self, PatchLogger, monkeypatch):
        """| Confirm scene removed from collection.
        | Case: view not in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_ABSENT = 1
        name_absent = target._id_to_name(ID_ABSENT)
        _ = scenes.pop(ID_ABSENT)
        target.remove_scene(ID_ABSENT)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing scene for item {} (Scenes.remove_scene)'
            ''.format(name_absent))

        class PatchRemove:
            def __init__(self): self.called = False

            def remove(self, _n): self.called = True

        patch_remove = PatchRemove()
        monkeypatch.setattr(
            Gtk.Stack, 'remove', patch_remove.remove)
        # Test
        target.remove_scene(ID_ABSENT)
        assert not patch_remove.called
        assert len(scenes) == len(target._gtk_stack)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_show_scene(self):
        """| Confirm scene selection.
        | Case: scene in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes[UI.IdTopic]()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)
        ID_VISIBLE = 0
        target._gtk_stack.set_visible_child(scenes[ID_VISIBLE])
        ID_SHOW = 2
        # Test
        id_shown = target.show_scene(ID_SHOW)
        assert ID_SHOW == id_shown
        assert target._gtk_stack.get_visible_child() is scenes[ID_SHOW]
