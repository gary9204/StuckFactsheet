"""
Defines class to specify an initial segment of natural nubmers.  See
:mod:`~.set_topic`.
"""
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.content import gtk_helper as XHELPER
from factsheet.content.ops.int import plusmodn_topic as XPLUS_N

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class SpecPlusModN(ABC_SHEET.AbstractTemplate):
    """Class to specify a topic for initial segment of natural numbers.

    The class provides a call interface that returns segment topic based
    on user's input or None when user cancels. The call takes no
    arguments. Instead, the call presents an assistant to query the user
    for values that define the new initial segment.

    See also :class:`.SegInt`.
    """

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 p_path_assist: str, p_model: typing.Type[XPLUS_N.PlusModN]
                 ) -> None:
        pass
        self._name_template = p_name
        self._summary_template = p_summary
        self._title_template = p_title

        builder = Gtk.Builder.new_from_file(p_path_assist)
        get_object = builder.get_object
        self._model_topic = p_model
        self._name_topic = get_object('ui_name')
        self._summary_topic = get_object('ui_summary')
        self._title_topic = get_object('ui_title')
        self._bound = get_object('ui_bound')
        self._segment = get_object('ui_segment')

        self._assistant = get_object('ui_assistant')
        _ = self._assistant.connect('apply', self.on_apply)
        _ = self._assistant.connect('cancel', self.on_cancel)
        _ = self._assistant.connect('destroy', self.on_cancel)
        _ = self._assistant.connect('prepare', self.on_prepare)

        self._response: typing.Optional[Gtk.ResponseType]
        self._clear_assist()

    def __call__(self) -> typing.Optional[XPLUS_N.PlusModN]:
        """Return topic based on user's input or None when user cancels."""
        self._assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()

        topic = None
        if self._response is Gtk.ResponseType.APPLY:
            name = self._name_topic.get_text()
            summary = XHELPER.textbuffer_get_text(self._summary_topic)
            title = self._title_topic.get_text()
            bound = self._bound.get_value_as_int()
            topic = self._model_topic(p_name=name, p_summary=summary,
                                      p_title=title, p_bound=bound)
        self._clear_assist()
        return topic

    def _clear_assist(self) -> None:
        """Clear the contents of assistant."""
        ALL = -1
        BLANK = ''
        BOUND_DEFAULT = 1
        self._name_topic.set_text(BLANK, ALL)
        self._summary_topic.set_text(BLANK, ALL)
        self._title_topic.set_text(BLANK, ALL)
        self._bound.set_value(BOUND_DEFAULT)
        self._response = None

    @property
    def name(self) -> str:
        """Return template name. """
        return self._name_template

    def on_apply(self, _p_assist: Gtk.Assistant) -> None:
        """Record the user's response, hide assistant, and unblock call
        method.
        """
        self._assistant.hide()
        self._response = Gtk.ResponseType.APPLY

    def on_cancel(self, _p_assist: Gtk.Assistant) -> None:
        """Record the user's response, hide assistant, and unblock call
        method.
        """
        self._assistant.hide()
        self._response = Gtk.ResponseType.CANCEL

    def on_prepare(self, p_assistant: Gtk.Assistant, p_page: Gtk.Widget
                   ) -> None:
        """Update assistant's visible page based on user's actions.

        :param p_assistant: active assistant.
        :param p_page: page about to be shown.
        """
        prepare_page = {
            'New Segment': lambda _page: None,
            'Bound': lambda _page: None,
            'Identify': self._prepare_identify,
            'Confirm': self._prepare_confirm,
            }
        title_page = p_assistant.get_page_title(p_page)
        prepare_page[title_page](p_page)

    def _prepare_identify(self, p_page) -> None:
        """Fill in identification fields based on bound the user entered."""
        self._assistant.set_page_complete(p_page, True)
        bound = self._bound.get_value_as_int()

        name = 'N({})'.format(bound)
        self._name_topic.set_text(name, -1)

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
        self._summary_topic.set_text(summary, -1)

        title = 'Set of integers [0, {})'.format(bound)
        self._title_topic.set_text(title, -1)

    def _prepare_confirm(self, _page) -> None:
        """Add bound to segment label."""
        bound = self._bound.get_value_as_int()
        segment = '<b>Segment: </b>[0, {})'.format(bound)
        self._segment.set_markup(segment)

    @property
    def summary(self) -> str:
        """Return template summary. """
        return self._summary_template

    @property
    def title(self) -> str:
        """Return template title. """
        return self._title_template
