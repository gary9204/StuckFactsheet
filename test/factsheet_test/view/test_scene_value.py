"""
Defines unit tests for classes to display fact values.
See :mod:`.scene_value`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.view import scene_value as VVALUE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]  # noqa:E402


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
        label = viewport.get_child()
        assert target._label_gtk is label
        assert target.SYNOPSIS_DEFAULT == label.get_label()
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_width_chars() is target.WIDTH_DEFAULT
        assert label.get_max_width_chars() is target.WIDTH_MAX
        assert label.get_ellipsize() is Pango.EllipsizeMode.MIDDLE
        assert label.get_selectable()

    def test_set_markup(self):
        """Confirm markup change."""
        # Setup
        MARKUP = 'A Norwegian Blue'
        target = VVALUE.SceneSynopsis()
        # Test
        target.set_markup(MARKUP)
        assert MARKUP == target._label_gtk.get_label()


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
        label = viewport.get_child()
        assert target._label_gtk is label
        assert target.TEXT_DEFAULT == label.get_label()
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_line_wrap()
        assert label.get_line_wrap_mode() is Pango.WrapMode.WORD_CHAR
        assert label.get_selectable()

    def test_set_markup(self):
        """Confirm text change."""
        # Setup
        TEXT = 'A Norwegian Blue'
        target = VVALUE.SceneText()
        # Test
        target.set_text(TEXT)
        assert TEXT == target._label_gtk.get_label()


class TestSceneValue:
    """Unit tests for :class:`.SceneValue`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneValue()
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)

    def test_add_content(self):
        """Confirm content added to scene."""
        # Setup
        CONTENT = Gtk.TreeView()
        target = VVALUE.SceneValue()
        # Test
        target.add_content(CONTENT)
        assert target._scene_gtk.get_child() is CONTENT

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
