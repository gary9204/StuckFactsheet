"""
Unit tests for base classes for topic specification.  See
:class:`~.spec.base_s.Base`.

.. include:: /test/refs_include_pytest.txt
"""
from pathlib import Path
import pytest  # type: ignore[import]
import gi   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.topic as MTOPIC
import factsheet.spec.base_s as SBASE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestBase:
    """Unit tests for :class:`~.spec.base_s.Base`."""

    def test_init(self):
        """| Confirm initialization.
        | Case: TBD
        """
        # Setup
        NAME_SPEC = 'Parrot'
        # Test
        target = SBASE.Base(p_name=NAME_SPEC)
        assert isinstance(target._name_spec, BUI.ModelTextMarkup)
        assert NAME_SPEC == target._name_spec.text

    def test_init_name_topic(self):
        """| Confirm initialization.
        | Case: topic name store and view factories
        """
        # Setup
        BLANK = ''
        NAME_SPEC = 'Parrot'
        # Test
        target = SBASE.Base(p_name=NAME_SPEC)
        assert isinstance(target._name_topic, MTOPIC.Name)
        assert BLANK == target._name_topic.text
        assert isinstance(
            target._new_display_name_topic, BUI.FactoryDisplayTextMarkup)
        assert target._new_display_name_topic._ui_model is (
            target._name_topic._ui_model)
        assert isinstance(
            target._new_editor_name_topic, BUI.FactoryEditorTextMarkup)
        assert target._new_editor_name_topic._ui_model is (
            target._name_topic._ui_model)

    @pytest.mark.skip(reason='next')
    def test_add_page_intro(self):
        """Confirm assistant construction."""
        # Setup
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        assist = target.new_assistant()
        # Test
        target.add_page_intro(p_assist=assist)

    def test_new_assistant(self):
        """| Confirm assistant construction.
        | Case: assistant file accessible and consistent.
        """
        # Setup
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        # Test
        assist = target.new_assistant()
        assert isinstance(assist, Gtk.Assistant)

    @pytest.mark.skip(reason="GTK.Builder aborts on invalid file contents.")
    def test_new_assistant_error(self, monkeypatch):
        """| Confirm assistant construction.
        | Case: assistant file error.
        """
        # Setup
        patch_ui = """
            <?xml version="1.0" encoding="UTF-8"?>
            <!-- Generated with glade 3.22.1 -->
            <interface>
              <requires lib="gtk+" version="3.20"/>
              <object class="GtkAssistant">
                <property name="can_focus">False</property>
                <property name="use_header_bar">1</property>
                <badkey>
                <child>
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Introduction page</property>
                  </object>
                  <packing>
                    <property name="page_type">intro</property>
                    <property name="has_padding">False</property>
                  </packing>
                </child>
                <child>
                  <placeholder/>
                </child>
                <child>
                  <placeholder/>
                </child>
              </object>
            </interface>
            """

        def new_from_file(_path):
            return Gtk.Builder.new_from_string(patch_ui, len(patch_ui))

        monkeypatch.setattr(Gtk.Builder, 'new_from_file', new_from_file)
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        # Test
        assert target.new_assistant() is None


class TestExceptions:
    """Unit tests for exceptions defined in :mod:`.control_sheet`."""

    @pytest.mark.parametrize('TARGET, SUPER', [
        (SBASE.ExceptionSpec, Exception),
        (SBASE.SpecFileError, SBASE.ExceptionSpec),
        (SBASE.UiObjectNotFoundError, SBASE.ExceptionSpec),
        ])
    def test_exceptions(self, TARGET, SUPER):
        """Confirm presence of exceptions.

        :parem TARGET: exception under test.
        :param SUPER: super class of exception.
        """
        # Setup
        # Test
        assert issubclass(TARGET, SUPER)


