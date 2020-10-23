"""
Defines fact-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``fact`` defines
the base class representing the model of a fact.  Additional classes
specialize the model for facts about sets, operations, and so on.
"""
import enum
import logging
import typing

import factsheet.model.idcore as MIDCORE

import factsheet.adapt_gtk.adapt as ADAPT

from factsheet.adapt_gtk.adapt import ValueOpaque

NameFact = ADAPT.AdaptTextMarkup
NoteFact = ADAPT.AdaptTextFormat
SummaryFact = ADAPT.AdaptTextFormat
TitleFact = ADAPT.AdaptTextMarkup
TagFact = typing.NewType('TagFact', int)
TopicOpaque = typing.TypeVar('TopicOpaque')


logger = logging.getLogger('Main.model.fact')


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
        formats, note, and identity attributes.  Transient aspects of
        the facts (like tags and views) are not compared and may be
        different.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same status, value, formats,
        and identity.

        :param px_other: object to compare with self.
        """
        if not super().__eq__(px_other):
            return False

        if not self._formats == px_other._formats:
            return False

        if self.note != px_other.note:
            return False

        if self.status != px_other.status:
            return False

        if self.value != px_other.value:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return identity in form pickle can persist.

        Persistent form of fact excludes run-time information.
        """
        state = super().__getstate__()
        del state['_tag']
        return state

    def __init__(self, *, p_topic: TopicOpaque, **kwargs: typing.Any
                 ) -> None:
        super().__init__(**kwargs)
        _ = p_topic  # Needed in every descendant but not base.
        self._formats: typing.Dict[str, ADAPT.FormatValue] = dict(
            Plain=ADAPT.FormatValuePlain())
        self._names_formats = None
        self._name = NameFact()
        self._note = NoteFact()
        self._status = StatusOfFact.BLOCKED
        self._summary = SummaryFact()
        self._tag = TagFact(id(self))
        self._title = TitleFact()
        self._value: typing.Optional[ValueOpaque] = None

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct identity from state pickle loads.

        Reconstructed identity is marked fresh.

        :param px_state: unpickled state of stored identity.
        """
        super().__setstate__(px_state)
        self._tag = TagFact(id(self))

    def check(self) -> StatusOfFact:
        """Determine fact value, if possible, and set corresponding status.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should set fact status and value and then call base class
        method.  Base class marks change in fact and sets fact formats
        to current value.
        """
        self.set_stale()
        for fmt in self._formats.values():
            fmt.set(self._value)
        return self._status

    def clear(self) -> None:
        """Clear fact status and value.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should set fact status and value and then call base class
        method.  Base class marks change in fact and sets fact formats
        to current value.
        """
        self.set_stale()
        for fmt in self._formats.values():
            fmt.clear()

    def get_format(self, p_name: str) -> typing.Optional[ADAPT.FormatValue]:
        """Return format with given name or None if format not supported..

        :param p_name: name of desired format.
        """
        return self._formats.get(p_name)

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
    def names_formats(self) -> None:
        """Return names of formats that the fact provides."""
        return self._names_formats

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
    def tag(self) -> TagFact:
        """Return fact identifier. """
        raise NotImplementedError
        # return self._tag

    @property
    def title(self) -> TitleFact:
        """Return fact title."""
        return self._title

    @property
    def value(self) -> typing.Optional[ValueOpaque]:
        """Return fact title."""
        return self._value
