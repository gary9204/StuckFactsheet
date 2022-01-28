"""
Unit tests for functions and objects for user interface elements.  See
:mod:`.view.ui`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def set_logger_debug():
    """Pytest fixture with teardown: temporarily set SBASE log level to
    DEBUG.
    """
    level = UI.logger.getEffectiveLevel()
    UI.logger.setLevel('DEBUG')
    yield
    UI.logger.setLevel(level)


@pytest.fixture
def ui_desc_minimal():
    """Pytest fixture: Return minimal user interface description.

    :returns:

        * DESC - user interface description as string.
        * ID_ELEMENT - ID of a `Gtk.Label`_ object.
        * TEXT_ITEM - contents of label object.

    .. _`Gtk.Label`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
    """
    ID_ELEMENT = 'ui_object'
    TEXT_ELEMENT = 'Test Item'
    DESC = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Generated with glade 3.22.1 -->
    <interface>
      <requires lib="gtk+" version="3.20"/>
      <object class="GtkLabel" id="{}">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">{}</property>
      </object>
    </interface>
    """.format(ID_ELEMENT, TEXT_ELEMENT)
    return DESC, ID_ELEMENT, TEXT_ELEMENT


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


class TestGetUiObject:
    """Unit tests for :class:`.GetUiView`."""

    class PatchGetUiObject(UI.GetUiView):
        """Patch subclass for testing abstract :class;`.GetUiView`."""

        def __init__(self, p_description, **kwargs):
            super().__init__(**kwargs)
            ALL = -1
            self._builder = Gtk.Builder.new_from_string(p_description, ALL)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (UI.GetUiView, '__init__'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: class that should be abstract.
        :param NAME_METHOD: method that should be abstract.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_init(self, ui_desc_minimal, caplog, set_logger_debug):
        """Confirm initialization.

        :param ui_desc_minimal: fixture :func:`.ui_desc_minimal`.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param set_logger_debug: fixture :func:`.set_logger_debug`.
        """
        # Setup
        DESC, ID_ELEMENT, TEXT_ELEMENT = ui_desc_minimal
        N_LOGS = 1
        LAST = -1
        log_message = 'Building UI description ...'
        # Test
        target = TestGetUiObject.PatchGetUiObject(p_description=DESC)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target._builder.get_object(ID_ELEMENT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_ELEMENT == label.get_text()

    def test_call(self, ui_desc_minimal):
        """| Confirm user interface element retrieval.
        | Case: ID matches an element.
        """
        # Setup
        DESC, ID_ELEMENT, TEXT_ELEMENT = ui_desc_minimal
        target = TestGetUiObject.PatchGetUiObject(p_description=DESC)
        # Test
        ui_object = target(ID_ELEMENT)
        assert isinstance(ui_object, Gtk.Label)
        assert TEXT_ELEMENT == ui_object.get_text()

    def test_call_no_element(self, ui_desc_minimal):
        """| Confirm user interface element retrieval.
        | Case: ID does not matches an element.
        """
        # Setup
        DESC, _ID_ELEMENT, _TEXT_ELEMENT = ui_desc_minimal
        ID_NONE = 'ui_oops'
        VALUE = 'No element found for ID {}.'.format(ID_NONE)
        target = TestGetUiObject.PatchGetUiObject(p_description=DESC)
        # Test
        with pytest.raises(UI.UiObjectNotFoundError, match=VALUE):
            _ui_element = target(ID_NONE)


class TestGetUiObjectPath:
    """Unit tests for :class:`.GetUiViewByPath`."""

    def test_init(self, ui_desc_minimal, tmp_path, caplog, set_logger_debug):
        """| Confirm initialization.
        | Case: description provided by path.

        :param ui_desc_minimal: fixture :func:`.ui_desc_minimal`.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        :param set_logger_debug: fixture :func:`.set_logger_debug`.
        """
        # Setup
        DESC, ID_ELEMENT, TEXT_ELEMENT = ui_desc_minimal
        FILE_NAME = 'test.ui'
        PATH = tmp_path / FILE_NAME
        _ = PATH.write_text(DESC)
        N_LOGS = 2
        LAST = -1
        log_message = '... from file {}.'.format(str(PATH))
        # Test
        target = UI.GetUiViewByPath(p_path=PATH)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target(ID_ELEMENT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_ELEMENT == label.get_text()

    def test_init_file_error(self, tmp_path):
        """| Confirm initialization.
        | Case: error accessing description provided by path.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        :param set_logger_debug: fixture :func:`.set_logger_debug`.
        """
        # Setup
        FILE_NAME = 'no.ui'
        PATH = tmp_path / FILE_NAME
        MATCH = 'Could not access description file "{}".'.format(PATH.name)
        # Test
        with pytest.raises(UI.UiDescriptionError, match=MATCH) as exc_info:
            _target = UI.GetUiViewByPath(p_path=PATH)
        cause = exc_info.value.__cause__
        assert isinstance(cause, FileNotFoundError)


class TestGetUiObjectStr:
    """Unit tests for :class:`.GetUiViewByStr`."""

    def test_init(self, ui_desc_minimal, caplog, set_logger_debug):
        """| Confirm initialization.
        | Case: description provided by path.

        :param ui_desc_minimal: fixture :func:`.ui_desc_minimal`.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        DESC, ID_ELEMENT, TEXT_ELEMENT = ui_desc_minimal
        N_LOGS = 2
        LAST = -1
        log_message = '... from string.'
        # Test
        target = UI.GetUiViewByStr(p_string=DESC)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target(ID_ELEMENT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_ELEMENT == label.get_text()


class TestModule:
    """Unit tests for module-level components of :mod:`.ui`."""

    @pytest.mark.parametrize('TARGET, SUPER', [
        (UI.ExceptionUi, Exception),
        (UI.UiDescriptionError, UI.ExceptionUi),
        (UI.UiObjectNotFoundError, UI.ExceptionUi),
        ])
    def test_exceptions(self, TARGET, SUPER):
        """Confirm presence of exceptions.

        :parem TARGET: exception under test.
        :param SUPER: super class of exception.
        """
        # Setup
        # Test
        assert issubclass(TARGET, SUPER)

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
