"""
Defines GTK-specific ancestor for template classes.

.. _`Gtk.Assistant`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Assistant.html

GTK-specific template classes wrap `GTK.Assistant`_. Module ``spec``
provides a common ancestor and helper function.
"""
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.view.block import block_fact as VFACT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


StrAssist = typing.NewType('StrAssist', str)


class Spec(ABC_SHEET.AbstractTemplate):
    """Ancestor for GTK-specific template classes to specify topics.

    :param p_name: name of template.
    :param p_summary: summary for template.
    :param p_title: title for template.
    :param p_class_topic: class defining topic.
    :param p_path_assist: file system path to assistant user interface
        definition.
    :param p_new_view_topics: funcion that returns current topics outline.
    """

    def __init__(
            self, *, p_name: str, p_summary: str, p_title: str,
            p_class_topic: typing.Type[ABC_TOPIC.AbstractTopic],
            p_path_assist: typing.Optional[StrAssist],
            p_new_view_topics: typing.Callable[[], ASHEET.AdaptTreeViewTopic]
            ) -> None:
        self._name_template = p_name
        self._summary_template = p_summary
        self._title_template = p_title
        self._class_topic = p_class_topic
        self._path_assist = p_path_assist
        self._new_view_topics = p_new_view_topics

        self._fact_to_block = VFACT.MapFactToBlock()
        self._response: typing.Optional[Gtk.ResponseType] = None

    def __call__(self) -> typing.Optional[ABC_TOPIC.AbstractTopic]:
        """Return topic based on user's input or None when user cancels.

        Ancestor method returns None without querying user.
        """
        return None

    @property
    def name(self) -> str:
        """Return template name. """
        return self._name_template

    def on_apply(self, p_assistant: Gtk.Assistant) -> None:
        """Record the user's response and hide assistant.

        Recording user's response unblocks call method.
        """
        p_assistant.hide()
        self._response = Gtk.ResponseType.APPLY

    def on_cancel(self, p_assistant: Gtk.Assistant) -> None:
        """Record the user's response and hide assistant.

        Recording user's reponse unblocks call method.
        """
        p_assistant.hide()
        self._response = Gtk.ResponseType.CANCEL

        # def on_prepare(self, p_assistant: Gtk.Assistant, p_page: Gtk.Widget,
        #                **kwargs: typing.Any) -> None:
        #     """Update assistant pages based on user's actions.
        #
        #     Ancestor method is a no-op.
        #     """
        #     pass

        # def set_view_topics(
        #         self, p_view_topics: ASHEET.AdaptTreeViewTopic) -> None:
        #     """Record view of topics outline to display topics to user.
        #
        #     Ancestor method is a no-op.
        #     """
        #     pass

    @property
    def summary(self) -> str:
        """Return template summary. """
        return self._summary_template

    @property
    def title(self) -> str:
        """Return template title. """
        return self._title_template


def textbuffer_get_text(
        p_buffer: Gtk.TextBuffer, p_hidden: bool = True) -> str:
    """Return contents of GTK text buffer.

    .. _`Gtk.TextBuffer`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

    Multiple template classes need to get content from a
    `Gtk.TextBuffer`_ in a `Gtk.Assistant`_.  Function
    ``textbuffer_get_text`` simplifies reading the entire contents of a
    buffer.
    """
    begin, end = p_buffer.get_bounds()
    text = p_buffer.get_text(begin, end, p_hidden)
    return text
