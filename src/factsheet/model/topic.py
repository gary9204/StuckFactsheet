"""
Defines topic-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
the base class representing the model of a topic.  Additional classes
specialize the model for sets, operations, and so on.
"""
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE

NameTopic = BUI.BridgeTextMarkup
SummaryTopic = BUI.BridgeTextFormat
TitleTopic = BUI.BridgeTextMarkup
TagTopic = typing.NewType('TagTopic', int)


class BadgeFact:
    """Representation to identify and distinguish a fact.

    The representation includes topic information to place a fact in
    context.

    :param p_fact: fact to identify.
    :param p_topic: topic containing fact.
    """

    def __init__(self, p_topic: 'Topic',
                 p_fact: MFACT.Fact['Topic', MFACT.ValueOpaque]) -> None:
        self._fact = p_fact
        self._topic = p_topic

    @property
    def name_fact(self) -> str:
        """***** stopped ***** """
        return self._fact.name.text

    # @property
    def name_topic(self) -> str:
        """ """
        raise NotImplementedError

    # @property
    def tag_fact(self) -> MFACT.TagFact:
        """ """
        raise NotImplementedError

    # @property
    def tag_topic(self) -> TagTopic:
        """ """
        raise NotImplementedError

    # @property
    def title_fact(self) -> str:
        """ """
        raise NotImplementedError

    # @property
    def title_topic(self) -> str:
        """ """
        raise NotImplementedError


class Topic(MIDCORE.IdCore[NameTopic, SummaryTopic, TitleTopic]):
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
        if not super().__eq__(p_other):
            return False

        # if self._facts != p_other._facts:
        #     return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return topic model in form pickle can persist.

        Persistent form of topic excludes run-time information.
        """
        state = super().__getstate__()
        del state['_tag']
        return state

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self._name = NameTopic()
        self._summary = SummaryTopic()
        self._title = TitleTopic()
        self._tag = TagTopic(id(self))

    def __setstate__(self, p_state: typing.Dict) -> None:
        """Reconstruct topic model from state pickle loads.

        Reconstructed attribute is marked fresh and has no topic forms.

        :param p_state: unpickled state of stored topic model.
        """
        super().__setstate__(p_state)
        self._tag = TagTopic(id(self))

    def check_fact(self, p_i: int) -> None:
        """Check a fact.

        :param p_i: index of fact to check.
        """
        raise NotImplementedError
        # fact = self._facts.get_item(p_i)
        # assert fact is not None
        # fact.check()

    def clear_all(self) -> None:
        """Clear all of topic's facts. """
        raise NotImplementedError
        # for index in self._facts.indices():
        #     self.clear_fact(index)

    def clear_fact(self, p_i: int) -> None:
        """Clear a fact.

        :param p_i: index of fact to clear.
        """
        raise NotImplementedError
        # fact = self._facts.get_item(p_i)
        # assert fact is not None
        # fact.clear()

    def facts(self, p_index: int = None) -> str:
        """Return iterator over facts in facts outline.

        The iterator is recursive (that is, includes fact at given
        index along with all its descendants).

        :param p_index: index of parent item of section.  Default
            iterates over entire facts outline.
        """
        raise NotImplementedError
        # for index in self._facts.indices(p_index):
        #     fact = self._facts.get_item(index)
        #     assert fact is not None
        #     yield fact

    def insert_fact_after(self, p_fact: str, p_i: int) -> int:
        """Adds fact to facts outline after fact at given index.

        If index is None, adds topic at beginning of outline.

        :param p_fact: new fact to add.
        :param p_i: index of fact to precede new fact.
        :returns: index of newly-added topic.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._facts.insert_after(p_fact, p_i)

    def insert_fact_before(self, p_fact: str, p_i: int) -> int:
        """Adds fact to facts outline before fact at given index.

        If index is None, adds topic at end of outline.

        :param p_fact: new fact to add.
        :param p_i: index of fact to follow new fact.
        :returns: index of newly-added topic.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._facts.insert_before(p_fact, p_i)

    def insert_fact_child(self, p_fact: str, p_i: int) -> int:
        """Adds fact to fact outline as child of fact at given index.

        Method adds fact after all existing children.  If index is
        None, it adds fact at end of outline.

        :param p_fact: new fact to add.
        :param px_i: index of parent fact for new fact.
        :returns: index of newly-added fact.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._facts.insert_child(p_fact, p_i)

    def insert_facts_section(self, p_source: int, p_i: int = None) -> None:
        """Copy another facts outline under given fact.

        .. note:: This method makes a shallow copy.  The outlines share
            the facts after the copy.

        :param p_source: facts outline to copy.
        :param p_i: index to copy section under.  Default is top level
            after existing top-level items.
        """
        raise NotImplementedError
        # self.set_stale()
        # COPY_ALL = None
        # return self._facts.insert_section(p_source, COPY_ALL, p_i)

    # def is_fresh(self) -> bool:
    #     """Return True when there are no unsaved changes to topic."""
    #     raise NotImplementedError
    #     # return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        raise NotImplementedError
        # if super().is_stale():
        #     return True

        # for fact in self.facts():
        #     if fact.is_stale():
        #         self._stale = True
        #         return True

        # return False

    @property
    def name(self) -> NameTopic:
        """Return topic name."""
        return self._name

    def set_fresh(self) -> None:
        """Mark topic in memory consistent with file contents."""
        raise NotImplementedError
        # super().set_fresh()
        # for fact in self.facts():
        #     fact.set_fresh()

    # def set_stale(self) -> None:
    #     """Mark topic in memory changed from file contents."""
    #     raise NotImplementedError
    #     # self._stale = True

    @property
    def summary(self) -> SummaryTopic:
        """Return topic summary."""
        return self._summary

    @property
    def tag(self) -> TagTopic:
        """Return topic identifier. """
        return self._tag

    @property
    def title(self) -> TitleTopic:
        """Return topic title."""
        return self._title
