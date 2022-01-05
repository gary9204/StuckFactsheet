"""
Defines base classes for topic specification.
"""
import abc
import gi   # type: ignore[import]
import logging
from pathlib import Path
import typing

import factsheet.bridge_ui as BUI
import factsheet.view.view_markup as VMARKUP

gi.require_version('Gtk', '3.0')
# from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.SBASE')

SUFFIX_SPEC = '.py'
SUFFIX_ASSIST = '.ui'

PageAssist = typing.Union[Gtk.Box]


class ExceptionSpec(Exception):
    """Base class for specification exceptions."""

    pass


class SpecFileError(ExceptionSpec):
    """Raise for when specification file is inaccessible."""

    pass


class UiDescriptionError(ExceptionSpec):
    """Raise for when user interface description in accessible."""

    pass


class UiObjectNotFoundError(ExceptionSpec):
    """Raise for when no object found for a given user interface ID."""

    pass


class GetUiObject(abc.ABC):
    """Get user interface element with supplemental failure information.

    `Gtk.Builder`_ aborts if there is an error opening a user interface
    description file or parsing a description.
    `Gtk.Builder.get_object()`_ returns None when the method cannot find
    the object for a given ID.  Class :class:`GetUiObject` augments
    `Gtk.Builder`_ to provide more information when a failure occurs.

    .. _`Gtk.Builder`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Builder.html

    .. _`Gtk.Builder.get_object()`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        Builder.html#Gtk.Builder.get_object
    """
    _builder: Gtk.Builder

    @abc.abstractmethod
    def __init__(self, **_kwargs) -> None:
        """Log start of user interface construction.

        Each subclass must extend this method by initializing the
        underlying builder attribute (`_builder`).
        """
        logger.debug('Building UI description ...')

    def __call__(self, p_id_ui: str) -> typing.Any:
        """Return user interface element with given ID.

        :param p_id_ui: ID of desired element.
        :raises UiObjectNotFoundError: when no element matches ID.
        """
        ui_element = self._builder.get_object(p_id_ui)
        if ui_element is None:
            MESSAGE = 'No element found for ID {}.'.format(p_id_ui)
            raise UiObjectNotFoundError(MESSAGE)
        return ui_element


class GetUiObjectPath(GetUiObject):
    """Extend :class:`.GetUiObject` with 'Gtk.Bujilder`_ from file."""

    def __init__(self, *, p_path: Path, **kwargs) -> None:
        """Initialize underlying builder and log source of description.

        :param p_path: location of user interface description file.
        :raises UiDescriptionError: when user interface description is
            missing or inaccessible.
        """
        super().__init__(**kwargs)
        logger.debug('... from file {}.'.format(str(p_path)))
        try:    # Reduce potential for new_from_file() abort.
            with p_path.open() as _io_none:
                pass
        except Exception as err_access:
            MESSAGE = ('Could not access description file "{}".'
                       ''.format(p_path.name))
            raise UiDescriptionError(MESSAGE) from err_access
        self._builder = Gtk.Builder.new_from_file(str(p_path))


class GetUiObjectStr(GetUiObject):
    """Extend :class:`.GetUiObject` with 'Gtk.Bujilder`_ from file."""

    def __init__(self, *, p_string: str, **kwargs) -> None:
        """Initialize underlying builder and log source of description.

        :param p_string: string containing user interface description.
        :param kwargs: superclass keyword parameters.
        """
        super().__init__(**kwargs)
        logger.debug('... from string.')
        ALL = -1
        self._builder = Gtk.Builder.new_from_string(p_string, ALL)

    def __call__(self, p_id: str) -> typing.Any:
        """Return object with given ID.

        :param p_id: ID of desired object.
        :raises UiObjectNotFoundError: when no object matches ID.
        """
        ui_object = self._builder.get_object(p_id)
        if ui_object is None:
            MESSAGE = 'No object found for ID {}.'.format(p_id)
            raise UiObjectNotFoundError(MESSAGE)
        return ui_object


