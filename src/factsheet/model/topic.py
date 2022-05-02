"""
Defines topic-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
the base class representing the model of a topic.  Additional classes
specialize the model for sets, operations, and so on.
"""
import typing

import factsheet.bridge_ui as BUI
# import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE

TagTopic = typing.NewType('TagTopic', int)
LineOutline = BUI.LineOutline
# OutlineFacts = BUI.BridgeOutlineColumnar[MFACT.Fact]

Name = BUI.ModelTextMarkup
DisplayName = BUI.DisplayTextMarkup
FactoryDisplayName = BUI.FactoryDisplayTextMarkup
EditorName = BUI.EditorTextMarkup
FactoryEditorName = BUI.FactoryEditorTextMarkup

Summary = BUI.ModelTextStyled
DisplaySummary = BUI.DisplayTextStyled
FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
EditorSummary = BUI.EditorTextStyled
FactoryEditorSummary = BUI.FactoryEditorTextStyled

Title = BUI.ModelTextMarkup
DisplayTitle = BUI.DisplayTextMarkup
FactoryDisplayTitle = BUI.FactoryDisplayTextMarkup
EditorTitle = BUI.EditorTextMarkup
FactoryEditorTitle = BUI.FactoryEditorTextMarkup


class Topic(MIDCORE.IdCore[Name, Summary, Title]):
    """Topic component of Factsheet :mod:`~factsheet.model`.

    Class :class:`Topic` represents a specific subject within a Factsheet.
    A model topic consists of an outline of facts along with
    identification information (see :class:`.IdCore`).  Each fact
    represents a statement about the topic's subject.

    .. admonition:: About Equality

        Each topic model has persistent identification information
        and a fact outline.  In addition, a topic model may have
        transient aspects such as change state with respect to file
        storage,

        Two topics are equal when their identification information
        are equal and their fact outlines are equal.  Transient
        aspects of the factsheets are not compared and may be different.
    """

    def __contains__(self, p_fact) -> bool:
        """Return True when fact is in facts outline."""
        raise NotImplementedError
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

        # if self._facts != p_other._facts:
        #     return False

        return True

    # def __getstate__(self) -> typing.Dict:
    #     """Return topic model in form pickle can persist.
    #
    #     Persistent form of topic excludes run-time information.
    #     """
    #     raise NotImplementedError
    #     state = super().__getstate__()
    #     del state['_tag']
    #     return state

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 **kwargs: typing.Any) -> None:
        """Initialize topic with given identity and no facts.

        :param p_name: name of topic.
        :param p_summary: summary of topic.
        :param p_title: title of topic.
        :param kwargs: superclass keyword parameters.
        """
        self._name = Name(p_text=p_name)
        self._summary = Summary(p_text=p_summary)
        self._title = Title(p_text=p_title)
        super().__init__(**kwargs)
        # self._facts = OutlineFacts()

    def __iter__(self) -> typing.Iterator:
        """Return iterator over facts in facts outline.

        Iterator skips lines that contain None.
        """
        raise NotImplementedError
        for fact in self._facts.items():
            if fact is not None:
                yield fact

    # def __setstate__(self, p_state: typing.Dict) -> None:
    #     """Reconstruct topic model from state pickle loads.
    #
    #     Reconstructed attribute is marked fresh.
    #
    #     :param p_state: unpickled state of stored topic model.
    #     """
    #     raise NotImplementedError
    #     super().__setstate__(p_state)
    #     self._tag = TagTopic(id(self))

    def append_fact(self, p_fact) -> None:
        """Add new fact to the end of facts outline.

        Do not add a fact already in the outline.

        :param p_fact: new fact to add.
        """
        raise NotImplementedError
        if p_fact in self:
            return

        _index = self._facts.insert_before(p_fact)
        self.set_stale()

    def append_outline_facts(self, p_topic: 'Topic') -> None:
        """Add other topic's facts outline to the end of facts outline.

        Do not add any fact already in the outline.

        :param p_topic: topic containing facts outline to add.
        """
        raise NotImplementedError
        for fact in p_topic:
            self.append_fact(fact)

    def check_fact(self, p_line: LineOutline) -> None:
        """Check a fact.

        :param p_line: line of fact to check.
        """
        raise NotImplementedError
        fact = self._facts.get_item(p_line)
        assert fact is not None
        fact.check()

    def clear(self) -> None:
        """Clear each fact in facts outline. """
        raise NotImplementedError
        for line in self._facts.lines():
            self.clear_fact(line)

    def clear_fact(self, p_i: LineOutline) -> None:
        """Clear a fact.

        :param p_i: line of fact to clear.
        """
        raise NotImplementedError
        fact = self._facts.get_item(p_i)
        assert fact is not None
        fact.clear()

    @property
    def facts(self):
        """Return facts outline."""
        raise NotImplementedError
        return self._facts

    @property
    def tag(self) -> TagTopic:
        """Return unique identifier of topic."""
        return TagTopic(id(self))

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        if super().is_stale():
            return True

        # for fact in self:
        #     if fact.is_stale():
        #         self._stale = True
        #         return True

        return False

    def set_fresh(self) -> None:
        """Mark topic in memory consistent with file contents."""
        super().set_fresh()
        # for fact in self:
        #     fact.set_fresh()

    # @property
    # def tag(self) -> TagTopic:
    #     """Return topic identifier. """
    #     raise NotImplementedError
    #     return self._tag