@pytest.fixture
def ui_desc_minimal():
    """Pytest fixture: Return minimal user interface description.

    :returns: DESC - user interface description as string.
    :returns: ID_OBJECT - ID of a `Gtk.Label`_ object.
    :returns: TEXT_ITEM - Sof label object.

    .. _`Gtk.Label`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
    """
    ID_OBJECT = 'ui_object'
    TEXT_OBJECT = 'Test Item'
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
    """.format(ID_OBJECT, TEXT_OBJECT)
    return DESC, ID_OBJECT, TEXT_OBJECT


@pytest.fixture
def set_logger_debug():
    """Pytest fixture with teardown: temporarily set SBASE log level to
    DEBUG.
    """
    level = SBASE.logger.getEffectiveLevel()
    SBASE.logger.setLevel('DEBUG')
    yield
    SBASE.logger.setLevel(level)


class TestGetUiObject:
    """Unit tests for :class:`.GetUiObject`."""

    def test_init_path(
            self, ui_desc_minimal, tmp_path, caplog, set_logger_debug):
        """| Confirm initialization.
        | Case: description provided by path.

        :param ui_desc_minimal: fixture :func:`.ui_desc_minimal`.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        DESC, ID_OBJECT, TEXT_OBJECT = ui_desc_minimal
        FILE_NAME = 'test.ui'
        PATH = tmp_path / FILE_NAME
        _ = PATH.write_text(DESC)
        N_LOGS = 1
        LAST = -1
        log_message = 'Building UI description from {}.'.format(str(PATH))
        # Test
        target = SBASE.GetUiObject(p_path=PATH)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target._builder.get_object(ID_OBJECT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_OBJECT == label.get_text()

    def test_init_string(self, ui_desc_minimal, caplog, set_logger_debug):
        """| Confirm initialization.
        | Case: description provided by path.

        :param ui_desc_minimal: fixture :func:`.ui_desc_minimal`.
        :param caplog: built-in fixture `Pytest caplog`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        DESC, ID_OBJECT, TEXT_OBJECT = ui_desc_minimal
        N_LOGS = 1
        LAST = -1
        log_message = 'Building UI description from string.'
        # Test
        target = SBASE.GetUiObject(p_string=DESC)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target._builder.get_object(ID_OBJECT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_OBJECT == label.get_text()

    def test_init_none(self):
        """| Confirm initialization.
        | Case: no description provided.
        """
        # Setup
        ERROR = 'No user interface description provided.'
        # Test
        with pytest.raises(SBASE.UiDescriptionError, match=ERROR):
            _target = SBASE.GetUiObject()

    def test_init_file_error(self, tmp_path, caplog, set_logger_debug):
        """| Confirm initialization.
        | Case: error accessing description provided by path.

        :param caplog: built-in fixture `Pytest caplog`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        FILE_NAME = 'no.ui'
        PATH = tmp_path / FILE_NAME
        MATCH = 'Could not access description file "{}".'.format(PATH.name)
        # Test
        with pytest.raises(SBASE.UiDescriptionError, match=MATCH) as exc_info:
            _target = SBASE.GetUiObject(p_path=PATH)
        cause = exc_info.value.__cause__
        assert isinstance(cause, FileNotFoundError)

    def test_call(self, ui_desc_minimal):
        """| Confirm object retrieval.
        | Case: ID matches an object.
        """
        # Setup
        DESC, ID_OBJECT, TEXT_OBJECT = ui_desc_minimal
        target = SBASE.GetUiObject(p_string=DESC)
        # Test
        ui_object = target(ID_OBJECT)
        assert isinstance(ui_object, Gtk.Label)
        assert TEXT_OBJECT == ui_object.get_text()

    def test_call_no_object(self, ui_desc_minimal):
        """| Confirm object retrieval.
        | Case: ID does not matches an object.
        """
        # Setup
        DESC, _ID_OBJECT, _TEXT_OBJECT = ui_desc_minimal
        ID_NONE = 'ui_oops'
        VALUE = 'No object found for ID {}.'.format(ID_NONE)
        target = SBASE.GetUiObject(p_string=DESC)
        # Test
        with pytest.raises(SBASE.UiObjectNotFoundError, match=VALUE):
            _ui_object = target(ID_NONE)


class TestModule:
    """Unit tests for module-level components of :mod:`.base_s`."""

    @pytest.mark.parametrize('CONSTANT, VALUE', [
        (SBASE.SUFFIX_SPEC, '.py'),
        (SBASE.SUFFIX_ASSIST, '.ui'),
        ])
    def test_constants(self, CONSTANT, VALUE):
        """Confirm class contant definitions.

        :param CONSTANT: constant under test.
        :param VALUE: expected value of constant.
        """
        # Setup
        # Test
        assert CONSTANT == VALUE
