"""
Defines template class to specify a topic for user notes.  See
:mod:`~.factsheet.content.note`.
"""
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.content.note import note_topic as XNOTE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class SpecNote(ABC_SHEET.AbstractTemplate):
    """Template to specify a topic for user notes.

    The class provides a call interface that returns note topic based on
    user's input or None when user cancels. The call takes no arguments.
    Instead, the call presents an assistant to query the user for values
    that define the new note.

    See also :class:`.Note`.
    """

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 p_path_assist: str, p_model: typing.Type[XNOTE.Note]
                 ) -> None:
        self._name_template = p_name
        self._summary_template = p_summary
        self._title_template = p_title

        builder = Gtk.Builder.new_from_file(p_path_assist)
        get_object = builder.get_object

        self._response: typing.Optional[Gtk.ResponseType] = None
        self._model_topic = p_model

        self._assistant = get_object('ui_assistant')
        _ = self._assistant.connect('apply', self.on_apply)
        _ = self._assistant.connect('cancel', self.on_cancel)
        _ = self._assistant.connect('destroy', self.on_cancel)
        _ = self._assistant.connect('prepare', self.on_prepare)

        self._name_topic = get_object('ui_name')
        self._summary_topic = get_object('ui_summary')
        self._title_topic = get_object('ui_title')

    def __call__(self) -> typing.Optional[XNOTE.Note]:
        """Return topic based on user's input or None when user cancels."""
        self._assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()

        topic = None
        if self._response is Gtk.ResponseType.APPLY:
            name = self._name_topic.get_text()
            start, end = self._summary_topic.get_bounds()
            INCLUDE_HIDDEN = True
            summary = self._summary_topic.get_text(start, end, INCLUDE_HIDDEN)
            title = self._title_topic.get_text()
            topic = self._model_topic(
                p_name=name, p_summary=summary, p_title=title)

        self._response = None
        BLANK = ''
        self._name_topic.set_text(BLANK, -1)
        self._summary_topic.set_text(BLANK, -1)
        self._title_topic.set_text(BLANK, -1)
        return topic

    @property
    def name(self) -> str:
        """Return template name. """
        return self._name_template

    def on_apply(self, _px_assist: Gtk.Assistant) -> None:
        """Record the user's response, hide assistant, and unblock call
        method.
        """
        self._assistant.hide()
        self._response = Gtk.ResponseType.APPLY

    def on_cancel(self, _px_assist: Gtk.Assistant) -> None:
        """Record the user's response, hide assistant, and unblock call
        method.
        """
        self._assistant.hide()
        self._response = Gtk.ResponseType.CANCEL

    def on_prepare(self, _px_assist: Gtk.Assistant, _pm_page: Gtk.Widget
                   ) -> None:
        """Update assistant pages based on user's actions.

        Method on_prepare is a no-op for :class:`~.SpecNote`.
        """
        pass

    @property
    def summary(self) -> str:
        """Return template summary. """
        return self._summary_template

    @property
    def title(self) -> str:
        """Return template title. """
        return self._title_template
