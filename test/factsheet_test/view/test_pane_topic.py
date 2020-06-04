"""
Unit tests for class to display topic in a factsheet window pane.

See :mod:`.pane_topic`.
"""
import pytest   # type: ignore[import]

from factsheet.control import topic as CTOPIC
from factsheet.content.section import section_topic as MTOPIC
from factsheet.view import pane_topic as VTOPIC
from factsheet.view import ui as UI
from factsheet.view import view_infoid as VINFOID

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_control_topic(text_ui_infoid):
    """Pytest fixture returns a stock
    :class:`~.factsheet.control.topic.Topic` control.
    """
    NAME = text_ui_infoid['name']
    SUMMARY = text_ui_infoid['summary']
    TITLE = text_ui_infoid['title']
    model = MTOPIC.Topic(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    control = CTOPIC.Topic.open(pm_model=model)
    return control


class TestPaneTopic:
    """Unit tests for :class:`.PaneTopic`."""

    def test_init(self, patch_control_topic):
        """Confirm initialization.

        Case: visual elements.
        """
        # Setup
        CONTROL = patch_control_topic
        # Test
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        assert target._control is CONTROL
        assert isinstance(target._pane, Gtk.Box)
        assert target._pane.is_visible()
        actions_topic = target._pane.get_action_group('topic')
        assert isinstance(actions_topic, Gio.SimpleActionGroup)

        # Components
        assert isinstance(target._context_name, Gtk.Popover)
        assert isinstance(target._context_summary, Gtk.Frame)
        assert isinstance(target._flip_summary, Gtk.CheckButton)
        assert target._name_former is None

        # Identification Information
        assert isinstance(target._infoid, VINFOID.ViewInfoId)
        assert target._infoid.name is not None
        assert target._infoid.summary is not None
        assert target._infoid.title is not None

        # Topic Menu
        assert actions_topic.lookup_action('show-help-topic') is not None

        # Topic Display Menu
        assert actions_topic.lookup_action('popup-name') is not None
        assert actions_topic.lookup_action('reset-name') is not None
        assert actions_topic.lookup_action('flip-summary') is not None
        assert actions_topic.lookup_action(
            'show-help-topic-display') is not None

        # Teardown
        target._pane.destroy()
        del target._pane

    def test_init_activate(self, patch_control_topic):
        """Confirm initialization.

        Case: name view activation signal."""
        # Setup
        entry_gtype = GO.type_from_name(GO.type_name(Gtk.Entry))
        delete_signal = GO.signal_lookup('activate', entry_gtype)
        CONTROL = patch_control_topic
        # Test
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        entry = target._infoid.get_view_name()
        activate_id = GO.signal_handler_find(
            entry, GO.SignalMatchType.ID, delete_signal,
            0, None, None, None)
        assert 0 != activate_id
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_get_infoid(self, patch_control_topic):
        """Confirm returns :class:`.InfoId` attribute."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        # Test
        assert target._infoid is target.get_infoid()
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_flip_summary(self, patch_control_topic):
        """Confirm flip of facthseet summary visibility.

        - Case: hide
        - Case: show
        """
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        target._context_summary.show()
        assert target._context_summary.get_visible()
        assert target._flip_summary.get_active()
        # Test: hide
        # Call clicked to invoke target.on_flip_summary.  Method clicked
        # has the side effect of setting active state of _flip_summary.
        target._flip_summary.clicked()
        assert not target._context_summary.get_visible()
        assert not target._flip_summary.get_active()
        # Test: show
        # As in case hide.
        target._flip_summary.clicked()
        assert target._context_summary.get_visible()
        assert target._flip_summary.get_active()
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_popup_name(self, patch_control_topic):
        """Confirm name popover becomes visible."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        target._context_name.hide()
        target._infoid.get_view_name().set_text('The Confy Chair!')
        # Test
        target.on_popup_name(None, None)
        assert target._context_name.get_visible()
        assert target._infoid.name == target._name_former
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_reset_name(self, patch_control_topic):
        """Confirm name reset in popover."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)
        name = target._infoid.get_view_name()
        name.set_text('The Spanish Inquisition!')
        target._name_former = 'Oh no!'
        # Test
        target.on_reset_name(None, None)
        assert target._name_former == name.get_text()
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_show_dialog(self, patch_control_topic, monkeypatch):
        """Confirm handler runs dialog.

        Case: topic pane in top-level window.

        See manual tests for dialog content checks.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)

        window = Gtk.ApplicationWindow()
        monkeypatch.setattr(
            Gtk.Widget, 'get_toplevel', lambda *_args: window)
        dialog = Gtk.Dialog()
        dialog.show()
        # Test
        target.on_show_dialog(None, None, dialog)
        assert patch.called
        assert not dialog.is_visible()
        assert dialog.get_transient_for() is window
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_show_dialog_no_top(self, patch_control_topic, monkeypatch):
        """Confirm handler runs dialog.

        Case: topic pane not in top-level window.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        CONTROL = patch_control_topic
        target = VTOPIC.PaneTopic(pm_control=CONTROL)

        monkeypatch.setattr(
            Gtk.Widget, 'get_toplevel', lambda *_args: target._pane)
        window = Gtk.ApplicationWindow()
        dialog = Gtk.Dialog()
        dialog.set_transient_for(window)
        dialog.show()
        # Test
        target.on_show_dialog(None, None, dialog)
        assert patch.called
        assert not dialog.is_visible()
        assert dialog.get_transient_for() is None
        # Teardown
        target._pane.destroy()
        del target._pane

    def test_on_show_dialog_input(self):
        """Confirm presence of shared dialogs."""
        # Setup
        # Test
        assert isinstance(UI.HELP_TOPIC, Gtk.Dialog)
        assert isinstance(UI.HELP_TOPIC_DISPLAY, Gtk.Dialog)
