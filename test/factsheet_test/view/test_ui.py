"""
Unit tests for functions and objects for user interface elements.

See :mod:`.view.ui`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_factory as AFACTORY
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestTypes:
    """Unit tests for type definitions in :mod:`.ui`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert UI.IdTopic is AFACTORY.IdTopic
        assert UI.IndexOutline is AFACTORY.IndexOutline
        assert UI.OutlineTemplates is AFACTORY.OutlineTemplates
        assert UI.OutlineTopics is AFACTORY.OutlineTopics
        assert UI.ViewOutlineTemplates is AFACTORY.ViewOutlineTemplates
        assert UI.ViewOutlineTopics is AFACTORY.ViewOutlineTopics
        assert UI.NewViewOutlineTopics is not None


class TestUiActions:
    """Unit tests for module functions defined in :mod:`.view.ui`.
    """

    def test_new_active_action(self):
        """Confirm new action connected to activate handler."""
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
            pm_group=group, p_name=name_action, px_handler=handler)
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
        """Confirm new action connected to activate handler."""
        # Setup
        _load_signals = Gio.SimpleAction.new('Null', None)
        action_gtype = GO.type_from_name(GO.type_name(Gio.SimpleAction))
        signal = GO.signal_lookup('activate', action_gtype)
        N_DEFAULT = 0

        group = Gio.SimpleActionGroup()
        name_action = 'test-action'

        def handler(p_action, p_target, px_dialog): pass
        dialog = Gtk.Dialog()
        # Test
        UI.new_action_active_dialog(pm_group=group, p_name=name_action,
                                    px_handler=handler, px_dialog=dialog)
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

    @pytest.mark.skip(reason='Not currently needed.')
    def test_new_action_bool_active(self):
        """Confirm new boolean action connected to activate handler."""
        # Setup
        # Review test_new_activate_action before updating.
#         action_gtype = GO.type_from_name(GO.type_name(Gio.SimpleAction))
#         signal = GO.signal_lookup('activate', action_gtype)
#
#         group = Gio.SimpleActionGroup()
#         name_action = 'test-action'
#         state = True
#
#         def handler(p_action, p_target): pass
        # Test
#         UI.new_activate_action_boolean(
#             pm_group=group, p_name=name_action, p_state=state,
#             px_handler=handler)
#         action = group.lookup_action(name_action)
#         assert action is not None
#         assert state == action.get_state().get_boolean()
#         id_signal = GO.signal_handler_find(
#             action, GO.SignalMatchType.ID, signal,
#             0, None, None, None)
#         assert 0 != id_signal