class Base:
    """Base spec for Factsheet topics.

    A spec provides a user the means to create a class of topics.  A
    spec embodies a template for the class.  It queries the user to
    complete the template for a specific topic.  The spec also queries
    the user of the location of the new topic in the Factsheet's
    outline of topics.
    """

    def __init__(self, *, p_name: str, p_summary: str, p_title: str) -> None:
        """Initialize spec identity and topic identity including location.

        :param p_name: name of specification.
        :param p_summary: description of specification.
        :param p_title: descriptive title for specification.
        """
        self._name_spec = BUI.ModelTextMarkup(p_text=p_name)

        self._init_name_topic()
        self._response = None

    def _init_name_topic(self) -> None:
        """ Initialize"""
        self._name_topic = BUI.ModelTextMarkup(p_text='')
        self._new_display_name_topic = (
            BUI.FactoryDisplayTextMarkup(p_model=self._name_topic))
        self._new_editor_name_topic = (
            BUI.FactoryEditorTextMarkup(p_model=self._name_topic))

    def __call__(self):
        """Orchestrate creation and placement of new topic.

        The user specializes the specification to create the topic.  The
        user may confirm or cancel the topic.
        """
        assist = self.new_assistant()
        self.add_pages(p_assist=assist)
        self.run_assistant(p_assistant=assist)
        # construct topic (or exit)
        # place topic (or exit)
        # Issue #245: patch pending completion of assistant
        logger.warning('New Topic')
        logger.warning('Name: {}'.format(self._name_topic.text))

    def add_pages(self, p_assistant: Gtk.Assistant) -> None:
        """Add pages to assistant.

        :param p_assistant: assistant to gather topic parameters.
        """
        page_intro = self.new_page_intro()
        _i_new = p_assistant.append_page(page_intro)
        p_assistant.set_page_title(page_intro, 'Introduction')

        identify_display_name = self._new_display_name_topic()
        identify_editor_name = self._new_editor_name_topic()
        identify_view_name = VMARKUP.ViewMarkup(
            identify_display_name, identify_editor_name, 'Name')
        page_identify = self.new_page_identify(
            identify_view_name)
        _i_new = p_assistant.append_page(page_identify)
        p_assistant.set_page_title(page_identify, 'Identify')

    def add_page_confirm(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def add_page_locate(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def name(self) -> str:
        """TBD"""
        pass

    def new_assistant(self) -> typing.Optional[Gtk.Assistant]:
        """Return an assistant from user interface definition."""
        get_ui_object = GetUiObjectStr(p_string=UI_ASSIST)
        assist = get_ui_object('ui_assistant')
        _ = assist.connect('apply', self.on_apply)
        _ = assist.connect('cancel', self.on_cancel)
        _ = assist.connect('destroy', self.on_cancel)
        _ = assist.connect('prepare', self.on_prepare)
        return assist

    def new_page_identify(
            self, p_view_name: VMARKUP.ViewMarkup) -> PageAssist:
        """Return an identification page.

        :param p_view_name: view to display and edit topic name.
        """
        get_ui_object = GetUiObjectStr(p_string=UI_PAGE_IDENTIFY)
        new_page = get_ui_object('ui_page_identify')
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        site_name = get_ui_object('ui_identify_site_name')
        site_name.pack_start(
            p_view_name.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

        return new_page

    def new_page_intro(self) -> PageAssist:
        """Return an introduction page."""
        get_ui_object = GetUiObjectStr(p_string=UI_PAGE_INTRO)
        new_page = get_ui_object('ui_page_intro')
        return new_page

    def on_apply(self, p_assistant: Gtk.Assistant) -> None:
        """Hide assistant and record user confirmed new topic.

        Recording user's response unblocks call method.
        """
        # p_assistant.hide()
        self._response = Gtk.ResponseType.APPLY

    def on_cancel(self, p_assistant: Gtk.Assistant) -> None:
        """Hide assistant and record user cancelled new topic.

        Recording user's response unblocks call method.
        """
        # p_assistant.hide()
        self._response = Gtk.ResponseType.CANCEL

    def on_prepare(self, p_assistant: Gtk.Assistant, p_page: PageAssist,
                   **_kwargs) -> None:
        """Prepare page contents for presentation in assistant.

        This method has no effect in the base class.

        :param p_assistant: assistant presenting page.
        :param p_page: page to present.
        """
        pass

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

    def summary(self) -> str:
        """TBD"""
        pass

    def title(self) -> str:
        """TBD"""
        pass


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


UI_PAGE_IDENTIFY = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Generated with glade 3.22.1 -->
    <interface>
      <requires lib="gtk+" version="3.20"/>
      <object class="GtkBox" id="ui_page_identify">
        <property name="width_request">500</property>
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="margin_top">6</property>
        <property name="margin_bottom">6</property>
        <property name="orientation">vertical</property>
        <property name="spacing">6</property>
        <child>
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="halign">start</property>
            <property name="label" translatable="yes">Enter a name, a
                title, and summary for the new topic </property>
            <property name="use_markup">True</property>
            <property name="justify">fill</property>
            <property name="wrap">True</property>
            <property name="max_width_chars">60</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkGrid">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="margin_top">6</property>
            <property name="margin_bottom">6</property>
            <property name="row_spacing">6</property>
            <property name="column_spacing">12</property>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                    translatable="yes">&lt;i&gt;Name:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                    translatable="yes">&lt;i&gt;Title:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                    translatable="yes">&lt;i&gt;Summary:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label"translatable="yes">short identifier
                    for the topic.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">one-line
                    description of the topic.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">start</property>
                <property name="valign">start</property>
                <property name="label" translatable="yes">Description of
                    topic that adds detail to title.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">2</property>
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
          <object class="GtkGrid">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="row_spacing">6</property>
            <property name="column_spacing">12</property>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">center</property>
                <property name="label"
                    translatable="yes">&lt;b&gt;Name:&lt;/b&gt;</property>
                <property name="use_markup">True</property>
                <property name="justify">right</property>
                <property name="wrap">True</property>
                <property name="width_chars">6</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">center</property>
                <property name="label"
                    translatable="yes">&lt;b&gt;Title:&lt;/b&gt;</property>
                <property name="use_markup">True</property>
                <property name="justify">right</property>
                <property name="wrap">True</property>
                <property name="width_chars">6</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_identify_site_name">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox" id="ui_identify_site_title">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="orientation">vertical</property>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">1</property>
              </packing>
            </child>
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
            <property name="can_focus">False</property>
            <property name="margin_top">6</property>
            <property name="label"
                translatable="yes">&lt;b&gt;Summary&lt;/b&gt;</property>
            <property name="use_markup">True</property>
            <property name="justify">fill</property>
            <property name="wrap">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="ui_identify_site_summary">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="shadow_type">in</property>
            <property name="min_content_height">60</property>
            <child>
              <placeholder/>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">4</property>
          </packing>
        </child>
      </object>
    </interface>
    """


UI_PAGE_INTRO = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Generated with glade 3.22.1 -->
    <interface>
      <requires lib="gtk+" version="3.20"/>
      <object class="GtkBox" id="ui_page_intro">
        <property name="width_request">500</property>
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="margin_top">6</property>
        <property name="margin_bottom">6</property>
        <property name="orientation">vertical</property>
        <property name="spacing">6</property>
        <child>
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="halign">start</property>
            <property name="valign">start</property>
            <property name="label" translatable="yes">Use this assistant
                to add a topic to the &lt;i&gt;Topics &lt;/i&gt;outline.
                Also, you may group topics within the outline by adding
                a topic and then adding or moving topics underneath it.
                The steps for adding a topic are as follows.</property>
            <property name="use_markup">True</property>
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
          <object class="GtkGrid">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="row_spacing">6</property>
            <property name="column_spacing">12</property>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                    translatable="yes">&lt;i&gt;Identify:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                translatable="yes">&lt;i&gt;Confirm:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
                <property name="wrap">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">Customize
                    identification information for the new topic.  A
                    topic is identified by the name, title, and summary
                    that you enter.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
                <property name="max_width_chars">50</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">start</property>
                <property name="label" translatable="yes">Confirm the
                    topic information is correct.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
                <property name="max_width_chars">50</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">end</property>
                <property name="valign">start</property>
                <property name="label"
                    translatable="yes">&lt;i&gt;Locate:&lt;/i&gt;</property>
                <property name="use_markup">True</property>
              </object>
              <packing>
                <property name="left_attach">0</property>
                <property name="top_attach">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="halign">start</property>
                <property name="label" translatable="yes">Pick location
                    for new topic.</property>
                <property name="use_markup">True</property>
                <property name="justify">fill</property>
                <property name="wrap">True</property>
                <property name="max_width_chars">50</property>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="top_attach">1</property>
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
          <object class="GtkLabel">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="halign">start</property>
            <property name="margin_top">6</property>
            <property name="label"translatable="yes">
                Click &lt;b&gt;Next &lt;/b&gt;to proceed.
                Click &lt;b&gt;Cancel &lt;/b&gt;at any time to abandon
                the new topic.</property>
            <property name="use_markup">True</property>
            <property name="justify">fill</property>
            <property name="wrap">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
    </interface>
    """
