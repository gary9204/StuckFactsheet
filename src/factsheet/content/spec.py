"""
Defines GTK-specific ancestor for template classes.

.. _`Gtk.Assistant`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Assistant.html

GTK-specific template classes wrap `GTK.Assistant`_. Module ``spec``
provides a common ancestor and helper function.
"""
import dataclasses as DC

import gi   # type: ignore[import]
import typing

import factsheet.view.block.block_fact as VFACT
import factsheet.view.types_view as VTYPES

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


StrAssist = typing.NewType('StrAssist', str)


@DC.dataclass
class ProtoFact:
    """Prototype information to define a fact.

    :param class_fact: class that defines fact.
    :param class_block: class that defines display block of fact.
    :param prereqs: names of prerequisite facts.
    """
    class_fact: typing.Type[ABC_FACT.InterfaceFact]  # noqa
    class_block: typing.Type[VFACT.BlockFact]   # noqa
    prereqs: typing.Iterable[str] = DC.field(default_factory=list)


@DC.dataclass
class ProtoTopic:
    """Prototype information to define a fact.

    :param class_topic: class that defines topic.
    :param classes_provider: class of topic's providers.
    """
    class_topic: typing.Type[ABC_TOPIC.AbstractTopic]  # noqa
    classes_provider: typing.Iterable[  # noqa
        typing.Type[ABC_TOPIC.AbstractTopic]] = DC.field(default_factory=list)


class Spec(ABC_SHEET.AbstractTemplate):
    """Ancestor for GTK-specific template classes to specify topics.

    :param p_name: name of template.
    :param p_summary: summary for template.
    :param p_title: title for template.
    :param p_path_assist: file system path to assistant user interface
        definition.
    :param p_attach_view_topics: funcion that returns current topics outline.
    :param p_prototopic: definition of topic.
    """

    def __init__(
            self, *, p_name: str, p_summary: str, p_title: str,
            p_path_assist: typing.Optional[StrAssist],
            p_attach_view_topics: VTYPES.AttachViewTopics,
            p_prototopic: ProtoTopic,
            ) -> None:
        self._name_template = p_name
        self._summary_template = p_summary
        self._title_template = p_title
        self._path_assist = p_path_assist
        self._attach_view_topics = p_attach_view_topics
        self._prototopic = p_prototopic.class_topic

        self._protofacts: typing.MutableSequence[ProtoFact] = list()
        self._fact_to_block = VFACT.MapFactToBlock()
        self._response: typing.Optional[Gtk.ResponseType] = None

    def __call__(self) -> typing.Optional[ABC_TOPIC.AbstractTopic]:
        """Return topic based on user's input or None when user cancels.

        Ancestor method returns None without querying user.
        """
        return None

    def add_protofact(self, p_protofact: ProtoFact) -> None:
        """Add fact prototype to collection."""
        self._protofacts.append(p_protofact)

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
