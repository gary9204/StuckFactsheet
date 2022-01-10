"""
Unit tests for base classes for topic specification.  See
:class:`~.spec.base_s.Base`.

.. include:: /test/refs_include_pytest.txt
"""
# from pathlib import Path
import pytest  # type: ignore[import]
import gi   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.topic as MTOPIC
import factsheet.spec.base_s as SBASE
import factsheet.view.view_markup as VMARKUP

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def new_identity_spec():
    """Pytest fixture: returns specification identity factory.

    Factory returns name, summary, and title for specification.
    """
    def new_identity():
        NAME_SPEC = 'Cheese Shop'
        SUMMARY_SPEC = 'Please select any cheese in the shop!'
        TITLE_SPEC = 'Cheese Specification'
        return NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC

    return new_identity


@pytest.fixture
def set_logger_debug():
    """Pytest fixture with teardown: temporarily set SBASE log level to
    DEBUG.
    """
    level = SBASE.logger.getEffectiveLevel()
    SBASE.logger.setLevel('DEBUG')
    yield
    SBASE.logger.setLevel(level)


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


class TestBase:
    """Unit tests for :class:`~.spec.base_s.Base`."""

    def test_call(self, new_identity_spec, monkeypatch):
        """Confirm orchestration for topic creation and placement.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        target.add_pages(p_assistant=assistant)

        called_new_assistant = False
        called_add_pages = False
        assistant_add_pages = None
        called_run_assistant = False
        assistant_run = None

        def patch_new_assistant(self):
            nonlocal called_new_assistant
            called_new_assistant = True  # pylint: disable=unused-variable
            nonlocal assistant
            return assistant

        def patch_add_pages(self, p_assistant):
            nonlocal called_add_pages
            called_add_pages = True  # pylint: disable=unused-variable
            nonlocal assistant_add_pages
            assistant_add_pages = (  # pylint: disable=unused-variable
                p_assistant)

        def patch_run_assistant(self, p_assistant):
            nonlocal called_run_assistant
            called_run_assistant = True  # pylint: disable=unused-variable
            nonlocal assistant_run
            assistant_run = p_assistant  # pylint: disable=unused-variable

        monkeypatch.setattr(SBASE.Base, 'new_assistant', patch_new_assistant)
        monkeypatch.setattr(SBASE.Base, 'add_pages', patch_add_pages)
        monkeypatch.setattr(SBASE.Base, 'run_assistant', patch_run_assistant)
        # Test
        target()
        assert called_new_assistant
        assert called_add_pages
        assert assistant_add_pages is assistant
        assert called_run_assistant
        assert assistant_run is assistant

    def test_init(self, new_identity_spec):
        """| Confirm initialization.
        | Case: non-topic attributes

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assert isinstance(target._name_spec, BUI.ModelTextMarkup)
        assert NAME_SPEC == target._name_spec.text
        assert SUMMARY_SPEC == target._summary_spec.text
        assert TITLE_SPEC == target._title_spec.text
        assert target._response is None

    def test_init_name_topic(self, new_identity_spec):
        """| Confirm initialization.
        | Case: attributes for topic name and view factories.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        BLANK = ''
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assert isinstance(target._name_topic, MTOPIC.Name)
        assert BLANK == target._name_topic.text
        assert isinstance(
            target._new_display_name_topic, MTOPIC.FactoryDisplayName)
        assert target._new_display_name_topic._ui_model is (
            target._name_topic._ui_model)
        assert isinstance(
            target._new_editor_name_topic, MTOPIC.FactoryEditorName)
        assert target._new_editor_name_topic._ui_model is (
            target._name_topic._ui_model)

    def test_init_summary_topic(self, new_identity_spec):
        """| Confirm initialization.
        | Case: attributes for topic summary and view factories.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        BLANK = ''
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assert isinstance(target._summary_topic, MTOPIC.Summary)
        assert BLANK == target._summary_topic.text
        assert isinstance(
            target._new_display_summary_topic, MTOPIC.FactoryDisplaySummary)
        assert target._new_display_summary_topic._ui_model is (
            target._summary_topic._ui_model)
        assert isinstance(
            target._new_editor_summary_topic, MTOPIC.FactoryEditorSummary)
        assert target._new_editor_summary_topic._ui_model is (
            target._summary_topic._ui_model)

    def test_init_title_topic(self, new_identity_spec):
        """| Confirm initialization.
        | Case: attributes for topic title and view factories.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        BLANK = ''
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assert isinstance(target._title_topic, MTOPIC.Title)
        assert BLANK == target._title_topic.text
        assert isinstance(
            target._new_display_title_topic, MTOPIC.FactoryDisplayTitle)
        assert target._new_display_title_topic._ui_model is (
            target._title_topic._ui_model)
        assert isinstance(
            target._new_editor_title_topic, MTOPIC.FactoryEditorTitle)
        assert target._new_editor_title_topic._ui_model is (
            target._title_topic._ui_model)

    @pytest.mark.parametrize('I_PAGE, TITLE', [
        (0, 'Introduction'),
        (1, 'Identify'),
        (2, 'Confirm'),
        ])
    def test_add_pages(self, new_identity_spec, I_PAGE, TITLE):
        """Confirm pages added to assistant.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param I_PAGE: index of page in assistant.
        :param TITLE: assistant's title for page.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        N_PAGES = 3
        # Test
        target.add_pages(p_assistant=assistant)
        page = assistant.get_nth_page(I_PAGE)
        assert TITLE == assistant.get_page_title(page)
        assert N_PAGES == assistant.get_n_pages()

    @pytest.mark.parametrize('METHOD, TITLE, TYPE, COMPLETE', [
        ('append_page_intro',
            'Introduction', Gtk.AssistantPageType.INTRO, True),
        ('append_page_identify',
            'Identify', Gtk.AssistantPageType.CONTENT, True),
        ('append_page_confirm',
            'Confirm', Gtk.AssistantPageType.CONFIRM, True),
        ])
    def test_append_page(
            self, new_identity_spec, METHOD, TITLE, TYPE, COMPLETE):
        """Confirm pages added to assistant.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :parem METHOD: append method under test.
        :param TITLE: assistant's title for page.
        :param TYPE: `Gtk.AssistantPageType`_ of page.

        .. _`Gtk.AssistantPageType`:
            https://lazka.github.io/pgi-docs/#Gtk-3.0/
            enums.html#Gtk.AssistantPageType
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        target_append = getattr(target, METHOD)
        FIRST = 0
        # Test
        target_append(p_assistant=assistant)
        page = assistant.get_nth_page(FIRST)
        assert TITLE == assistant.get_page_title(page)
        assert TYPE == assistant.get_page_type(page)
        assert assistant.get_page_complete(page) is COMPLETE

    def test_new_assistant(self, new_identity_spec):
        """Confirm assistant construction.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        # Test
        assist = target.new_assistant()
        assert isinstance(assist, Gtk.Assistant)

    @pytest.mark.parametrize('NAME_SIGNAL, ORIGIN, N_DEFAULT', [
            ('apply', Gtk.Assistant, 0),
            ('cancel', Gtk.Assistant, 0),
            ('destroy', Gtk.Assistant, 0),
            ('prepare', Gtk.Assistant, 0),
            ])
    def test_new_assistant_signals(
            self, new_identity_spec, NAME_SIGNAL, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param NAME_SIGNAL: name of signal under test.
        :param ORIGIN: source class of signal.
        :param N_DEFAULT: number of default handlers for signal.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                assistant, GO.SignalMatchType.ID, signal, 0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(assistant, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    def test_new_page_confirm_sites(self, monkeypatch, new_identity_spec):
        """Confirm builder populates page sites.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        PATCH_UI_PAGE_CONFIRM = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.22.1 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkBox" id="ui_page_confirm">
            <child>
              <object class="GtkBox" id="ui_confirm_site_name">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkScrolledWindow" id="ui_confirm_site_summary">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_confirm_site_title">
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
        monkeypatch.setattr(SBASE, 'UI_PAGE_CONFIRM', PATCH_UI_PAGE_CONFIRM)

        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        sites = list()
        display_name = target._new_display_name_topic()
        sites.append(display_name)
        display_summary = target._new_display_summary_topic()
        sites.append(display_summary)
        display_title = target._new_display_title_topic()
        sites.append(display_title)
        FIRST = 0
        # Test
        new_page = target.new_page_confirm(
            display_name, display_summary, display_title)
        children = new_page.get_children()
        for index in range(len(sites)):
            site = children[index]
            view = site.get_children()[FIRST]
            assert view is sites[index]

    def test_new_page_confirm_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        display_name = target._new_display_name_topic()
        display_summary = target._new_display_summary_topic()
        display_title = target._new_display_title_topic()
        # Test
        new_page = target.new_page_confirm(
            display_name, display_summary, display_title)
        assert isinstance(new_page, SBASE.PageAssist)

    def test_new_page_identify_sites(self, monkeypatch, new_identity_spec):
        """Confirm builder populates page sites.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
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
              <object class="GtkScrolledWindow" id="ui_identify_site_summary">
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_identify_site_title">
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

        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        sites = list()
        display_name = target._new_display_name_topic()
        editor_name = target._new_editor_name_topic()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        sites.append(view_name.ui_view)
        editor_summary = target._new_editor_summary_topic()
        sites.append(editor_summary)
        display_title = target._new_display_title_topic()
        editor_title = target._new_editor_title_topic()
        view_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        sites.append(view_title.ui_view)
        FIRST = 0
        # Test
        new_page = target.new_page_identify(
            view_name, editor_summary, view_title)
        children = new_page.get_children()
        for index in range(len(sites)):
            site = children[index]
            view = site.get_children()[FIRST]
            assert view is sites[index]

    def test_new_page_identify_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        display_name = target._new_display_name_topic()
        editor_name = target._new_editor_name_topic()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        editor_summary = target._new_editor_summary_topic()
        display_title = target._new_display_title_topic()
        editor_title = target._new_editor_title_topic()
        view_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        # Test
        new_page = target.new_page_identify(
            view_name, editor_summary, view_title)
        assert isinstance(new_page, SBASE.PageAssist)

    def test_new_page_intro_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        # Test
        new_page = target.new_page_intro()
        assert isinstance(new_page, SBASE.PageAssist)

    def test_on_apply(self, new_identity_spec):
        """Confirm assistant hidden and response set.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        # assistant.show()
        # Test
        target.on_apply(assistant)
        # assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.APPLY

    def test_on_cancel(self, new_identity_spec):
        """Confirm assistant hidden and response set.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        # assistant.show()
        # Test
        target.on_cancel(assistant)
        # assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.CANCEL

    def test_on_prepare(self, new_identity_spec, monkeypatch):
        """Confirm class defines method.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        page = Gtk.Box()
        _i_page = assistant.append_page(page)
        called_show_all = False

        def patch_show_all(self):
            nonlocal called_show_all
            called_show_all = True  # pylint: disable=unused-variable

        monkeypatch.setattr(Gtk.Widget, 'show_all', patch_show_all)
        # Test
        target.on_prepare(p_assistant=assistant, p_page=page)
        assert called_show_all

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('name', '_name_spec'),
        ('summary', '_summary_spec'),
        ('title', '_title_spec'),
        ])
    def test_property_access(self, new_identity_spec, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        attr = getattr(target, NAME_ATTR)
        CLASS = SBASE.Base
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_run_assistant(self, new_identity_spec, monkeypatch):
        """Confirm presentation of assistant.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        assistant.hide()

        def patch_main_iteration():
            nonlocal target
            target._response = Gtk.ResponseType.APPLY

        monkeypatch.setattr(Gtk, 'main_iteration', patch_main_iteration)
        # Test
        target.run_assistant(p_assistant=assistant)
        assert target._response is Gtk.ResponseType.APPLY
        assert not assistant.get_visible()


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

    def test_g_spec_basic(self):
        """Confirm specification fo Basic Topic."""
        # Setup
        target = SBASE.g_spec_basic
        TITLE = 'Basic Topic'
        # Test
        assert isinstance(target, SBASE.Base)
        assert TITLE == target.title.text

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (SBASE.NameSpec, BUI.ModelTextMarkup),
        (SBASE.PageAssist, Gtk.Box),
        (SBASE.SummarySpec, BUI.ModelTextStyled),
        (SBASE.TitleSpec, BUI.ModelTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
