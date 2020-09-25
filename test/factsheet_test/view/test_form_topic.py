"""
Unit tests for class to display topic form in a factsheet window pane.
See :mod:`.form_topic`.
"""
import dataclasses as DC
import pytest   # type: ignore[import]

from factsheet.control import control_topic as CTOPIC
from factsheet.model import topic as MTOPIC
from factsheet.view import form_topic as VTOPIC
from factsheet.view import ui as UI
from factsheet.view import view_infoid as VINFOID

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_control_topic(patch_args_infoid):
    """Pytest fixture returns a stock :class:`.ControlTopic`."""
    ARGS = patch_args_infoid
    model = MTOPIC.Topic()
    model.init_identity(**DC.asdict(ARGS))
    control = CTOPIC.ControlTopic(p_model=model)
    return control


class TestFormTopic:
    """Unit tests for :class:`.FormTopic`."""

    def test_init(self, patch_control_topic):
        """Confirm initialization.

        Case: visual elements.
        """
        # Setup
        CONTROL = patch_control_topic
        model = CONTROL._model
        # Test
        target = VTOPIC.FormTopic(p_control=CONTROL)
        assert target._control is CONTROL
        assert isinstance(target._gtk_pane, Gtk.Box)
        assert target in model._forms.values()
        assert target._gtk_pane.is_visible()
        actions_topic = target._gtk_pane.get_action_group('topic')
        assert isinstance(actions_topic, Gio.SimpleActionGroup)

        # Components
        assert isinstance(target._context_name, Gtk.Popover)
        # assert isinstance(target._context_summary, Gtk.Frame)
        # assert isinstance(target._flip_summary, Gtk.CheckButton)
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
        # assert actions_topic.lookup_action('flip-summary') is not None
        assert actions_topic.lookup_action(
            'show-help-topic-display') is not None

        # Teardown
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_init_activate(self, patch_control_topic):
        """Confirm initialization.

        Case: name view activation signal."""
        # Setup
        entry_gtype = GO.type_from_name(GO.type_name(Gtk.Entry))
        delete_signal = GO.signal_lookup('activate', entry_gtype)
        CONTROL = patch_control_topic
        # Test
        target = VTOPIC.FormTopic(p_control=CONTROL)
        entry = target._infoid.get_view_name()
        activate_id = GO.signal_handler_find(
            entry, GO.SignalMatchType.ID, delete_signal,
            0, None, None, None)
        assert 0 != activate_id
        # Teardown
        target._gtk_pane.destroy()
        del target._gtk_pane

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_gtk_pane', 'gtk_pane'],
        ])
    def test_property(self, patch_control_topic, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VTOPIC.FormTopic, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_get_infoid(self, patch_control_topic):
        """Confirm returns :class:`.InfoId` attribute."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)
        # Test
        assert target._infoid is target.get_infoid()
        # Teardown
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_on_popup_name(self, patch_control_topic):
        """Confirm name popover becomes visible."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)
        target._context_name.hide()
        target._infoid.get_view_name().set_text('The Confy Chair!')
        # Test
        target.on_popup_name(None, None)
        assert target._context_name.get_visible()
        assert target._infoid.name == target._name_former
        # Teardown
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_on_reset_name(self, patch_control_topic):
        """Confirm name reset in popover."""
        # Setup
        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)
        name = target._infoid.get_view_name()
        name.set_text('The Spanish Inquisition!')
        target._name_former = 'Oh no!'
        # Test
        target.on_reset_name(None, None)
        assert target._name_former == name.get_text()
        # Teardown
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_on_show_dialog(self, patch_control_topic, monkeypatch):
        """| Confirm handler runs dialog.
        | Case: topic form in top-level window.
        | See manual tests for dialog content checks.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)

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
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_on_show_dialog_no_top(self, patch_control_topic, monkeypatch):
        """| Confirm handler runs dialog.
        | Case: topic form not in top-level window.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        CONTROL = patch_control_topic
        target = VTOPIC.FormTopic(p_control=CONTROL)

        monkeypatch.setattr(
            Gtk.Widget, 'get_toplevel', lambda *_args: target._gtk_pane)
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
        target._gtk_pane.destroy()
        del target._gtk_pane

    def test_on_show_dialog_input(self):
        """Confirm presence of shared dialogs."""
        # Setup
        # Test
        assert isinstance(UI.HELP_TOPIC, Gtk.Dialog)
        assert isinstance(UI.HELP_TOPIC_DISPLAY, Gtk.Dialog)
