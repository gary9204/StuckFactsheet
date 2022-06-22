"""
Unit tests for base classes for topic specification.  See
:class:`~.spec.base_s.Base`.

.. include:: /test/refs_include_pytest.txt
"""
import pytest
import gi   # type: ignore[import]
from gi.repository import GObject as GO  # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.control.control_topic as CTOPIC
import factsheet.spec.base_s as SBASE
import factsheet.view.view_markup as VMARKUP

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


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


class TestBase:
    """Unit tests for :class:`~.spec.base_s.Base`."""

    @pytest.mark.parametrize('ID_DIRECTION, TEXT_DIRECTION', [
        ('id_after', 'after'),
        ('id_before', 'before'),
        ('id_child', 'as child of'),
        ])
    def test_direction(self, ID_DIRECTION, TEXT_DIRECTION):
        """Confirm definition of placement direction constants.

        :param ID_DIRECTION: key for direction under text.
        :param TEXT_DIRECTION: text for direction under test.
        """
        # Setup
        # Test
        assert TEXT_DIRECTION == SBASE.Base.DIRECTION[ID_DIRECTION]

    @pytest.mark.skip(reason='pending completion of delegates')
    def test_call(self, new_identity_spec, monkeypatch):
        """Confirm orchestration for topic creation and placement.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        ui_view_topics = control_sheet.new_view_topics()
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        target.add_pages(assistant, ui_view_topics)

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

        def patch_add_pages(self, p_assistant, p_ui_view_outline):
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
        target(ui_view_topics)
        assert called_new_assistant
        assert called_add_pages
        assert assistant_add_pages is assistant
        assert called_run_assistant
        assert assistant_run is assistant

    @pytest.mark.skip(reason='Changing to fields')
    def test_call_delegate(self, new_identity_spec, monkeypatch):
        """Confirm delegation of topic creation and placement.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        ui_view_topics = control_sheet.new_view_topics()
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        # target.add_pages(assistant, ui_view_topics)

        called_new_assistant = False
        called_add_pages = False
        assistant_add_pages = None
        view_add_pages = None
        called_run_assistant = False
        assistant_run = None

        def patch_new_assistant(self):
            nonlocal called_new_assistant
            called_new_assistant = True  # pylint: disable=unused-variable
            nonlocal assistant
            return assistant

        def patch_add_pages(self, p_assistant, p_ui_view_outline):
            nonlocal called_add_pages
            called_add_pages = True  # pylint: disable=unused-variable
            nonlocal assistant_add_pages
            assistant_add_pages = (  # pylint: disable=unused-variable
                p_assistant)
            nonlocal view_add_pages
            view_add_pages = (  # pylint: disable=unused-variable
                p_ui_view_outline)

        def patch_run_assistant(self, p_assistant):
            nonlocal called_run_assistant
            called_run_assistant = True  # pylint: disable=unused-variable
            nonlocal assistant_run
            assistant_run = p_assistant  # pylint: disable=unused-variable

        monkeypatch.setattr(SBASE.Base, 'new_assistant', patch_new_assistant)
        monkeypatch.setattr(SBASE.Base, 'add_pages', patch_add_pages)
        monkeypatch.setattr(SBASE.Base, 'run_assistant', patch_run_assistant)
        # Test
        target(ui_view_topics)
        assert called_new_assistant
        assert called_add_pages
        assert assistant_add_pages is assistant
        assert view_add_pages is ui_view_topics
        assert called_run_assistant
        assert assistant_run is assistant

    def test_init(self, new_identity_spec):
        """| Confirm initialization.
        | Case: defintion of attributes other than fields.

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

    @pytest.mark.parametrize('DELEGATE', [
        '_init_fields_identity',
        '_init_fields_place',
        ])
    def test_init_delegate(self, monkeypatch, new_identity_spec, DELEGATE):
        """| Confirm initialization.
        | Case: delegation of field definitions.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param DELEGATE: method delegated to define attribute(s).
        """
        # Setup
        called_delegate = False

        def patch_delegate(self):
            nonlocal called_delegate
            called_delegate = True  # pylint: disable=unused-variable

        monkeypatch.setattr(SBASE.Base, DELEGATE, patch_delegate)
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        _target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assert called_delegate

    @pytest.mark.parametrize('FIELD, CLASS, CONTENT', [
        ('_field_name', CTOPIC.Name, ''),
        ('_field_summary', CTOPIC.Summary, ''),
        ('_field_title', CTOPIC.Title, ''),
        ])
    def test_init_fields_identity(
            self, new_identity_spec, FIELD, CLASS, CONTENT):
        """| Confirm initialization.
        | Case: delegated definitions of topic identity fields.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param FIELD: name of field under test.
        :param CLASS: class expected for field.
        :param CONTENT: content expected for field.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        field = getattr(target, FIELD)
        assert isinstance(field, CLASS)
        assert CONTENT == field.text

    @pytest.mark.parametrize('FIELD, CLASS, CONTENT', [
        ('_field_anchor', type(None), None),
        ('_field_direction', type(None), None),
        ])
    def test_init_fields_place(
            self, new_identity_spec, FIELD, CLASS, CONTENT):
        """| Confirm initialization.
        | Case: delegated definitions of topic place fields.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param FIELD: name of field under test.
        :param CLASS: class expected for field.
        :param CONTENT: content expected for field.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        # Test
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        field = getattr(target, FIELD)
        assert isinstance(field, CLASS)
        assert CONTENT == field

    @pytest.mark.parametrize('FIELD, CONTENT', [
        ('_field_name', ''),
        ('_field_summary', ''),
        ('_field_title', ''),
        ])
    def test_reset_fields_identity(self, new_identity_spec, FIELD, CONTENT):
        """Confirm topic identity fields reset to initial values.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param FIELD: name of field under test.
        :param CONTENT: content expected for field.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        field = getattr(target, FIELD)
        field.text = 'Oops'
        # Test
        target._reset_fields_identity()
        assert CONTENT == field.text

    @pytest.mark.parametrize('FIELD, CHANGE, EXPECT', [
        ('_field_anchor', Gtk.TreeIter(), None),
        ('_field_direction', 'Oops', None),
        ])
    def test_reset_fields_place(
            self, new_identity_spec, FIELD, CHANGE, EXPECT):
        """Confirm topic place fields reset to initial values.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param FIELD: name of field under test.
        :param CHANGE: content distinct from initial field content.
        :param EXPECT: content expected for field.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        setattr(target, FIELD, CHANGE)
        # Test
        target._reset_fields_place()
        assert EXPECT == getattr(target, FIELD)

    @pytest.mark.skip(reason='Changing to fields')
    @pytest.mark.parametrize('I_PAGE, TITLE', [
        (0, 'Introduction'),
        (1, 'Identify'),
        (3, 'Confirm'),
        ])
    def test_add_pages(self, new_identity_spec, I_PAGE, TITLE):
        """Confirm pages added to assistant.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param I_PAGE: index of page in assistant.
        :param TITLE: assistant's title for page.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        ui_view_topics = control_sheet.new_view_topics()
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        N_PAGES = 4
        # Test
        target.add_pages(assistant, ui_view_topics)
        page = assistant.get_nth_page(I_PAGE)
        assert TITLE == assistant.get_page_title(page)
        assert N_PAGES == assistant.get_n_pages()

    @pytest.mark.parametrize('METHOD, TITLE, TYPE, COMPLETE', [
        ('append_page_intro',
            'Introduction', Gtk.AssistantPageType.INTRO, True),
        ('append_page_identify',
            'Identify', Gtk.AssistantPageType.CONTENT, True),
        # ('append_page_confirm',
        #     'Confirm', Gtk.AssistantPageType.CONFIRM, True),
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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

    @pytest.mark.skip(reason='Changing to fields')
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

        # control_sheet = CSHEET.ControlSheet(p_path=None)
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

    @pytest.mark.skip(reason='Changing to fields')
    def test_new_page_confirm_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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

    @pytest.mark.skip(reason='Changing to fields')
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

        # control_sheet = CSHEET.ControlSheet(p_path=None)
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

    @pytest.mark.skip(reason='Changing to fields')
    def test_new_page_identify_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        # Test
        new_page = target.new_page_intro()
        assert isinstance(new_page, SBASE.PageAssist)

    @pytest.mark.skip(reason='Next')
    def test_new_page_place_sites(self, monkeypatch, new_identity_spec):
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

        control_sheet = CSHEET.ControlSheet(p_path=None)
        ui_view_topics = control_sheet.new_view_topics()
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
        new_page = target.new_page_place(control_sheet)
        children = new_page.get_children()
        for index in range(len(sites)):
            site = children[index]
            view = site.get_children()[FIRST]
            assert view is sites[index]

    @pytest.mark.skip(reason='Next')
    def test_new_page_place_parse(self, new_identity_spec):
        """Confirm builder can parse page description.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
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
        new_page = target.new_page_place(control_sheet)
        assert isinstance(new_page, SBASE.PageAssist)

    @pytest.mark.parametrize('ID_DIRECTION, TEXT_DIRECTION', [
        ('id_after', 'after'),
        ('id_before', 'before'),
        ('id_child', 'as child of'),
        ])
    def test_new_chooser_direction(
            self, new_identity_spec, ID_DIRECTION, TEXT_DIRECTION):
        """Confirm initialization.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param ID_DIRECTION: key for direction under test.
        :param TEXT_DIRECTION: text for direction under test.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        TEXT_ACTIVE = 'after'
        # Test
        chooser = target._new_chooser_direction()
        assert isinstance(chooser, SBASE.ChooserDirection)
        assert TEXT_ACTIVE == chooser.get_active_text()
        assert chooser.set_active_id(ID_DIRECTION)
        assert TEXT_DIRECTION == chooser.get_active_text()

    @pytest.mark.parametrize(
        'NAME_DISPLAY, NAME_EDITOR, NAME_MODEL, NAME_METHOD, EXPECT_TYPE', [
            ('FactoryDisplayName', 'FactoryEditorName', '_field_name',
             '_new_markup_name', 'Name'),
            ('FactoryDisplayTitle', 'FactoryEditorTitle', '_field_title',
             '_new_markup_title', 'Title'),
        ])
    def test_new_markup(self, monkeypatch, new_identity_spec,
                        NAME_DISPLAY, NAME_EDITOR, NAME_MODEL,
                        NAME_METHOD, EXPECT_TYPE):
        """Confirm return of visual element to markup a topic name.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        :param NAME_DISPLAY: name of display factory class.
        :param NAME_EDITOR: name of editor factory class
        :param NAME_MODEL: name of model attribute.
        :param NAME_METHOD: name of method under test.
        :param EXPECT_TYPE: expected markup type.
        """
        # Setup
        EXPECT_DISPLAY = Gtk.Label()
        EXPECT_EDITOR = Gtk.Label()

        class PatchCalls:
            def __init__(self):
                self.display = None
                self.editor = None
                self.model_display = None
                self.model_editor = None
                self.type = None

            def call_display(self):
                return EXPECT_DISPLAY

            def call_editor(self):
                return EXPECT_EDITOR

            def init_display(self, p_model):
                self.model_display = p_model

            def init_editor(self, p_model):
                self.model_editor = p_model

            def init_markup(self, p_display, p_editor, p_type):
                self.display = p_display
                self.editor = p_editor
                self.type = p_type

        patch_calls = PatchCalls()
        form_init = 'factsheet.control.control_topic.{}.__init__'
        form_call = 'factsheet.control.control_topic.{}.__call__'
        monkeypatch.setattr(
            form_init.format(NAME_DISPLAY), patch_calls.init_display)
        monkeypatch.setattr(
            form_call.format(NAME_DISPLAY), patch_calls.call_display)
        monkeypatch.setattr(
            form_init.format(NAME_EDITOR), patch_calls.init_editor)
        monkeypatch.setattr(
            form_call.format(NAME_EDITOR), patch_calls.call_editor)
        monkeypatch.setattr(
            VMARKUP.ViewMarkup, '__init__', patch_calls.init_markup)

        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        model = getattr(target, NAME_MODEL)
        method = getattr(target, NAME_METHOD)
        # Test
        result = method(model)
        assert patch_calls.model_display is model
        assert patch_calls.model_editor is model
        assert isinstance(result, VMARKUP.ViewMarkup)
        assert patch_calls.display is EXPECT_DISPLAY
        assert patch_calls.editor is EXPECT_EDITOR
        assert patch_calls.type == EXPECT_TYPE

    def test_on_apply(self, new_identity_spec):
        """Confirm assistant hidden and response set.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        # control_sheet = CSHEET.ControlSheet(p_path=None)
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        assistant = target.new_assistant()
        # assistant.show()
        # Test
        target.on_apply(assistant)
        # assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.APPLY

    def test_on_change_direction(self, new_identity_spec):
        """Confirm assistant hidden and response set.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        NAME_SPEC, SUMMARY_SPEC, TITLE_SPEC = new_identity_spec()
        target = SBASE.Base(
            p_name=NAME_SPEC, p_summary=SUMMARY_SPEC, p_title=TITLE_SPEC)
        chooser = target._new_chooser_direction()
        ID_ACTIVE = 'id_child'
        chooser.set_active_id(ID_ACTIVE)
        # Test
        target.on_change_direction(chooser)
        assert ID_ACTIVE == target._field_direction

    def test_on_cancel(self, new_identity_spec):
        """Confirm assistant hidden and response set.

        :param new_identity_spec: fixture :func:`.new_identity_spec`.
        """
        # Setup
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        # control_sheet = CSHEET.ControlSheet(p_path=None)
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
        (SBASE.ChooserDirection, Gtk.ComboBoxText),
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
