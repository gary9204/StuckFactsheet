"""
Defines base classes for topic specification.
"""
# import abc
import gi   # type: ignore[import]
import logging
import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.control.control_topic as CTOPIC
import factsheet.view.outline_id as VOUTLINE_ID
import factsheet.view.ui as UI
import factsheet.view.view_markup as VMARKUP

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]   # noqa: E402

logger = logging.getLogger('Main.SBASE')

ChooserDirection = typing.Union[Gtk.ComboBoxText]
NameSpec = BUI.ModelTextMarkup
PageAssist = typing.Union[Gtk.Box]
SummarySpec = BUI.ModelTextStyled
TitleSpec = BUI.ModelTextMarkup

ViewDuoName = typing.Union[Gtk.Box]


class FieldTextMarkup:
    """Specification field for text with markup."""

    def __init__(self, p_name_field: str) -> None:
        """Initialize topic name field and view factories.

        :param p_name_field: field name as shown to user.
        """
        self._name_field = p_name_field
        self._model = BUI.ModelTextMarkup(p_text='')
        self._factory_display = (
            BUI.FactoryDisplayTextMarkup(p_model=self._model))
        self._factory_editor = (
            BUI.FactoryEditorTextMarkup(p_model=self._model))

    @property
    def model(self) -> BUI.ModelTextMarkup:
        """Return field model."""
        return self._model

    def new_display(self) -> BUI.DisplayTextMarkup:
        """Return visual element to display field."""
        return self._factory_display()

    def new_editor(self) -> BUI.EditorTextMarkup:
        """Return visual element to edit field."""
        return self._factory_editor()

    def new_view_duo(self) -> ViewDuoName:
        """Return visual element combining both display and editor."""
        pass
        # display = self.new_display()
        # editor = self.new_editor()
        # markup = VMARKUP.ViewMarkup(display, editor, 'Name')
        # return markup.ui_view


class ManifestIdentify:
    """Fields :class:`.Base` uses to identify new topic."""

    def __init__(self):
        """Initialize identification fields"""
        self._name = CTOPIC.Name(p_text='')
        self._summary = CTOPIC.Summary(p_text='')
        self._title = CTOPIC.Title(p_text='')

    @property
    def name(self) -> CTOPIC.Name:
        """Return name field."""
        return self._name

    @property
    def summary(self) -> CTOPIC.Summary:
        """Return summary field."""
        return self._summary

    @property
    def title(self) -> CTOPIC.Title:
        """Return title field."""
        return self._title


