"""
Defines fact-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``fact`` defines
the base class representing the model of a fact.  Additional classes
specialize the model for facts about sets, operations, and so on.
"""
import enum
import typing

import factsheet.model.idcore as MIDCORE

import factsheet.bridge_ui as BUI

Aspect = BUI.BridgeAspect
AspectValuePlain = BUI.BridgeAspectPlain[typing.Any]
NamesAspect = BUI.BridgeOutlineSelect[str]
NameFact = BUI.BridgeTextMarkup
NameTopic = BUI.BridgeTextMarkup
NoteFact = BUI.BridgeTextFormat
PersistAspectStatus = BUI.PersistAspectPlain
SummaryFact = BUI.BridgeTextFormat
SummaryTopic = BUI.BridgeTextFormat
TagFact = typing.NewType('TagFact', int)
TagTopic = typing.NewType('TagTopic', int)
TitleFact = BUI.BridgeTextMarkup
TitleTopic = BUI.BridgeTextMarkup
TopicOpaque = typing.TypeVar('TopicOpaque')
ValueOpaque = typing.TypeVar('ValueOpaque')


class StatusOfFact(enum.Enum):
    """Indicates whether user has checked fact and outcome of check.

    .. attribute:: BLOCKED

        Fact cannot be checked because, for example, prerequisite
        information is unavailable.

    .. attribute:: DEFINED

        User checked fact and its value is defined.

    .. attribute:: UNCHECKED

        User has not checked fact and its value is unknown.

    .. attribute:: UNDEFINED

        User checked fact but its value is not defined.
    """
    BLOCKED = enum.auto()
    DEFINED = enum.auto()
    UNCHECKED = enum.auto()
    UNDEFINED = enum.auto()


class AspectStatus(BUI.BridgeAspectPlain[StatusOfFact]):
    """Plain text aspect for status of fact."""

    def transcribe(self, p_source: typing.Optional[StatusOfFact]
                   ) -> PersistAspectStatus:
        """Return persistent representation of status.

        When source is None, return empty plain text.

        :param p_source: status metadata for aspect.
        """
        persist = StatusOfFact.UNCHECKED.name
        if p_source is not None:
            persist = p_source.name
        return persist


class Fact(typing.Generic[TopicOpaque, ValueOpaque],
           MIDCORE.IdCore[NameFact, SummaryFact, TitleFact]
           ):
    """Fact component of Factsheet :mod:`~.factsheet.model`.

    Class ``Fact`` represents a fact about a specific subject within a
    Factsheet. A model fact consists of value along with identity
    information (see :class:`.IdCore`.) A fact's value may be unknown or
    undefined.  A fact value that is both known and defined depends on
    the fact in context of its topic (for example, True for associative
    property of modular addition, 0 for the size of the empty set, or
    the elements in a set).

    .. admonition:: About Equality

        Two facts are equivalent when they have the same status, value,
        aspects, note, and identity attributes.  Transient aspects of
        the facts (like tags and views) are not compared and may be
        different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same status, value, aspects,
        and identity.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if not self._aspects == p_other._aspects:
            return False

        if self.note != p_other.note:
            return False

        if self.status != p_other.status:
            return False

        if self.value != p_other.value:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return fact in form pickle can persist.

        Persistent form of fact excludes run-time information.
        """
        state = super().__getstate__()
        del state['_tag']
        return state

    def __init__(self, *, p_topic: TopicOpaque, **kwargs: typing.Any
                 ) -> None:
        super().__init__(**kwargs)
        self._aspects: typing.Dict[str, Aspect] = dict()
        self._name = NameFact()
        self._names_aspect = NamesAspect()
        self._note = NoteFact()
        self._status = StatusOfFact.BLOCKED
        self._summary = SummaryFact()
        self._tag = TagFact(id(self))
        self._title = TitleFact()
        self._topic = p_topic
        self._value: typing.Optional[ValueOpaque] = None
        self._init_aspects()

    def _init_aspects(self) -> None:
        """Populate fact's aspects and aspect names."""
        self._aspects['Plain'] = AspectValuePlain()
        self._names_aspect.insert_before('Plain', None)
        self._aspects['Status'] = AspectStatus()
        self._names_aspect.insert_before('Status', None)

    def __setstate__(self, p_state: typing.Dict) -> None:
        """Reconstruct fact from state pickle loads.

        Reconstructed fact is marked fresh.

        :param p_state: unpickled state of stored fact.
        """
        super().__setstate__(p_state)
        self._tag = TagFact(id(self))

    def check(self) -> StatusOfFact:
        """Determine fact value, if possible, and set corresponding status.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should set fact status and value and then call base class
        method.  Base class marks change in fact and sets fact aspects
        to current value.
        """
        self.set_stale()
        self._aspects['Plain'].refresh(self._value)
        self._aspects['Status'].refresh(self._status)
        return self._status

    def clear(self) -> None:
        """Clear fact status and value.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should set fact status and value and then call base class
        method.  Base class marks change in fact and sets fact aspects
        to current value.
        """
        self.set_stale()
        self._aspects['Plain'].refresh(None)
        self._aspects['Status'].refresh(None)

    def get_aspect(self, p_name: str) -> typing.Optional[Aspect]:
        """Return aspect with given name or placeholder for missing aspect.

        :param p_name: name of desired aspect.
        """
        return self._aspects.get(p_name, None)

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        fact.
        """
        if super().is_stale():
            return True

        if self.note.is_stale():
            self._stale = True
            return True

        return False

    @property
    def name(self) -> NameFact:
        """Return fact name."""
        return self._name

    @property
    def names_aspect(self) -> NamesAspect:
        """Return names of fact's aspects."""
        return self._names_aspect

    @property
    def name_topic(self) -> NameTopic:
        """Return topic name."""
        try:
            name = getattr(self._topic, 'name')
        except AttributeError:
            name = NameTopic()
            name.text = 'Malformed topic! please report.'
        return name

    @property
    def note(self) -> NoteFact:
        """Return user note for fact."""
        return self._note

    def set_fresh(self) -> None:
        """Mark fact in memory consistent with file contents."""
        super().set_fresh()
        self._note.set_fresh()

    @property
    def status(self) -> StatusOfFact:
        """Return status of fact check."""
        return self._status

    @property
    def summary(self) -> SummaryFact:
        """Return fact summary."""
        return self._summary

    @property
    def summary_topic(self) -> SummaryTopic:
        """Return topic summary."""
        try:
            summary = getattr(self._topic, 'summary')
        except AttributeError:
            summary = SummaryTopic()
            summary.text = 'Malformed topic! please report.'
        return summary

    @property
    def tag(self) -> TagFact:
        """Return fact identifier. """
        return self._tag

    @property
    def tag_topic(self) -> TagTopic:
        """Return topic tag."""
        try:
            tag = getattr(self._topic, 'tag')
        except AttributeError:
            TAG_MISSING = -1
            tag = TagTopic(TAG_MISSING)
        return tag

    @property
    def title(self) -> TitleFact:
        """Return fact title."""
        return self._title

    @property
    def title_topic(self) -> TitleTopic:
        """Return topic title."""
        try:
            title = getattr(self._topic, 'title')
        except AttributeError:
            title = TitleTopic()
            title.text = 'Malformed topic! please report.'
        return title

    @property
    def value(self) -> typing.Optional[ValueOpaque]:
        """Return fact value."""
        return self._value
