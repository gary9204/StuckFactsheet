"""
Defines class to specify an modular addition of integers.  See
:mod:`~.plusmodn_topic`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import typing

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import spec as XSPEC
from factsheet.content.ops.int import plusmodn_topic as XPLUS_N
from factsheet.content.sets.int import setint_topic as XSET_INT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class UiConfirm:
    """Collection of user interface fields for assistant page Confirm."""
    ui_cursor: Gtk.TreeSelection
    ui_name_set: Gtk.Label
    ui_title_set: Gtk.Label
    ui_modulus: Gtk.SpinButton
    ui_view_modulus: Gtk.Label


@DC.dataclass
class UiIdentify:
    """Collection of user interface fields for assistant page Identify."""
    ui_modulus: Gtk.SpinButton
    ui_name: Gtk.EntryBuffer
    ui_summary: Gtk.TextBuffer
    ui_title: Gtk.EntryBuffer


@DC.dataclass
class UiPages:
    """Collection of user interface fields by assistant page."""
    page_confirm: UiConfirm
    page_identify: UiIdentify


class SpecPlusModN(XSPEC.Spec):
    """Class to specify a topic for modular addition operation.

    The class provides a call interface that returns modular addition
    topic based on user's input or None when user cancels. The call
    takes no arguments. Instead, the call presents an assistant to query
    the user for values that define the new operation.

    See also :class:`.PlusModN`.

    .. attribute:: NO_SUMMARY

    Summary text to display when the user has not selected a topic.
    """

    NO_SUMMARY = 'Please select a <b>topic.</b>'

    def __call__(self) -> typing.Optional[XPLUS_N.PlusModN]:
        """Return topic based on user's input or None when user cancels."""
        builder = Gtk.Builder.new_from_file(self._path_assist)
        get_ui = builder.get_object

        assistant = get_ui('ui_assistant')
        outline_topics = self._new_view_topics()
        gtk_outline = outline_topics.gtk_view
        ui_search_entry = get_ui('ui_search_entry')
        gtk_outline.set_search_entry(ui_search_entry)
        cursor = gtk_outline.get_selection()
        ui_summary_set = get_ui('ui_summary_set')
        _ = cursor.connect(
            'changed', self.on_changed_cursor, assistant, ui_summary_set)
        # gtk_outline.show_all()

        ui_modulus = get_ui('ui_modulus')
        ui_confirm = UiConfirm(
            ui_cursor=cursor,
            ui_name_set=get_ui('ui_name_set'),
            ui_title_set=get_ui('ui_title_set'),
            ui_modulus=ui_modulus,
            ui_view_modulus=get_ui('ui_view_modulus')
            )
        ui_identify = UiIdentify(
            ui_modulus=ui_modulus,
            ui_name=get_ui('ui_name'),
            ui_summary=get_ui('ui_summary'),
            ui_title=get_ui('ui_title')
            )
        ui_pages = UiPages(
            page_confirm=ui_confirm,
            page_identify=ui_identify
            )

        ui_search_by_name = get_ui('ui_search_by_name')
        ui_search_by_name.connect('toggled', self.on_toggle_search_field,
                                  outline_topics, ASHEET.FieldsTopic.NAME)
        ui_search_by_title = get_ui('ui_search_by_title')
        ui_search_by_title.connect('toggled', self.on_toggle_search_field,
                                   outline_topics, ASHEET.FieldsTopic.NAME)

        ui_context_topics = get_ui('ui_context_topics')
        ui_context_topics.add(gtk_outline)
        ui_context_topics.show_all()

        _ = assistant.connect('apply', self.on_apply)
        _ = assistant.connect('cancel', self.on_cancel)
        _ = assistant.connect('destroy', self.on_cancel)
        _ = assistant.connect('prepare', self.on_prepare, ui_pages)

        self._response = None
        assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()

        topic = None
        if self._response is Gtk.ResponseType.APPLY:
            name = ui_identify.ui_name.get_text()
            summary = XSPEC.textbuffer_get_text(ui_identify.ui_summary)
            title = ui_identify.ui_title.get_text()
            model, index = cursor.get_selected()
            set_int = AOUTLINE.get_item_gtk(model, index)
            modulus = ui_modulus.get_value_as_int()
            topic = self._class_topic(
                p_name=name, p_summary=summary, p_title=title,
                p_set=set_int, p_modulus=modulus)
        return topic

    def on_changed_cursor(
            self, p_cursor: Gtk.TreeSelection, p_assistant: Gtk.Assistant,
            p_summary_set: Gtk.TextBuffer) -> None:
        """Changes summary text to match current template.

        :param p_cursor: identifies now-current topic.
        :param p_assistant: assistant collecting user responses.
        :param p_summary_set: assistant field for set topic summary.
        """
        N_PAGE_SET = 2
        summary = self.NO_SUMMARY
        is_complete = False
        model, index = p_cursor.get_selected()
        if index is not None:
            item = AOUTLINE.get_item_gtk(model, index)
            if item is not None:
                summary = item.summary
                is_complete = isinstance(item, XSET_INT.SetInt)

        ALL = -1
        p_summary_set.set_text(summary, ALL)
        page = p_assistant.get_nth_page(N_PAGE_SET)
        p_assistant.set_page_complete(page, is_complete)

    def on_prepare(self, p_assistant: Gtk.Assistant, p_page: Gtk.Widget,
                   p_ui_pages: UiPages) -> None:
        """Update assistant's visible page based on user's actions.

        :param p_assistant: active assistant.
        :param p_page: page about to be shown.
        :param p_ui_pages: assistant fields by page.
        """
        title_page = p_assistant.get_page_title(p_page)
        if 'New Operation' == title_page:
            pass
        elif 'Modulus' == title_page:
            pass
        elif 'Set' == title_page:
            pass
        elif 'Identify' == title_page:
            self._prepare_identify(
                p_assistant, p_page, p_ui_pages.page_identify)
        elif 'Confirm' == title_page:
            self._prepare_confirm(
                p_assistant, p_page, p_ui_pages.page_confirm)
        else:
            pass

    def _prepare_confirm(
            self, _assistant, _page, p_ui_confirm: UiConfirm) -> None:
        """Populate set name, set title, and modulus fields."""
        model, index = p_ui_confirm.ui_cursor.get_selected()
        topic_set = AOUTLINE.get_item_gtk(model, index)
        if topic_set is None:
            WARNING = 'Oops! Please go back and select a set.'
            name_set = WARNING
            title_set = WARNING
        else:
            name_set = topic_set.name
            title_set = topic_set.title
        p_ui_confirm.ui_name_set.set_markup(name_set)
        p_ui_confirm.ui_title_set.set_markup(title_set)
        modulus = p_ui_confirm.ui_modulus.get_value_as_int()
        text = '<i>Modulus: </i>{}'.format(modulus)
        p_ui_confirm.ui_view_modulus.set_markup(text)

    def _prepare_identify(self, p_assistant: Gtk.Assistant,
                          p_page: Gtk.Widget, p_ui_identify: UiIdentify
                          ) -> None:
        """Fill in identification fields based on modulus from user."""
        p_assistant.set_page_complete(p_page, True)
        modulus = p_ui_identify.ui_modulus.get_value_as_int()

        ALL = -1
        name = '+ (mod {})'.format(modulus)
        p_ui_identify.ui_name.set_text(name, ALL)
        summary = 'The operation is addition modulo {}.'.format(modulus)
        p_ui_identify.ui_summary.set_text(summary, ALL)
        title = 'Plus Modulo {}'.format(modulus)
        p_ui_identify.ui_title.set_text(title, ALL)

    def on_toggle_search_field(self, p_button: Gtk.ToggleButton,
                               p_outline: ASHEET.AdaptTreeViewTopic,
                               p_field: ASHEET.FieldsTopic) -> None:
        """Sets search to match active field button.

        :param p_button: button user toggled.
        :param p_outline: view of topics outline.
        :param p_field: search field of toggled button.
        """
        if p_button.get_active():
            p_outline.scope_search |= p_field
        else:
            p_outline.scope_search &= ~p_field
