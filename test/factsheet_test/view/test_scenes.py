"""
Unit tests for class for collection of presentations.
See :mod:`.scenes`.
"""
import logging

from factsheet.view import scenes as VSCENES

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestScenes:
    """Unit tests for :class:`Scenes`."""

    def test_init(self):
        """| Confirm initialization.
        | Case: pre-defined collection.
        """
        # Setup
        STACK = Gtk.Stack()
        # Test
        target = VSCENES.Scenes(STACK)
        assert isinstance(target._stack, Gtk.Stack)
        assert target._stack is STACK

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default collection.
        """
        # Setup
        N_EMPTY = 0
        # Test
        target = VSCENES.Scenes()
        assert isinstance(target._stack, Gtk.Stack)
        assert N_EMPTY == len(target._stack)

    def test_add_scene(self):
        """| Confirm view added to collection.
        | Case: view not in collection.
        """
        # Setup
        VIEW = Gtk.Label(label='Parrot')
        VIEW.hide()
        ID_ITEM = 42
        NAME = str(hex(ID_ITEM))
        target = VSCENES.Scenes()
        # Test
        target.add_scene(VIEW, ID_ITEM)
        child = target._stack.get_child_by_name(NAME)
        assert child is VIEW
        assert child.get_visible()

    def test_add_scene_present(self, PatchLogger, monkeypatch):
        """| Confirm view added to collection.
        | Case: view in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_PRESENT = 1
        name_dup = str(hex(ID_PRESENT))
        view_dup = scenes[ID_PRESENT]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view of item {}: {} (Scenes.add_scene)'
            ''.format(name_dup, view_dup))

        class PatchAddNamed:
            def __init__(self): self.called = False

            def add_named(self, _v, _n): self.called = True

        patch_add = PatchAddNamed()
        monkeypatch.setattr(
            Gtk.Stack, 'add_named', patch_add.add_named)
        # Test
        target.add_scene(view_dup, ID_PRESENT)
        assert len(scenes) == len(target._stack)
        assert not patch_add.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_remove_scene(self):
        """| Confirm view removed from collection.
        | Case: view in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_REMOVE = 1
        _ = scenes.pop(ID_REMOVE)
        # Test
        target.remove_scene(ID_REMOVE)
        assert len(scenes) == len(target._stack)
        for key, item in scenes.items():
            name = str(hex(key))
            assert item is target._stack.get_child_by_name(name)

    def test_remove_scene_absent(self, PatchLogger, monkeypatch):
        """| Confirm scene removed from collection.
        | Case: view not in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)

        ID_ABSENT = 1
        name_absent = str(hex(ID_ABSENT))
        _ = scenes.pop(ID_ABSENT)
        target.remove_scene(ID_ABSENT)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view for item {} (Scenes.remove_scene)'
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
        assert len(scenes) == len(target._stack)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_show_scene(self):
        """| Confirm scene selection.
        | Case: scene in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)
        ID_VISIBLE = 0
        target._stack.set_visible_child(scenes[ID_VISIBLE])
        ID_SHOW = 2
        # Test
        target.show_scene(ID_SHOW)
        assert target._stack.get_visible_child() is scenes[ID_SHOW]

    def test_show_scene_absent(self, PatchLogger, monkeypatch):
        """| Confirm scene selection.
        | Case: scene nto in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], i)
        I_VISIBLE = 0
        target._stack.set_visible_child(scenes[I_VISIBLE])
        I_ABSENT = -1
        name_absent = str(hex(I_ABSENT))

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view for item {} (Scenes.show_scene)'
            ''.format(name_absent))

        class PatchShow:
            def __init__(self): self.called = False

            def set_visible_child(self, _n): self.called = True

        patch_show = PatchShow()
        monkeypatch.setattr(
            Gtk.Stack, 'set_visible_child', patch_show.set_visible_child)
        # Test
        target.show_scene(I_ABSENT)
        assert not patch_show.called
        assert len(scenes) == len(target._stack)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message
