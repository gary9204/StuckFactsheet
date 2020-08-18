"""
Unit tests for class for collection of presentations.
See :mod:`.scenes`.
"""
import logging

from factsheet.view import scenes as VSCENES
from factsheet.view import ui as UI

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
        assert isinstance(target._stack_gtk, Gtk.Stack)
        assert target._stack_gtk is STACK

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default collection.
        """
        # Setup
        N_EMPTY = 0
        # Test
        target = VSCENES.Scenes()
        assert isinstance(target._stack_gtk, Gtk.Stack)
        assert N_EMPTY == len(target._stack_gtk)

    def test_init_fixed_name(self):
        """| Confirm initialization.
        | Case: default collection with fixed name.
        """
        # Setup
        NAME = 'Parrot'
        # Test
        target = VSCENES.Scenes(p_name_fixed=NAME)
        assert isinstance(target._stack_gtk, Gtk.Stack)
        assert NAME == target._name_fixed
        scene_fixed = target._stack_gtk.get_child_by_name(target._name_fixed)
        assert scene_fixed is None

    def test_init_fixed_scene(self):
        """| Confirm initialization.
        | Case: default collection with fixed name and scene.
        """
        # Setup
        NAME = 'Parrot'
        SCENE = Gtk.Label(label=NAME)
        # Test
        target = VSCENES.Scenes(p_name_fixed=NAME, p_scene_fixed=SCENE)
        assert isinstance(target._stack_gtk, Gtk.Stack)
        assert NAME == target._name_fixed
        scene_fixed = target._stack_gtk.get_child_by_name(target._name_fixed)
        assert scene_fixed is SCENE

    def test_add_scene(self):
        """| Confirm view added to collection.
        | Case: view not in collection.
        """
        # Setup
        NAME = 'Parrot'
        VIEW = Gtk.Label(label=NAME)
        VIEW.hide()
        target = VSCENES.Scenes()
        # Test
        target.add_scene(VIEW, NAME)
        child = target._stack_gtk.get_child_by_name(NAME)
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
            target.add_scene(scenes[i], hex(i))

        ID_PRESENT = 1
        name_dup = hex(ID_PRESENT)
        view_dup = scenes[ID_PRESENT]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate name \'{}\' with scene {} (Scenes.add_scene)'
            ''.format(name_dup, view_dup))

        class PatchAddNamed:
            def __init__(self): self.called = False

            def add_named(self, _v, _n): self.called = True

        patch_add = PatchAddNamed()
        monkeypatch.setattr(
            Gtk.Stack, 'add_named', patch_add.add_named)
        # Test
        target.add_scene(view_dup, name_dup)
        assert len(scenes) == len(target._stack_gtk)
        assert not patch_add.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_clear(self):
        """Confirm collection empty."""
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))
        # Test
        target.clear()
        assert not len(target._stack_gtk)

    def test_get_scene_visible(self):
        """| Confirm return of visible scene.
        | Case: a scene is visible.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))

        ID_VISIBLE = UI.IdTopic(1)
        name_visible = hex(ID_VISIBLE)
        scene_visible = scenes[ID_VISIBLE]
        target._stack_gtk.set_visible_child(scene_visible)

        # Test
        assert name_visible == target.get_scene_visible()

    def test_get_scene_visible_none(self):
        """| Confirm return of visible scene.
        | Case: no scene is visible.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))
            scenes[i].hide()
        # Test
        assert target.get_scene_visible() is None

    def test_remove_scene(self):
        """| Confirm view removed from collection.
        | Case: scene in collection and not fixed.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))

        ID_REMOVE = 1
        _ = scenes.pop(ID_REMOVE)
        name_remove = hex(ID_REMOVE)
        # Test
        target.remove_scene(name_remove)
        assert len(scenes) == len(target._stack_gtk)
        for key, scene in scenes.items():
            assert scene is target._stack_gtk.get_child_by_name(hex(key))

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
            target.add_scene(scenes[i], hex(i))

        ID_ABSENT = 1
        _ = scenes.pop(ID_ABSENT)
        name_absent = hex(ID_ABSENT)
        target.remove_scene(name_absent)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing scene named \'{}\' (Scenes.remove_scene)'
            ''.format(name_absent))

        class PatchRemove:
            def __init__(self): self.called = False

            def remove(self, _n): self.called = True

        patch_remove = PatchRemove()
        monkeypatch.setattr(
            Gtk.Stack, 'remove', patch_remove.remove)
        # Test
        target.remove_scene(name_absent)
        assert not patch_remove.called
        assert len(scenes) == len(target._stack_gtk)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_remove_scene_fixed(self, PatchLogger, monkeypatch):
        """| Confirm scene removed from collection.
        | Case: fixed scene in collection.
        """
        # Setup
        NAME = 'Parrot'
        SCENE = Gtk.Label(label=NAME)
        target = VSCENES.Scenes(p_name_fixed=NAME, p_scene_fixed=SCENE)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Fixed scene \'{}\' cannot be removed. (Scenes.remove_scene)'
            ''.format(NAME))

        class PatchRemove:
            def __init__(self): self.called = False

            def remove(self, _n): self.called = True

        patch_remove = PatchRemove()
        monkeypatch.setattr(
            Gtk.Stack, 'remove', patch_remove.remove)
        # Test
        target.remove_scene(NAME)
        assert not patch_remove.called
        assert target._stack_gtk.get_child_by_name(NAME) is SCENE
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
            target.add_scene(scenes[i], hex(i))
        ID_VISIBLE = 0
        target._stack_gtk.set_visible_child(scenes[ID_VISIBLE])
        ID_SHOW = 2
        name_show = hex(ID_SHOW)
        # Test
        name_shown = target.show_scene(name_show)
        assert name_show == name_shown
        assert target._stack_gtk.get_visible_child() is scenes[ID_SHOW]

    def test_show_scene_absent(self):
        """| Confirm scene selection.
        | Case: scene not in collection.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))
        ID_VISIBLE = 0
        name_visible = hex(ID_VISIBLE)
        target._stack_gtk.set_visible_child_name(name_visible)
        name_show = 'Something completely different'
        # Test
        name_shown = target.show_scene(name_show)
        assert name_visible == name_shown
        assert target._stack_gtk.get_visible_child() is scenes[ID_VISIBLE]

    def test_show_scene_none(self):
        """| Confirm scene selection.
        | Case: no name without fixed scene.
        """
        # Setup
        N_SCENES = 3
        target = VSCENES.Scenes()
        scenes = dict()
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))
        ID_VISIBLE = 0
        name_visible = hex(ID_VISIBLE)
        target._stack_gtk.set_visible_child_name(name_visible)
        # Test
        name_shown = target.show_scene(None)
        assert name_visible == name_shown
        assert target._stack_gtk.get_visible_child() is scenes[ID_VISIBLE]

    def test_show_scene_none_fixed(self):
        """| Confirm scene selection.
        | Case: no name with fixed scene.
        """
        # Setup
        NAME = 'Parrot'
        SCENE = Gtk.Label(label=NAME)
        target = VSCENES.Scenes(p_name_fixed=NAME, p_scene_fixed=SCENE)
        scenes = dict()
        N_SCENES = 3
        for i in range(N_SCENES):
            scenes[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_scene(scenes[i], hex(i))
        ID_VISIBLE = 0
        name_visible = hex(ID_VISIBLE)
        target._stack_gtk.set_visible_child_name(name_visible)
        # Test
        name_shown = target.show_scene(None)
        assert NAME == name_shown
        assert target._stack_gtk.get_visible_child() is SCENE
