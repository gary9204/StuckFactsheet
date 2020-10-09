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

import factsheet.abc_types.abc_fact as ABC_FACT
import factsheet.abc_types.abc_topic as ABC_TOPIC
import factsheet.model.infoid as MINFOID
import factsheet.model.types_model as MTYPES

from factsheet.abc_types.abc_topic import TagTopic
from factsheet.model.types_model import IndexTopic
from factsheet.model.types_model import IndexFact
from factsheet.view.types_view import ViewOutlineFacts

logger = logging.getLogger('Main.model.topic')


class Topic(ABC_TOPIC.AbstractTopic[IndexFact, ViewOutlineFacts]):
    """Topic component of Factsheet :mod:`~factsheet.model`.

    Class ``Topic`` represents a specific subject within a Factsheet.
    A model topic consists of an outline of facts along with
    identification information (see :class:`.InfoId`.) Each fact
    represents statement about the topic's subject.

    .. admonition:: About Equality

        Two topics are equivalent when they have the equal facts
        outlines and identification information. Transient aspects of
        the topics (like topic forms) are not compared and may be
        different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same facts and topic information.

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

    def attach_form(
            self, p_form: ABC_TOPIC.InterfaceFormTopic[ViewOutlineFacts]
            ) -> None:
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
        self._facts.attach_view(p_form.get_view_facts())
        self._forms[id_form] = p_form

    def check_fact(self, p_i: IndexFact) -> None:
        """Check a fact.

        :param p_i: index of fact to check.
        """
        fact = self._facts.get_item(p_i)
        assert fact is not None
        fact.check()

    def clear_all(self) -> None:
        """Clear all of topic's facts. """
        for index in self._facts.indices():
            self.clear_fact(index)

    def clear_fact(self, p_i: IndexFact) -> None:
        """Clear a fact.

        :param p_i: index of fact to clear.
        """
        fact = self._facts.get_item(p_i)
        assert fact is not None
        fact.clear()

    def detach_all(self) -> None:
        """Detach all forms from topic."""
        while self._forms:
            _id_form, form = self._forms.popitem()
            self._detach_attribute_views(form)

    def detach_form(
            self, p_form: ABC_TOPIC.InterfaceFormTopic[ViewOutlineFacts]
            ) -> None:
        """Remove a topic form from topic.

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
        self._facts.detach_view(p_form.get_view_facts())

    def facts(self, p_index: IndexTopic = None
              ) -> typing.Iterator[ABC_FACT.InterfaceFact]:
        """Return iterator over facts in facts outline.

        The iterator is recursive (that is, includes fact at given
        index along with all its descendants).

        :param p_index: index of parent item of section.  Default
            iterates over entire facts outline.
        """
        for index in self._facts.indices(p_index):
            fact = self._facts.get_item(index)
            assert fact is not None
            yield fact

    def insert_fact_after(self, p_fact: ABC_FACT.InterfaceFact,
                          p_i: IndexFact) -> IndexFact:
        """Adds fact to facts outline after fact at given index.

        If index is None, adds topic at beginning of outline.

        :param p_fact: new fact to add.
        :param p_i: index of fact to precede new fact.
        :returns: index of newly-added topic.
        """
        self.set_stale()
        return self._facts.insert_after(p_fact, p_i)

    def insert_fact_before(self, p_fact: ABC_FACT.InterfaceFact,
                           p_i: IndexFact) -> IndexFact:
        """Adds fact to facts outline before fact at given index.

        If index is None, adds topic at end of outline.

        :param p_fact: new fact to add.
        :param p_i: index of fact to follow new fact.
        :returns: index of newly-added topic.
        """
        self.set_stale()
        return self._facts.insert_before(p_fact, p_i)

    def insert_fact_child(self, p_fact: ABC_FACT.InterfaceFact,
                          p_i: IndexFact) -> IndexFact:
        """Adds fact to fact outline as child of fact at given index.

        Method adds fact after all existing children.  If index is
        None, it adds fact at end of outline.

        :param p_fact: new fact to add.
        :param px_i: index of parent fact for new fact.
        :returns: index of newly-added fact.
        """
        self.set_stale()
        return self._facts.insert_child(p_fact, p_i)

    def insert_facts_section(self, p_source: MTYPES.OutlineFacts,
                             p_i: IndexFact = None) -> None:
        """Copy another facts outline under given fact.

        .. note:: This method makes a shallow copy.  The outlines share
            the facts after the copy.

        :param p_source: facts outline to copy.
        :param p_i: index to copy section under.  Default is top level
            after existing top-level items.
        """
        self.set_stale()
        COPY_ALL = None
        return self._facts.insert_section(p_source, COPY_ALL, p_i)

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to topic."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        if self._stale:
            return True

        if self._infoid.is_stale():
            self._stale = True
            return True

        for fact in self.facts():
            if fact.is_stale():
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
        for fact in self.facts():
            fact.set_fresh()

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
