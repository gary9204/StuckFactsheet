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

LineOutline = BUI.LineOutline
# NameTopic = MFACT.NameTopic
OutlineFacts = BUI.BridgeOutlineColumnar[MFACT.Fact]
# SummaryTopic = MFACT.SummaryTopic
TagTopic = typing.NewType('TagTopic', int)  # was: MFACT.TagTopic
# TitleTopic = MFACT.TitleTopic

ViewNameTopic = BUI.ViewTextMarkup
ViewSummaryTopic = BUI.ViewTextTagged
ViewTitleTopic = BUI.ViewTextMarkup


class Topic(MIDCORE.IdCore[ViewNameTopic, ViewSummaryTopic, ViewTitleTopic]):
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

    def __contains__(self, p_fact: MFACT.Fact) -> bool:
        """Return True when fact is in facts outline."""
        for fact in self:
            if p_fact is fact:
                return True

        return False

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same facts and topic information.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._facts != p_other._facts:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return topic model in form pickle can persist.

        Persistent form of topic excludes run-time information.
        """
        state = super().__getstate__()
        del state['_tag']
        return state

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 **kwargs: typing.Any) -> None:
        super().__init__(p_name=p_name, p_summary=p_summary,
                         p_title=p_title, **kwargs)
        self._facts = OutlineFacts()
        # self._name = NameTopic()
        # self._summary = SummaryTopic()
        # self._title = TitleTopic()
        self._tag = TagTopic(id(self))

    def __iter__(self) -> typing.Iterator[MFACT.Fact]:
        """Return iterator over facts in facts outline.

        Iterator skips lines that contain None.
        """
        for fact in self._facts.items():
            if fact is not None:
                yield fact

    def __setstate__(self, p_state: typing.Dict) -> None:
        """Reconstruct topic model from state pickle loads.

        Reconstructed attribute is marked fresh.

        :param p_state: unpickled state of stored topic model.
        """
        super().__setstate__(p_state)
        self._tag = TagTopic(id(self))

    def append_fact(self, p_fact: MFACT.Fact) -> None:
        """Add new fact to the end of facts outline.

        Do not add a fact already in the outline.

        :param p_fact: new fact to add.
        """
        if p_fact in self:
            return

        _index = self._facts.insert_before(p_fact)
        self.set_stale()

    def append_outline_facts(self, p_topic: 'Topic') -> None:
        """Add other topic's facts outline to the end of facts outline.

        Do not add any fact already in the outline.

        :param p_topic: topic containing facts outline to add.
        """
        for fact in p_topic:
            self.append_fact(fact)

    def check_fact(self, p_line: LineOutline) -> None:
        """Check a fact.

        :param p_line: line of fact to check.
        """
        fact = self._facts.get_item(p_line)
        assert fact is not None
        fact.check()

    def clear(self) -> None:
        """Clear each fact in facts outline. """
        for line in self._facts.lines():
            self.clear_fact(line)

    def clear_fact(self, p_i: LineOutline) -> None:
        """Clear a fact.

        :param p_i: line of fact to clear.
        """
        fact = self._facts.get_item(p_i)
        assert fact is not None
        fact.clear()

    @property
    def facts(self) -> OutlineFacts:
        """Return facts outline."""
        return self._facts

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        if super().is_stale():
            return True

        for fact in self:
            if fact.is_stale():
                self._stale = True
                return True

        return False

    # @property
    # def name(self) -> NameTopic:
    #     """Return topic name."""
    #     return self._name

    def set_fresh(self) -> None:
        """Mark topic in memory consistent with file contents."""
        super().set_fresh()
        for fact in self:
            fact.set_fresh()

    # @property
    # def summary(self) -> SummaryTopic:
    #     """Return topic summary."""
    #     return self._summary

    @property
    def tag(self) -> TagTopic:
        """Return topic identifier. """
        return self._tag

    # @property
    # def title(self) -> TitleTopic:
    #     """Return topic title."""
    #     return self._title
