"""
Unit tests for functions and objects for user interface elements.

See :mod:`.view.ui`.
"""
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestUiItems:
    """Unit tests for user interface constants and shared objects."""

    @pytest.mark.parametrize('NAME, TYPE', [
        ('DIR_UI', Path),
        ('ABOUT_APP', Gtk.Dialog),
        ('HELP_APP', Gtk.Dialog),
        ('INTRO_APP', Gtk.Dialog),
        ('HELP_SHEET', Gtk.Dialog),
        ('HELP_TOPIC', Gtk.Dialog),
        ('HELP_TOPIC_DISPLAY', Gtk.Dialog),
        ])
    def test_defined(self, NAME, TYPE):
        """Confirm module defines constants and shared objects."""
        # Setup
        item = getattr(UI, NAME)
        assert isinstance(item, TYPE)


class TestUiActions:
    """Unit tests for module functions defined in :mod:`.view.ui`.
    """

    def test_new_action_active(self):
        """Confirm activate signal for new action invokes handler."""
        # Setup
        _load_signals = Gio.SimpleAction.new('Null', None)
        action_gtype = GO.type_from_name(GO.type_name(Gio.SimpleAction))
        signal = GO.signal_lookup('activate', action_gtype)
        N_DEFAULT = 0

        group = Gio.SimpleActionGroup()
        name_action = 'test-action'

        def handler(p_action, p_target): pass
        # Test
        UI.new_action_active(
            p_group=group, p_name=name_action, p_handler=handler)
        action = group.lookup_action(name_action)
        assert action is not None
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                action, GO.SignalMatchType.ID, signal, 0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(action, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    def test_new_action_active_dialog(self):
        """Confirm activate signal for new action invokes handler with
        dialog to display.
        """
        # Setup
        # Warning: GO.signal_lookup fails unless there is a prior
        #    reference to Gio.SimpleAction.  Reference loads GObject
        #    class.
        _load_signals = Gio.SimpleAction.new('Null', None)
        action_gtype = GO.type_from_name(GO.type_name(Gio.SimpleAction))
        signal = GO.signal_lookup('activate', action_gtype)
        N_DEFAULT = 0

        group = Gio.SimpleActionGroup()
        name_action = 'test-action'

        def handler(p_action, p_target, p_dialog): pass
        dialog = Gtk.Dialog()
        # Test
        UI.new_action_active_dialog(p_group=group, p_name=name_action,
                                    p_handler=handler, p_dialog=dialog)
        action = group.lookup_action(name_action)
        assert action is not None
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                action, GO.SignalMatchType.ID, signal, 0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(action, id_signal)

        assert N_DEFAULT + 1 == n_handlers

#     @pytest.mark.skip(reason='Not currently needed.')
#     def test_new_action_bool_active(self):
#         """Confirm new boolean action connected to activate handler."""
#         # Setup
#         # Review test_new_activate_action before updating.
# #         action_gtype = GO.type_from_name(GO.type_name(Gio.SimpleAction))
# #         signal = GO.signal_lookup('activate', action_gtype)
# #
# #         group = Gio.SimpleActionGroup()
# #         name_action = 'test-action'
# #         state = True
# #
# #         def handler(p_action, p_target): pass
#         # Test
# #         UI.new_activate_action_boolean(
# #             p_group=group, p_name=name_action, p_state=state,
# #             p_handler=handler)
# #         action = group.lookup_action(name_action)
# #         assert action is not None
# #         assert state == action.get_state().get_boolean()
# #         id_signal = GO.signal_handler_find(
# #             action, GO.SignalMatchType.ID, signal,
# #             0, None, None, None)
# #         assert 0 != id_signal