class Base:
    """Base spec for Factsheet topics.

    A spec provides a user the means to create a class of topics.  A
    spec embodies a template for the class.  It queries the user to
    complete the template for a specific topic.  The spec also queries
    the user of the location of the new topic in the Factsheet's
    outline of topics.
    """

    DIRECTION: typing.MutableMapping[str, str] = dict(
        id_after='after',
        id_before='before',
        id_child='as child of',
        )

    def __call__(self, p_control_sheet: CSHEET.ControlSheet) -> None:
        """Orchestrate creation and placement of new topic.

        The user completes fields in the specification to create a topic.
        The user may confirm or cancel the topic.

        :param p_control_sheet: sheet in which to place new topic.
        """
        assist = self.new_assistant()
        self.add_pages(assist, p_control_sheet)
        self.run_assistant(p_assistant=assist)
        # construct topic (or exit)
        # place topic (or exit)
        # Issue #245: patch pending completion of assistant
        logger.info('New Topic')
        logger.info('Name:    {}'.format(self._field_name.text))
        logger.info('Summary: {}'.format(self._field_summary.text))
        logger.info('Title:   {}'.format(self._field_title.text))
        response = 'None'
        if self._response is not None:
            response = self._response.value_name
        logger.info('Response: {}'.format(response))

    def __init__(self, *, p_name: str, p_summary: str, p_title: str) -> None:
        """Initialize spec identity and topic identity including location.

        :param p_name: name of specification.
        :param p_summary: description of specification.
        :param p_title: descriptive title for specification.
        """
        self._name_spec = NameSpec(p_text=p_name)
        self._summary_spec = SummarySpec(p_text=p_summary)
        self._title_spec = TitleSpec(p_text=p_title)
        self._response: typing.Optional[Gtk.ResponseType] = None

        self._init_fields_identity()
        self._init_fields_place()

    def _init_fields_identity(self):
        """Initialize topic name, summary, and title fields."""
        self._field_name = CTOPIC.Name(p_text='')
        self._field_summary = CTOPIC.Summary(p_text='')
        self._field_title = CTOPIC.Title(p_text='')

    def _init_fields_place(self):
        """Initialize anchor and direction of place for new topic."""
        self._field_anchor: BUI.LineOutline = None
        self._field_direction: str = None

    def _reset_fields_identity(self):
        """Reset topic name, summary, and title fields to initial values."""
        self._field_name.text = ''
        self._field_summary.text = ''
        self._field_title.text = ''

    def _reset_fields_place(self):
        """Reset anchor and direction of place to initial values."""
        self._field_anchor = None
        self._field_direction = None

    def _init_name_topic(self) -> None:
        """ Initialize attributes for a topic name and view factories."""
        self._field_name = CTOPIC.Name(p_text='')
        self._new_display_name_topic = (
            CTOPIC.FactoryDisplayName(p_model=self._field_name))
        self._new_editor_name_topic = (
            CTOPIC.FactoryEditorName(p_model=self._field_name))

    def _init_summary_topic(self) -> None:
        """ Initialize attributes for a topic summary and view factories."""
        self._field_summary = CTOPIC.Summary(p_text='')
        self._new_display_summary_topic = (
            CTOPIC.FactoryDisplaySummary(p_model=self._field_summary))
        self._new_editor_summary_topic = (
            CTOPIC.FactoryEditorSummary(p_model=self._field_summary))

    def _init_title_topic(self) -> None:
        """ Initialize attributes for a topic title and view factories."""
        self._field_title = CTOPIC.Title(p_text='')
        self._new_display_title_topic = (
            CTOPIC.FactoryDisplayTitle(p_model=self._field_title))
        self._new_editor_title_topic = (
            CTOPIC.FactoryEditorTitle(p_model=self._field_title))

    def add_pages(self, p_assistant: Gtk.Assistant,
                  p_control_sheet: CSHEET.ControlSheet) -> None:
        """Add pages to assistant.

        :param p_assistant: assistant to populate.
        :param p_control_sheet: sheet in which to place new topic.
        """
        self.append_page_intro(p_assistant)
        self.append_page_identify(p_assistant)
        self.append_page_place(p_assistant, p_control_sheet)
        self.append_page_confirm(p_assistant)

    def append_page_confirm(self, p_assistant: Gtk.Assistant) -> None:
        """Append confirmation page to assistant.

        :param p_assistant: assistant to append to.
        """
        # confirm_display_name = self._new_display_name_topic()
        factory_display_name = CTOPIC.FactoryDisplayName(
            p_model=self._field_name)
        confirm_display_name = factory_display_name()
        # confirm_display_summary = self._new_display_summary_topic()
        factory_display_summary = CTOPIC.FactoryDisplaySummary(
            p_model=self._field_summary)
        confirm_display_summary = factory_display_summary()
        # confirm_display_title = self._new_display_title_topic()
        factory_display_title = CTOPIC.FactoryDisplayTitle(
            p_model=self._field_title)
        confirm_display_title = factory_display_title()
        page_confirm = self.new_page_confirm(confirm_display_name,
                                             confirm_display_summary,
                                             confirm_display_title)
        _i_new = p_assistant.append_page(page_confirm)
        p_assistant.set_page_title(page_confirm, 'Confirm')
        p_assistant.set_page_type(page_confirm, Gtk.AssistantPageType.CONFIRM)
        p_assistant.set_page_complete(page_confirm, True)

    def append_page_identify(self, p_assistant: Gtk.Assistant) -> None:
        """Append identify page to assistant.

        :param p_assistant: assistant to append to.
        """
        identify_view_name = self._new_markup_name(self._field_name)
        new_editor_summary = CTOPIC.FactoryEditorSummary(
            p_model=self._field_summary)
        identify_editor_summary = new_editor_summary()
        identify_view_title = self._new_markup_title(self._field_title)
        page_identify = self.new_page_identify(
            identify_view_name, identify_editor_summary, identify_view_title)
        _i_new = p_assistant.append_page(page_identify)
        p_assistant.set_page_title(page_identify, 'Identify')
        p_assistant.set_page_type(page_identify, Gtk.AssistantPageType.CONTENT)
        p_assistant.set_page_complete(page_identify, True)

    def append_page_intro(self, p_assistant: Gtk.Assistant) -> None:
        """Append introduction page to assistant.

        :param p_assistant: assistant to append to.
        """
        page_intro = self.new_page_intro()
        _i_new = p_assistant.append_page(page_intro)
        p_assistant.set_page_title(page_intro, 'Introduction')
        p_assistant.set_page_type(page_intro, Gtk.AssistantPageType.INTRO)
        p_assistant.set_page_complete(page_intro, True)

    def append_page_place(self, p_assistant: Gtk.Assistant,
                          p_control_sheet: CSHEET.ControlSheet) -> None:
        """Append place page to assistant.

        :param p_assistant: assistant to append to.
        :param p_control_sheet: sheet in which to place new topic.
        """
        page_place = self.new_page_place(p_control_sheet)
        _i_new = p_assistant.append_page(page_place)
        p_assistant.set_page_title(page_place, 'Place')
        p_assistant.set_page_type(page_place, Gtk.AssistantPageType.CONTENT)
        p_assistant.set_page_complete(page_place, True)

    @property
    def name(self) -> NameSpec:
        """Return spec name."""
        return self._name_spec

    def new_assistant(self) -> typing.Optional[Gtk.Assistant]:
        """Return an assistant from user interface definition."""
        get_ui_object = UI.GetUiElementByStr(p_string_ui=UI_ASSIST)
        assist = get_ui_object('ui_assistant')
        _ = assist.connect('apply', self.on_apply)
        _ = assist.connect('cancel', self.on_cancel)
        _ = assist.connect('destroy', self.on_cancel)
        _ = assist.connect('prepare', self.on_prepare)
        return assist

    def _new_chooser_direction(self) -> ChooserDirection:
        """Return visual element to choose placement direction."""
        chooser = ChooserDirection()
        for key, text in Base.DIRECTION.items():
            chooser.append(key, text)
        _ = chooser.set_active_id('id_after')
        return chooser

    def _new_markup_name(self, p_name: CTOPIC.Name) -> VMARKUP.ViewMarkup:
        """Return visual element to markup a topic name.

        :param p_name: topic name model.
        """
        factory_display = CTOPIC.FactoryDisplayName(p_model=p_name)
        display_name = factory_display()
        factory_editor = CTOPIC.FactoryEditorName(p_model=p_name)
        editor_name = factory_editor()
        markup_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        return markup_name

    def _new_markup_title(self, p_title: CTOPIC.Title) -> VMARKUP.ViewMarkup:
        """Return visual element to markup a topic title.

        :param p_title: topic title model.
        """
        factory_display = CTOPIC.FactoryDisplayTitle(p_model=p_title)
        factory_editor = CTOPIC.FactoryEditorTitle(p_model=p_title)
        display_title = factory_display()
        editor_title = factory_editor()
        markup_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        return markup_title

    def new_page_confirm(self, p_display_name: CTOPIC.DisplayName,
                         p_display_summary: CTOPIC.DisplaySummary,
                         p_display_title: CTOPIC.DisplayTitle) -> PageAssist:
        """Return a confirmation page.

        :param p_display_name: display for topic name.
        :param p_display_summary: display for topic summary.
        :param p_display_title: display for topic title.
        """
        get_ui_object = UI.GetUiElementByStr(p_string_ui=UI_PAGE_CONFIRM)
        new_page = get_ui_object('ui_page_confirm')
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_name = get_ui_object('ui_confirm_site_name')
        site_name.pack_start(p_display_name, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        site_summary = get_ui_object('ui_confirm_site_summary')
        site_summary.add(p_display_summary)
        site_title = get_ui_object('ui_confirm_site_title')
        site_title.pack_start(
            p_display_title, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        return new_page

    def new_page_identify(self, p_view_name: VMARKUP.ViewMarkup,
                          p_editor_summary: CTOPIC.EditorSummary,
                          p_view_title: VMARKUP.ViewMarkup) -> PageAssist:
        """Return an identification page.

        :param p_view_name: view to display and edit topic name.
        :param p_editor_summary: view to display and edit topic summary.
        :param p_view_title: view to display and edit topic title.
        """
        get_ui_object = UI.GetUiElementByStr(p_string_ui=UI_PAGE_IDENTIFY)
        new_page = get_ui_object('ui_page_identify')
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_name = get_ui_object('ui_identify_site_name')
        site_name.pack_start(
            p_view_name.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        site_summary = get_ui_object('ui_identify_site_summary')
        site_summary.add(p_editor_summary)
        site_title = get_ui_object('ui_identify_site_title')
        site_title.pack_start(
            p_view_title.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)
        return new_page

    def new_page_intro(self) -> PageAssist:
        """Return an introduction page."""
        get_ui_object = UI.GetUiElementByStr(p_string_ui=UI_PAGE_INTRO)
        new_page = get_ui_object('ui_page_intro')
        return new_page

    def new_page_place(
            self, p_control_sheet: CSHEET.ControlSheet) -> PageAssist:
        """Return a topic place page.

        :param p_control_sheet: sheet in which to place new topic.
        """
        get_ui_object = UI.GetUiElementByStr(p_string_ui=UI_PAGE_PLACE)
        new_page = get_ui_object('ui_page_place')
        ui_choose_direction = self._new_chooser_direction()
        ui_choose_direction.connect('changed', self.on_change_direction)
        site_direction = get_ui_object('ui_place_site_direction')
        site_direction.add(ui_choose_direction)
        ui_view_outline = p_control_sheet.new_view_topics()
        selector_anchor = VOUTLINE_ID.SelectorItem(ui_view_outline)
        site_oultine = get_ui_object('ui_place_site_outline')
        site_oultine.add(selector_anchor.ui_selector)
        # EXPAND_OKAY = True
        # FILL_OKAY = True
        # N_PADDING = 6
        # site_place = get_ui_object('ui_place_site_place')
        # site_place.pack_start(
        #     Gtk.Label(label=' Picker '), EXPAND_OKAY, FILL_OKAY, N_PADDING)
        # site_topics = get_ui_object('ui_site_display_topics')
        # site_topics.add(Gtk.Label(label='Topics'))
        # site_summary = get_ui_object('ui_site_summary')
        # site_summary.add(Gtk.Label(label='Summary'))
        return new_page

    def on_apply(self, p_assistant: Gtk.Assistant) -> None:
        """Hide assistant and record user confirmed new topic.

        Recording user's response unblocks call method.
        """
        del p_assistant  # Unused in base method
        self._response = Gtk.ResponseType.APPLY

    def on_change_direction(self, p_chooser: ChooserDirection) -> None:
        """Update placement direction when user makes a choice.

        :param p_chooser: visual element for choosing placement direction.
        """
        self._field_direction = p_chooser.get_active_id()

    def on_cancel(self, p_assistant: Gtk.Assistant) -> None:
        """Hide assistant and record user cancelled new topic.

        Recording user's response unblocks call method.
        """
        del p_assistant  # Unused in base method
        self._response = Gtk.ResponseType.CANCEL

    def on_prepare(self, p_assistant: Gtk.Assistant, p_page: PageAssist,
                   **_kwargs) -> None:
        """Prepare page contents for presentation in assistant.

        :param p_assistant: assistant presenting page.
        :param p_page: page to present.
        """
        del p_assistant  # Unused in base method
        p_page.show_all()

    def run_assistant(self, p_assistant: Gtk.Assistant) -> None:
        """Present assistant to the user and wait for user's responses.

        The user navigates the assistant and fills in assistant's
        fields.  The user may confirm or cancel their selections.

        :param p_assistant: assistant to present.
        """
        self._response = None
        p_assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()
        p_assistant.hide()

    @property
    def summary(self) -> SummarySpec:
        """Return spec summary."""
        return self._summary_spec

    @property
    def title(self) -> TitleSpec:
        """Return spec title."""
        return self._title_spec


g_spec_basic = Base(
    p_name='Basic',
    p_summary=('Lets you customize the Topics outline of a Factsheet. '
               'A Basic topic has a name, title, and summary, but no facts. '
               'Specify a Basic topic to add a note to the Topics outline. '
               'Also, you may group topics within the outline by adding a '
               'Basic topic and then adding or moving topics underneath it. '
               ),
    p_title='Basic Topic')


UI_ASSIST = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Generated with glade 3.22.1 -->
    <interface>
      <requires lib="gtk+" version="3.20"/>
      <object class="GtkAssistant" id="ui_assistant">
        <property name="can_focus">False</property>
        <property name="modal">True</property>
        <property name="window_position">mouse</property>
        <property name="default_width">350</property>
        <property name="default_height">450</property>
        <property name="use_header_bar">1</property>
        <child>
          <placeholder/>
        </child>
      </object>
    </interface>
    """


UI_PAGE_CONFIRM = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!-- Generated with glade 3.22.1 -->\n'
    '<interface>\n'
    '  <requires lib="gtk+" version="3.20"/>\n'
    '  <object class="GtkBox" id="ui_page_confirm">\n'
    '    <property name="width_request">500</property>\n'
    '    <property name="visible">True</property>\n'
    '    <property name="can_focus">False</property>\n'
    '    <property name="margin_top">6</property>\n'
    '    <property name="margin_bottom">6</property>\n'
    '    <property name="orientation">vertical</property>\n'
    '    <property name="spacing">6</property>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">start</property>\n'
    '        <property name="label" translatable="yes">Click '
    '&lt;b&gt;Apply&lt;/b&gt; to accept the topic information below or '
    '&lt;b&gt;Back&lt;/b&gt; to change the information.</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '        <property name="max_width_chars">60</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">0</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkGrid">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="row_spacing">6</property>\n'
    '        <property name="column_spacing">12</property>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="label" translatable="yes">'
    '&lt;i&gt;Name:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">right</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="label" translatable="yes">'
    '&lt;i&gt;Title:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">right</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkBox" id="ui_confirm_site_name">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="orientation">vertical</property>\n'
    '            <child>\n'
    '              <placeholder/>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkBox" id="ui_confirm_site_title">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="orientation">vertical</property>\n'
    '            <child>\n'
    '              <placeholder/>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">1</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">center</property>\n'
    '        <property name="label" translatable="yes">'
    '&lt;i&gt;Content&lt;/i&gt;</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">2</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkScrolledWindow" '
    'id="ui_confirm_site_summary">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">True</property>\n'
    '        <property name="shadow_type">in</property>\n'
    '        <child>\n'
    '          <placeholder/>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">True</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">3</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">center</property>\n'
    '        <property name="label" translatable="yes">'
    '&lt;i&gt;Location&lt;/i&gt;</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">4</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkBox">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="orientation">vertical</property>\n'
    '        <child>\n'
    '          <object class="GtkFrame">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="label_xalign">'
    '0.10000000149011612</property>\n'
    '            <property name="shadow_type">in</property>\n'
    '            <child>\n'
    '              <object class="GtkScrolledWindow" '
    'id="ui_confirm_site_topics">\n'
    '                <property name="visible">True</property>\n'
    '                <property name="can_focus">True</property>\n'
    '                <property name="margin_bottom">6</property>\n'
    '                <property name="shadow_type">in</property>\n'
    '                <property name="min_content_height">120</property>\n'
    '                <child>\n'
    '                  <placeholder/>\n'
    '                </child>\n'
    '              </object>\n'
    '            </child>\n'
    '            <child type="label">\n'
    '              <object class="GtkLabel">\n'
    '                <property name="visible">True</property>\n'
    '                <property name="can_focus">False</property>\n'
    '                <property name="label" '
    'translatable="yes">&lt;i&gt;Topics&lt;/i&gt;</property>\n'
    '                <property name="use_markup">True</property>\n'
    '              </object>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="expand">False</property>\n'
    '            <property name="fill">True</property>\n'
    '            <property name="position">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkSearchBar" id="ui_confirm_search_bar">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="search_mode_enabled">True</property>\n'
    '            <child>\n'
    '              <object class="GtkBox">\n'
    '                <property name="visible">True</property>\n'
    '                <property name="can_focus">False</property>\n'
    '                <child>\n'
    '                  <object class="GtkCheckButton" '
    'id="ui_search_by_name">\n'
    '                    <property name="label" '
    'translatable="yes">By name</property>\n'
    '                    <property name="visible">True</property>\n'
    '                    <property name="can_focus">True</property>\n'
    '                    <property name="receives_default">False</property>\n'
    '                    <property name="active">True</property>\n'
    '                    <property name="draw_indicator">True</property>\n'
    '                  </object>\n'
    '                  <packing>\n'
    '                    <property name="expand">False</property>\n'
    '                    <property name="fill">True</property>\n'
    '                    <property name="position">0</property>\n'
    '                  </packing>\n'
    '                </child>\n'
    '                <child>\n'
    '                  <object class="GtkCheckButton" '
    'id="ui_search_by_title">\n'
    '                    <property name="label" translatable="yes">By '
    'title</property>\n'
    '                    <property name="visible">True</property>\n'
    '                    <property name="can_focus">True</property>\n'
    '                    <property name="receives_default">False</property>\n'
    '                    <property name="active">True</property>\n'
    '                    <property name="draw_indicator">True</property>\n'
    '                  </object>\n'
    '                  <packing>\n'
    '                    <property name="expand">False</property>\n'
    '                    <property name="fill">True</property>\n'
    '                    <property name="position">1</property>\n'
    '                  </packing>\n'
    '                </child>\n'
    '                <child>\n'
    '                  <object class="GtkSearchEntry" id="ui_search_entry1">\n'
    '                    <property name="visible">True</property>\n'
    '                    <property name="can_focus">True</property>\n'
    '                    <property name="width_chars">25</property>\n'
    '                    <property name="primary_icon_name">'
    'edit-find-symbolic</property>\n'
    '                    <property name="primary_icon_activatable">'
    'False</property>\n'
    '                    <property name="primary_icon_sensitive">'
    'False</property>\n'
    '                  </object>\n'
    '                  <packing>\n'
    '                    <property name="expand">True</property>\n'
    '                    <property name="fill">True</property>\n'
    '                    <property name="position">2</property>\n'
    '                  </packing>\n'
    '                </child>\n'
    '              </object>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="expand">False</property>\n'
    '            <property name="fill">True</property>\n'
    '            <property name="position">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">5</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '  </object>\n'
    '</interface>\n'
    )

UI_PAGE_IDENTIFY = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!-- Generated with glade 3.22.1 -->\n'
    '<interface>\n'
    '  <requires lib="gtk+" version="3.20"/>\n'
    '  <object class="GtkBox" id="ui_page_identify">\n'
    '    <property name="width_request">500</property>\n'
    '    <property name="visible">True</property>\n'
    '    <property name="can_focus">False</property>\n'
    '    <property name="margin_top">6</property>\n'
    '    <property name="margin_bottom">6</property>\n'
    '    <property name="orientation">vertical</property>\n'
    '    <property name="spacing">6</property>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">start</property>\n'
    '        <property name="label" '
    'translatable="yes">Enter a name, a title, and summary for the new '
    'topic </property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '        <property name="max_width_chars">60</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">0</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkGrid">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="margin_top">6</property>\n'
    '        <property name="margin_bottom">6</property>\n'
    '        <property name="row_spacing">6</property>\n'
    '        <property name="column_spacing">12</property>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Name:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Title:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Summary:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">2</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">start</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" translatable="yes">short identifier '
    'for the topic.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">start</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" translatable="yes">one-line '
    'description of the topic.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">start</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" translatable="yes">description of '
    'topic that adds detail to title.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">2</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">1</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkGrid">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="row_spacing">6</property>\n'
    '        <property name="column_spacing">12</property>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">center</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;b&gt;Name:&lt;/b&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">right</property>\n'
    '            <property name="wrap">True</property>\n'
    '            <property name="width_chars">6</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">center</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;b&gt;Title:&lt;/b&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">right</property>\n'
    '            <property name="wrap">True</property>\n'
    '            <property name="width_chars">6</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkBox" id="ui_identify_site_name">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="orientation">vertical</property>\n'
    '            <child>\n'
    '              <placeholder/>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkBox" id="ui_identify_site_title">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="orientation">vertical</property>\n'
    '            <child>\n'
    '              <placeholder/>\n'
    '            </child>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">2</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="margin_top">6</property>\n'
    '        <property name="label" '
    'translatable="yes">&lt;b&gt;Summary&lt;/b&gt;</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">3</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkScrolledWindow" id="ui_identify_site_summary">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">True</property>\n'
    '        <property name="shadow_type">in</property>\n'
    '        <property name="min_content_height">60</property>\n'
    '        <child>\n'
    '          <placeholder/>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">True</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">4</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '  </object>\n'
    '</interface>\n'
)


UI_PAGE_INTRO = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!-- Generated with glade 3.22.1 -->\n'
    '<interface>\n'
    '  <requires lib="gtk+" version="3.20"/>\n'
    '  <object class="GtkBox" id="ui_page_intro">\n'
    '    <property name="width_request">500</property>\n'
    '    <property name="visible">True</property>\n'
    '    <property name="can_focus">False</property>\n'
    '    <property name="margin_top">6</property>\n'
    '    <property name="margin_bottom">6</property>\n'
    '    <property name="orientation">vertical</property>\n'
    '    <property name="spacing">6</property>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">start</property>\n'
    '        <property name="valign">start</property>\n'
    '        <property name="label" translatable="yes">Use this assistant '
    'to add a basic topic to the &lt;i&gt;Topics &lt;/i&gt;outline. You '
    'may use a basic topic to add a note or group topics within the '
    'outline. To group topics, add a basic topic and then add or move '
    'topics underneath it. The steps for adding a basic topic are as '
    'follows.</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">0</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkGrid">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="row_spacing">6</property>\n'
    '        <property name="column_spacing">12</property>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Identify:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Confirm:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="wrap">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">2</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="label" translatable="yes">Customize '
    'identification information for the new topic.  A topic is identified '
    'by the name, title, and summary that you enter.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '            <property name="max_width_chars">50</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">0</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">start</property>\n'
    '            <property name="label" translatable="yes">Confirm the '
    'topic information is correct.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '            <property name="max_width_chars">50</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">2</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">end</property>\n'
    '            <property name="valign">start</property>\n'
    '            <property name="label" '
    'translatable="yes">&lt;i&gt;Place:&lt;/i&gt;</property>\n'
    '            <property name="use_markup">True</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">0</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '        <child>\n'
    '          <object class="GtkLabel">\n'
    '            <property name="visible">True</property>\n'
    '            <property name="can_focus">False</property>\n'
    '            <property name="halign">start</property>\n'
    '            <property name="label" translatable="yes">Pick location '
    'in the the &lt;i&gt;Topics &lt;/i&gt;outline for new topic.</property>\n'
    '            <property name="use_markup">True</property>\n'
    '            <property name="justify">fill</property>\n'
    '            <property name="wrap">True</property>\n'
    '            <property name="max_width_chars">50</property>\n'
    '          </object>\n'
    '          <packing>\n'
    '            <property name="left_attach">1</property>\n'
    '            <property name="top_attach">1</property>\n'
    '          </packing>\n'
    '        </child>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">1</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '    <child>\n'
    '      <object class="GtkLabel">\n'
    '        <property name="visible">True</property>\n'
    '        <property name="can_focus">False</property>\n'
    '        <property name="halign">start</property>\n'
    '        <property name="margin_top">6</property>\n'
    '        <property name="label" '
    'translatable="yes">Click &lt;b&gt;Next &lt;/b&gt;to proceed.  '
    'Click &lt;b&gt;Cancel &lt;/b&gt;at any time to abandon the new '
    'topic.</property>\n'
    '        <property name="use_markup">True</property>\n'
    '        <property name="justify">fill</property>\n'
    '        <property name="wrap">True</property>\n'
    '      </object>\n'
    '      <packing>\n'
    '        <property name="expand">False</property>\n'
    '        <property name="fill">True</property>\n'
    '        <property name="position">2</property>\n'
    '      </packing>\n'
    '    </child>\n'
    '  </object>\n'
    '<interface>\n'
)


# UI_PAGE_PLACE = """
# <?xml version="1.0" encoding="UTF-8"?>
# <!-- Generated with glade 3.38.2 -->
# <interface>
#   <requires lib="gtk+" version="3.20"/>
#   <object class="GtkImage" id="image_find">
#     <property name="visible">True</property>
#     <property name="can-focus">False</property>
#     <property name="icon-name">edit-find-symbolic</property>
#   </object>
#   <object class="GtkBox" id="ui_page_place">
#     <property name="width-request">500</property>
#     <property name="visible">True</property>
#     <property name="can-focus">False</property>
#     <property name="margin-start">6</property>
#     <property name="margin-end">6</property>
#     <property name="margin-top">6</property>
#     <property name="margin-bottom">6</property>
#     <property name="orientation">vertical</property>
#     <property name="spacing">6</property>
#     <child>
#       <object class="GtkExpander">
#         <property name="visible">True</property>
#         <property name="can-focus">True</property>
#         <property name="resize-toplevel">True</property>
#         <child>
#           <object class="GtkBox">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="margin-top">6</property>
#             <property name="margin-bottom">6</property>
#             <property name="orientation">vertical</property>
#             <property name="spacing">6</property>
#             <child>
#               <object class="GtkLabel">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="halign">start</property>
#                 <property name="valign">start</property>
#                 <property name="label" translatable="yes">An existing topic and order determine where in the topic outline the application will place the new topic. </property>
#                 <property name="use-markup">True</property>
#                 <property name="justify">fill</property>
#                 <property name="wrap">True</property>
#               </object>
#               <packing>
#                 <property name="expand">False</property>
#                 <property name="fill">True</property>
#                 <property name="position">0</property>
#               </packing>
#             </child>
#             <child>
#               <object class="GtkLabel">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="halign">start</property>
#                 <property name="valign">start</property>
#                 <property name="label" translatable="yes">The &lt;i&gt;Topics &lt;/i&gt;table below lists the names and titles of existing topics.  Click on a row to select a topic and show its summary.</property>
#                 <property name="use-markup">True</property>
#                 <property name="justify">fill</property>
#                 <property name="wrap">True</property>
#               </object>
#               <packing>
#                 <property name="expand">False</property>
#                 <property name="fill">True</property>
#                 <property name="position">1</property>
#               </packing>
#             </child>
#             <child>
#               <object class="GtkLabel">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="halign">start</property>
#                 <property name="valign">start</property>
#                 <property name="label" translatable="yes">One of the &lt;b&gt;After&lt;/b&gt;, &lt;b&gt;Before&lt;/b&gt;, or &lt;b&gt;Child&lt;/b&gt; buttons determines the order of the new topic relative to the selected topic. Click &lt;b&gt;After &lt;/b&gt;(&lt;b&gt;Before&lt;/b&gt;) to place the new topic after (before) the selected topic. Click &lt;b&gt;Child &lt;/b&gt;to make the new topic a child of the selected topic. In this case, the new topic will appear after any children of the selected topic.</property>
#                 <property name="use-markup">True</property>
#                 <property name="justify">fill</property>
#                 <property name="wrap">True</property>
#               </object>
#               <packing>
#                 <property name="expand">False</property>
#                 <property name="fill">True</property>
#                 <property name="position">2</property>
#               </packing>
#             </child>
#             <child>
#               <object class="GtkLabel">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="halign">start</property>
#                 <property name="valign">start</property>
#                 <property name="label" translatable="yes">Click the &lt;b&gt;Find &lt;/b&gt;button below to search for text in topic name,  title, or summary fields. Select one or more fields to search by checking corresponding box(es) below the search bar.</property>
#                 <property name="use-markup">True</property>
#                 <property name="justify">fill</property>
#                 <property name="wrap">True</property>
#               </object>
#               <packing>
#                 <property name="expand">False</property>
#                 <property name="fill">True</property>
#                 <property name="position">3</property>
#               </packing>
#             </child>
#           </object>
#         </child>
#         <child type="label">
#           <object class="GtkLabel">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="label" translatable="yes">&lt;b&gt;Instructions&lt;/b&gt;</property>
#             <property name="use-markup">True</property>
#           </object>
#         </child>
#       </object>
#       <packing>
#         <property name="expand">False</property>
#         <property name="fill">True</property>
#         <property name="position">0</property>
#       </packing>
#     </child>
#     <child>
#       <object class="GtkBox" id="ui_place_site_place">
#         <property name="visible">True</property>
#         <property name="can-focus">False</property>
#         <child>
#           <object class="GtkLabel">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="label" translatable="yes">Place</property>
#           </object>
#           <packing>
#             <property name="expand">False</property>
#             <property name="fill">True</property>
#             <property name="position">0</property>
#           </packing>
#         </child>
#         <child>
#           <object class="GtkToggleButton" id="ui_button_find">
#             <property name="label" translatable="yes">Find</property>
#             <property name="visible">True</property>
#             <property name="can-focus">True</property>
#             <property name="receives-default">True</property>
#             <property name="image">image_find</property>
#             <property name="always-show-image">True</property>
#           </object>
#           <packing>
#             <property name="expand">False</property>
#             <property name="fill">True</property>
#             <property name="pack-type">end</property>
#             <property name="position">1</property>
#           </packing>
#         </child>
#         <child>
#           <placeholder/>
#         </child>
#         <child>
#           <object class="GtkLabel">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="label" translatable="yes">topic selected below</property>
#           </object>
#           <packing>
#             <property name="expand">False</property>
#             <property name="fill">True</property>
#             <property name="position">3</property>
#           </packing>
#         </child>
#       </object>
#       <packing>
#         <property name="expand">True</property>
#         <property name="fill">True</property>
#         <property name="position">1</property>
#       </packing>
#     </child>
#     <child>
#       <object class="GtkPaned">
#         <property name="visible">True</property>
#         <property name="can-focus">True</property>
#         <property name="orientation">vertical</property>
#         <property name="wide-handle">True</property>
#         <child>
#           <object class="GtkBox">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="orientation">vertical</property>
#             <child>
#               <object class="GtkFrame">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="label-xalign">0.10000000149011612</property>
#                 <property name="shadow-type">in</property>
#                 <child>
#                   <object class="GtkScrolledWindow" id="ui_site_display_topics">
#                     <property name="visible">True</property>
#                     <property name="can-focus">True</property>
#                     <property name="margin-bottom">6</property>
#                     <property name="shadow-type">in</property>
#                     <property name="min-content-height">120</property>
#                     <child>
#                       <placeholder/>
#                     </child>
#                   </object>
#                 </child>
#                 <child type="label">
#                   <object class="GtkLabel">
#                     <property name="visible">True</property>
#                     <property name="can-focus">False</property>
#                     <property name="label" translatable="yes">&lt;i&gt;Topics&lt;/i&gt;</property>
#                     <property name="use-markup">True</property>
#                   </object>
#                 </child>
#               </object>
#               <packing>
#                 <property name="expand">True</property>
#                 <property name="fill">True</property>
#                 <property name="position">0</property>
#               </packing>
#             </child>
#             <child>
#               <object class="GtkSearchBar" id="ui_search">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="hexpand">True</property>
#                 <property name="search-mode-enabled">True</property>
#                 <property name="show-close-button">True</property>
#                 <child>
#                   <object class="GtkBox">
#                     <property name="visible">True</property>
#                     <property name="can-focus">False</property>
#                     <property name="hexpand">True</property>
#                     <property name="orientation">vertical</property>
#                     <child>
#                       <object class="GtkSearchEntry" id="ui_search_entry">
#                         <property name="visible">True</property>
#                         <property name="can-focus">True</property>
#                         <property name="valign">start</property>
#                         <property name="width-chars">40</property>
#                         <property name="primary-icon-name">edit-find-symbolic</property>
#                         <property name="primary-icon-activatable">False</property>
#                         <property name="primary-icon-sensitive">False</property>
#                       </object>
#                       <packing>
#                         <property name="expand">False</property>
#                         <property name="fill">True</property>
#                         <property name="position">0</property>
#                       </packing>
#                     </child>
#                     <child>
#                       <object class="GtkBox">
#                         <property name="visible">True</property>
#                         <property name="can-focus">False</property>
#                         <property name="hexpand">True</property>
#                         <child>
#                           <object class="GtkCheckButton" id="ui_search_in_name">
#                             <property name="label" translatable="yes">In name</property>
#                             <property name="visible">True</property>
#                             <property name="can-focus">True</property>
#                             <property name="receives-default">False</property>
#                             <property name="active">True</property>
#                             <property name="draw-indicator">True</property>
#                           </object>
#                           <packing>
#                             <property name="expand">False</property>
#                             <property name="fill">True</property>
#                             <property name="position">0</property>
#                           </packing>
#                         </child>
#                         <child>
#                           <object class="GtkCheckButton" id="ui_search_in_title">
#                             <property name="label" translatable="yes">In title</property>
#                             <property name="visible">True</property>
#                             <property name="can-focus">True</property>
#                             <property name="receives-default">False</property>
#                             <property name="draw-indicator">True</property>
#                           </object>
#                           <packing>
#                             <property name="expand">False</property>
#                             <property name="fill">True</property>
#                             <property name="position">1</property>
#                           </packing>
#                         </child>
#                         <child>
#                           <object class="GtkCheckButton" id="ui_search_in_summary">
#                             <property name="label" translatable="yes">In summary</property>
#                             <property name="visible">True</property>
#                             <property name="can-focus">True</property>
#                             <property name="receives-default">False</property>
#                             <property name="draw-indicator">True</property>
#                           </object>
#                           <packing>
#                             <property name="expand">False</property>
#                             <property name="fill">True</property>
#                             <property name="position">2</property>
#                           </packing>
#                         </child>
#                       </object>
#                       <packing>
#                         <property name="expand">False</property>
#                         <property name="fill">True</property>
#                         <property name="position">1</property>
#                       </packing>
#                     </child>
#                   </object>
#                 </child>
#               </object>
#               <packing>
#                 <property name="expand">False</property>
#                 <property name="fill">True</property>
#                 <property name="position">1</property>
#               </packing>
#             </child>
#           </object>
#           <packing>
#             <property name="resize">True</property>
#             <property name="shrink">False</property>
#           </packing>
#         </child>
#         <child>
#           <object class="GtkFrame">
#             <property name="visible">True</property>
#             <property name="can-focus">False</property>
#             <property name="label-xalign">0.10000000149011612</property>
#             <property name="shadow-type">in</property>
#             <child>
#               <object class="GtkScrolledWindow" id="ui_site_summary">
#                 <property name="visible">True</property>
#                 <property name="can-focus">True</property>
#                 <property name="margin-bottom">6</property>
#                 <property name="shadow-type">in</property>
#                 <property name="min-content-height">60</property>
#                 <child>
#                   <placeholder/>
#                 </child>
#               </object>
#             </child>
#             <child type="label">
#               <object class="GtkLabel">
#                 <property name="visible">True</property>
#                 <property name="can-focus">False</property>
#                 <property name="label" translatable="yes">&lt;i&gt;Summary&lt;/i&gt;</property>
#                 <property name="use-markup">True</property>
#               </object>
#             </child>
#           </object>
#           <packing>
#             <property name="resize">True</property>
#             <property name="shrink">False</property>
#           </packing>
#         </child>
#       </object>
#       <packing>
#         <property name="expand">True</property>
#         <property name="fill">True</property>
#         <property name="position">2</property>
#       </packing>
#     </child>
#   </object>
# </interface>
# """

UI_PAGE_PLACE = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.38.2 -->
<interface>
  <requires lib="gtk+" version="3.20"/>
  <object class="GtkBox" id="ui_page_place">
    <property name="width-request">500</property>
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="margin-start">6</property>
    <property name="margin-end">6</property>
    <property name="margin-top">6</property>
    <property name="margin-bottom">6</property>
    <property name="orientation">vertical</property>
    <property name="spacing">6</property>
    <child>
      <object class="GtkExpander">
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="resize-toplevel">True</property>
        <child>
          <object class="GtkBox">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="margin-top">6</property>
            <property name="margin-bottom">6</property>
            <property name="orientation">vertical</property>
            <property name="spacing">6</property>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">An existing topic and order determine where in the topic outline the application will place the new topic. </property>
                <property name="use-markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">The &lt;i&gt;Topics &lt;/i&gt;table below lists the names and titles of existing topics.  Click on a row to select a topic and show its summary.</property>
                <property name="use-markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">One of the &lt;b&gt;After&lt;/b&gt;, &lt;b&gt;Before&lt;/b&gt;, or &lt;b&gt;Child&lt;/b&gt; buttons determines the order of the new topic relative to the selected topic. Click &lt;b&gt;After &lt;/b&gt;(&lt;b&gt;Before&lt;/b&gt;) to place the new topic after (before) the selected topic. Click &lt;b&gt;Child &lt;/b&gt;to make the new topic a child of the selected topic. In this case, the new topic will appear after any children of the selected topic.</property>
                <property name="use-markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">Click the &lt;b&gt;Find &lt;/b&gt;button below to search for text in topic name,  title, or summary fields. Select one or more fields to search by checking corresponding box(es) below the search bar.</property>
                <property name="use-markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">3</property>
              </packing>
            </child>
          </object>
        </child>
        <child type="label">
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="label" translatable="yes">&lt;b&gt;Instructions&lt;/b&gt;</property>
            <property name="use-markup">True</property>
          </object>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkBox" id="ui_place_direction">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <child>
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="label" translatable="yes">Place new topic </property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkBox" id="ui_place_site_direction">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="orientation">vertical</property>
            <child>
              <placeholder/>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="halign">start</property>
            <property name="label" translatable="yes"> topic selected below</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">1</property>
      </packing>
    </child>
    <child>
      <object class="GtkBox" id="ui_place_site_outline">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="orientation">vertical</property>
        <child>
          <placeholder/>
        </child>
      </object>
      <packing>
        <property name="expand">True</property>
        <property name="fill">True</property>
        <property name="position">2</property>
      </packing>
    </child>
  </object>
</interface>
"""
