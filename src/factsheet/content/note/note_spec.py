"""
Defines template class to specify a topic for user notes.  See
:mod:`~.factsheet.content.note`.
"""
import gi   # type: ignore[import]
import typing

from factsheet.content import spec as XSPEC
from factsheet.content.note import note_topic as XNOTE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class SpecNote(XSPEC.Spec):
    """Template to specify a topic for user notes.

    The class provides a call interface that returns note topic based on
    user's input or None when user cancels. The call takes no arguments.
    Instead, the call presents an assistant to query the user for values
    that define the new note.

    See also :class:`.Note`.
    """

    # def __init__(self, **kwargs) -> None:
    #     super().__init__(**kwargs)

    def __call__(self) -> typing.Optional[XNOTE.Note]:
        """Return topic based on user's input or None when user cancels."""
        builder = Gtk.Builder.new_from_file(self._path_assist)
        get_object = builder.get_object

        assistant = get_object('ui_assistant')
        _ = assistant.connect('apply', self.on_apply)
        _ = assistant.connect('cancel', self.on_cancel)
        _ = assistant.connect('destroy', self.on_cancel)
        _ = assistant.connect('prepare', lambda _assistant, _page: None)

        name_topic = get_object('ui_name')
        summary_topic = get_object('ui_summary')
        title_topic = get_object('ui_title')

        self._response = None
        assistant.show()
        while self._response is None:
            _ = Gtk.main_iteration()

        topic = None
        if self._response is Gtk.ResponseType.APPLY:
            name = name_topic.get_text()
            summary = XSPEC.textbuffer_get_text(summary_topic)
            title = title_topic.get_text()
            topic = self._class_topic(
                p_name=name, p_summary=summary, p_title=title)
        return topic
