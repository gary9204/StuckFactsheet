"""
Defines unit tests for classes for displaying fact values.
See :mod:`.scene_value`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.view import scene_value as VVALUE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestSceneEvaluate:
    """Unit tests for :class:`.SceneEvaluate`."""

    @pytest.mark.skip(reason='Deferred until complete Face implementation.')
    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        pass


class TestSceneSynopsis:
    """Unit tests for :class:`.SceneSynopsis`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneSynopsis()
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        assert isinstance(target._label_gtk, Gtk.Label)
        viewport = target._scene_gtk.get_child()
        assert target._label_gtk is viewport.get_child()


class TestSceneTableau:
    """Unit tests for :class:`.SceneTableau`.
    """

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneTableau()
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        assert isinstance(target._treeview_gtk, Gtk.TreeView)
        assert target._scene_gtk.get_child() is target._treeview_gtk


class TestSceneText:
    """Unit tests for :class:`.SceneText`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneText()
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        assert isinstance(target._label_gtk, Gtk.Label)
        viewport = target._scene_gtk.get_child()
        assert target._label_gtk is viewport.get_child()


class TestSceneValue:
    """Unit tests for :class:`.SceneValue`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneValue()
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_scene_gtk', 'scene_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = VVALUE.SceneValue()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.SceneValue, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
