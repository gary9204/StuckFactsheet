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
import factsheet.view.view_markup as VMARKUP

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

    def test_new_page_identify_sites(self, monkeypatch):
        """Confirm builder populates page sites."""
        # Setup
        PATCH_UI_PAGE_IDENTITY = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.22.1 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkBox" id="ui_page_identify">
            <child>
              <object class="GtkBox" id="ui_identify_site_name">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_identify_site_title">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_identify_site_summary">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">2</property>
              </packing>
            </child>
          </object>
        </interface>
        """
        monkeypatch.setattr(SBASE, 'UI_PAGE_IDENTIFY', PATCH_UI_PAGE_IDENTITY)

        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        sites = list()
        display_name = target._new_display_name_topic()
        editor_name = target._new_editor_name_topic()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        sites.append(view_name)
        FIRST = 0
        # Test
        new_page = target.new_page_identify(view_name)
        children = new_page.get_children()
        for index in range(len(sites)):
            site = children[index]
            view = site.get_children()[FIRST]
            assert view is sites[index].ui_view

    def test_new_page_identify_parse(self):
        """Confirm builder can parse page description."""
        # Setup
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        NAME = MTOPIC.Name()
        NEW_DISPLAY_NAME = MTOPIC.FactoryDisplayName(NAME)
        DISPLAY_NAME = NEW_DISPLAY_NAME()
        NEW_EDITOR_NAME = MTOPIC.FactoryEditorName(NAME)
        EDITOR_NAME = NEW_EDITOR_NAME()
        VIEW_NAME = VMARKUP.ViewMarkup(DISPLAY_NAME, EDITOR_NAME, 'Name')
        # Test
        new_page = target.new_page_identify(VIEW_NAME)
        assert isinstance(new_page, SBASE.PageAssist)

    def test_new_page_intro_parse(self):
        """Confirm builder can parse page description."""
        # Setup
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        # Test
        new_page = target.new_page_intro()
        assert isinstance(new_page, SBASE.PageAssist)

    def test_new_assistant(self):
        """Confirm assistant construction."""
        # Setup
        NAME_SPEC = 'Parrot'
        target = SBASE.Base(p_name=NAME_SPEC)
        # Test
        assist = target.new_assistant()
        assert isinstance(assist, Gtk.Assistant)


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
    :returns: ID_ELEMENT - ID of a `Gtk.Label`_ object.
    :returns: TEXT_ITEM - Sof label object.

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

    class PatchGetUiObject(SBASE.GetUiObject):
        """Patch subclass for testing abstract :class;`.GetUiObject`."""

        def __init__(self, p_description, **kwargs):
            super().__init__(**kwargs)
            ALL = -1
            self._builder = Gtk.Builder.new_from_string(p_description, ALL)

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (SBASE.GetUiObject, '__init__'),
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
        with pytest.raises(SBASE.UiObjectNotFoundError, match=VALUE):
            _ui_element = target(ID_NONE)


class TestGetUiObjectPath:
    """Unit tests for :class:`.GetUiObjectPath`."""

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
        target = SBASE.GetUiObjectPath(p_path=PATH)
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
        with pytest.raises(SBASE.UiDescriptionError, match=MATCH) as exc_info:
            _target = SBASE.GetUiObjectPath(p_path=PATH)
        cause = exc_info.value.__cause__
        assert isinstance(cause, FileNotFoundError)


class TestGetUiObjectStr:
    """Unit tests for :class:`.GetUiObjectStr`."""

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
        target = SBASE.GetUiObjectStr(p_string=DESC)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'DEBUG' == record.levelname
        label = target(ID_ELEMENT)
        assert isinstance(label, Gtk.Label)
        assert TEXT_ELEMENT == label.get_text()


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
