"""
Defines unit tests for classes to display integer fact values.
See :mod:`.scene_int`.
"""
from factsheet.view import scene_int as VINT


class TestSceneSynopsisInt:
    """Unit tests for :class:`.SceneSynopsisInt`."""

    def test_init(self):
        """| Confirm initialization."""
        # Setup
        VALUE = 42
        # Test
        target = VINT.SceneSynopsisInt(p_value=VALUE)
        value_text = target._label_gtk.get_label()
        assert VALUE == int(value_text)


class TestSceneTextInt:
    """Unit tests for :class:`.SceneTextInt`."""

    def test_init(self):
        """| Confirm initialization."""
        # Setup
        VALUE = 42
        REPR = repr(VALUE)
        # Test
        target = VINT.SceneTextInt(p_value=VALUE)
        value_text = target._label_gtk.get_label()
        assert REPR == value_text
        assert VALUE == int(value_text)
