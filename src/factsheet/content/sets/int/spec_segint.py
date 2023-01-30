"""
Defines class to specify an initial segment of natural nubmers.  See
:mod:`~.topic_set`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import typing

import factsheet.content.spec as XSPEC
import factsheet.content.sets.int.topic_segint as XSEGINT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class UiArgs:
    """Collection of user interface objects in assistant to define topic."""
    ui_name: Gtk.EntryBuffer
    ui_summary: Gtk.TextBuffer
    ui_title: Gtk.EntryBuffer
    ui_bound: Gtk.SpinButton
    ui_segment: Gtk.Label


class SpecSegInt(XSPEC.Spec):
    """Class to specify a topic for initial segment of natural numbers.

    The class provides a call interface that returns segment topic based
    on user's input or None when user cancels. The call takes no
    arguments. Instead, the call presents an assistant to query the user
    for values that define the new initial segment.

    See also :class:`.SegInt`.
    """

    def __call__(self) -> typing.Optional[XSEGINT.SegInt]:
        """Return topic based on user's input or None when user cancels."""
        builder = Gtk.Builder.new_from_file(self._path_assist)
        get_object = builder.get_object

        ui_topic = UiArgs(
            ui_name=get_object('ui_name'),
            ui_summary=get_object('ui_summary'),
            ui_title=get_object('ui_title'),
            ui_bound=get_object('ui_bound'),
            ui_segment=get_object('ui_segment')
        )

        assistant = get_object('ui_assistant')
        _ = assistant.connect('apply', self.on_apply)
        _ = assistant.connect('cancel', self.on_cancel)
        _ = assistant.connect('destroy', self.on_cancel)
        _ = assistant.connect('prepare', self.on_prepare, ui_topic)

        self._response = None
        assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()

        topic = None
        if self._response is Gtk.ResponseType.APPLY:
            name = ui_topic.ui_name.get_text()
            summary = XSPEC.textbuffer_get_text(ui_topic.ui_summary)
            title = ui_topic.ui_title.get_text()
            bound = ui_topic.ui_bound.get_value_as_int()
            topic = self._prototopic(p_bound=bound)
            topic.init_identity(p_name=name, p_summary=summary, p_title=title)
        return topic

    def on_prepare(self, p_assistant: Gtk.Assistant, p_page: Gtk.Widget,
                   p_ui_topic: UiArgs) -> None:
        """Update assistant's visible page based on user's actions.

        :param p_assistant: active assistant.
        :param p_page: page about to be shown.
        :param p_ui_topic: user responses in assistant fields.
        """
        title_page = p_assistant.get_page_title(p_page)
        if 'New Segment' == title_page:
            pass
        elif 'Bound' == title_page:
            pass
        elif 'Identify' == title_page:
            self._prepare_identify(p_assistant, p_page, p_ui_topic)
        elif 'Confirm' == title_page:
            self._prepare_confirm(p_assistant, p_page,
                                  p_ui_topic.ui_bound, p_ui_topic.ui_segment)
        else:
            pass

    def _prepare_confirm(
            self, _assistant, _page, p_ui_bound: Gtk.SpinButton,
            p_ui_segment: Gtk.Label) -> None:
        """Add bound to segment label."""
        bound = p_ui_bound.get_value_as_int()
        segment = '<b>Segment: </b>[0, {})'.format(bound)
        p_ui_segment.set_markup(segment)

    def _prepare_identify(self, p_assistant: Gtk.Assistant,
                          p_page: Gtk.Widget, p_ui_topic: UiArgs) -> None:
        """Fill in identification fields based on bound the user entered."""
        p_assistant.set_page_complete(p_page, True)
        bound = p_ui_topic.ui_bound.get_value_as_int()

        name = 'N({})'.format(bound)
        ALL = -1
        p_ui_topic.ui_name.set_text(name, ALL)

        pattern = ('The set is initial segment of natural numbers '
                   '[0, {}) (that is, {}).')
        if 1 == bound:
            summary = pattern.format(bound, '{0}')
        elif 2 == bound:
            summary = pattern.format(bound, '{0, 1}')
        elif 3 == bound:
            summary = pattern.format(bound, '{0, 1, 2}')
        else:
            detail = '{{0, 1, ..., {}}}'.format(bound - 1)
            summary = pattern.format(bound, detail)
        p_ui_topic.ui_summary.set_text(summary, ALL)

        title = 'Set of integers [0, {})'.format(bound)
        p_ui_topic.ui_title.set_text(title, ALL)
