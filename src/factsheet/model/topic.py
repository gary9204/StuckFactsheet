"""
Defines topic-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
the base class representing the model of a topic.  Additional classes
specialize the model for sets, operations, and so on.
"""
import logging
import typing   # noqa

import factsheet.abc_types.abc_topic as ABC_TOPIC
import factsheet.model.fact as MFACT
import factsheet.model.infoid as MINFOID
import factsheet.model.types_model as MTYPES

from factsheet.abc_types.abc_topic import TagTopic

logger = logging.getLogger('Main.model.topic')

ClassesFact = typing.Iterable[typing.Type[MFACT.Fact]]


class Topic(ABC_TOPIC.AbstractTopic):
    """Topic component of Factsheet :mod:`~factsheet.model`.

    Class ``Topic`` represents a specific subject within a Factsheet.
    A model topic consists of an outline of facts along with
    identification information (see :class:`.InfoId`.) Each fact
    represents statement about the topic's subject.

    .. admonition:: About Equality

        Two topics are equivalent when they have the same fact outlines
        and identification information. Transient aspects of the topics
        (like topic forms) are not compared and may be different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same topic information.

        :param p_other: object to compare with self.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self._infoid != p_other._infoid:
            return False

        if self._facts != p_other._facts:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return topic model in form pickle can persist.

        Persistent form of topic excludes run-time information.
        """
        state = self.__dict__.copy()
        del state['_forms']
        del state['_stale']
        return state

    def __init__(self, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError("Topic.__init__() called with extra argument(s): "
                            "{}".format(kwargs))
        self._infoid = MINFOID.InfoId()
        self._tag = TagTopic(id(self))
        self._facts = MTYPES.OutlineFacts()
        self._state_transient()

    def init_identity(self, *, p_name: str = '', p_summary: str = '',
                      p_title: str = '') -> None:
        """Assign initial name, title, and summary for topic.

        :param p_name: name for component.
        :param p_summary: summary for component.
        :param p_title: title for component.
        """
        self._infoid.init_identity(
            p_name=p_name, p_summary=p_summary, p_title=p_title)

    def __setstate__(self, p_state: typing.Dict) -> None:
        """Reconstruct topic model from state pickle loads.

        Reconstructed attribute is marked fresh and has no topic forms.

        :param p_state: unpickled state of stored topic model.
        """
        self.__dict__.update(p_state)
        self._state_transient()

    def _state_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._stale = False
        self._forms: typing.MutableMapping[
            int, ABC_TOPIC.InterfaceFormTopic] = dict()

    def attach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Add topic form to update display when topic changes.

        Log warning when requested form is already attached.

        :param p_form: form to add.

        """
        id_form = id(p_form)
        if id_form in self._forms.keys():
            logger.warning(
                'Duplicate form: {} ({}.{})'.format(
                    hex(id_form),
                    self.__class__.__name__, self.attach_form.__name__))
            return

        self._infoid.attach_view(p_form.get_infoid())
        self._forms[id_form] = p_form

    def check_fact(self, p_i: ABC_TOPIC.IndexOpaque) -> None:
        """Check a fact.

        :param p_i: index of fact to check.
        """
        raise NotImplementedError

    def clear_all(self) -> None:
        """Clear all of topic's facts. """
        raise NotImplementedError

    def clear_fact(self, p_i: ABC_TOPIC.IndexOpaque) -> None:
        """Clear a fact.

        :param p_i: index of fact to clear.
        """
        raise NotImplementedError

    def detach_all(self) -> None:
        """Detach all forms from topic."""
        while self._forms:
            _id_form, form = self._forms.popitem()
            self._detach_attribute_views(form)

    def detach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Remove one topic form from topic.

        Log warning when requested form is not attached.

        :param p_form: form to remove.
        """
        id_form = id(p_form)
        try:
            self._forms.pop(id_form)
        except KeyError:
            logger.warning(
                'Missing form: {} ({}.{})'.format(
                    hex(id_form),
                    self.__class__.__name__, self.detach_form.__name__))
            return

        self._detach_attribute_views(p_form)

    def _detach_attribute_views(
            self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
        """For each topic attribute with a distinct view, remove the
        view for the attribute.

        :param p_form: topic form as a whole.
        """
        self._infoid.detach_view(p_form.get_infoid())

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to topic."""
        if self._stale:
            return False

        if self._infoid.is_stale():
            self._stale = True
            return False

        return True

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        if self._stale:
            return True

        if self._infoid.is_stale():
            self._stale = True
            return True

        return False

    @property
    def name(self) -> str:
        """Return topic name."""
        return self._infoid.name

    def set_fresh(self) -> None:
        """Mark topic in memory consistent with file contents."""
        self._stale = False
        self._infoid.set_fresh()

    def set_stale(self) -> None:
        """Mark topic in memory changed from file contents."""
        self._stale = True

    @property
    def summary(self) -> str:
        """Return topic summary."""
        return self._infoid.summary

    @property
    def tag(self) -> TagTopic:
        """Return topic identifier. """
        return self._tag

    @property
    def title(self) -> str:
        """Return topic title."""
        return self._infoid.title
