"""
Unit etsts for class to display and edit topics outline of a factsheet.
See :mod:`.editor_topics`.
"""
import pytest  # type: ignore[import]
import gi   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.view.editor_topics as VTOPICS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestEditorTopics:
    """Unit tests for :class:`.editor_topics`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        # Test
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        assert target._control_sheet is control_sheet
        assert isinstance(target._ui_view, Gtk.Frame)

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(
            self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        attr = getattr(target, NAME_ATTR)
        CLASS = VTOPICS.EditorTopics
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestModule:
    """Unit tests for module-level components of :mod:`.editor_topics`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (VTOPICS.UiEditorTopics, Gtk.Frame),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
