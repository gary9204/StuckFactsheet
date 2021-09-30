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

import factsheet.model.aspect as MASPECT
import factsheet.model.idcore as MIDCORE

import factsheet.bridge_ui as BUI

NameFact = BUI.ModelTextMarkup
SummaryFact = BUI.ModelGtkTextBuffer
TitleFact = BUI.ModelTextMarkup
ViewNameFactActive = BUI.ViewTextMarkup
ViewNameFactPassive = BUI.ViewTextDisplay
ViewSummaryFactActive = BUI.ViewTextTagged
ViewSummaryFactPassive = BUI.ViewTextTagged
ViewTitleFactActive = BUI.ViewTextMarkup
ViewTitleFactPassive = BUI.ViewTextDisplay

NamesAspects = BUI.BridgeOutlineSelect[str]
ViewNamesAspects = BUI.ViewOutlineSelect

NoteFact = BUI.ModelTextMarkup
ViewNoteFact = BUI.ViewTextMarkup

AspectStatus = MASPECT.AspectPlain
ViewAspectStatus = MASPECT.ViewAspectPlain

TagFact = typing.NewType('TagFact', int)
AspectTagFact = MASPECT.AspectPlain
ViewAspectTagFact = MASPECT.ViewAspectPlain

ValueOpaque = typing.TypeVar('ValueOpaque')
AspectValuePlain = MASPECT.AspectPlain

TopicOpaque = typing.TypeVar('TopicOpaque')


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
           MIDCORE.IdCore[ViewNameFactActive, ViewNameFactPassive,
                          ViewSummaryFactActive, ViewSummaryFactPassive,
                          ViewTitleFactActive, ViewTitleFactPassive]):
    """Fact component of Factsheet :mod:`~.factsheet.model`.

    Class ``Fact`` represents a fact about a specific subject within a
    Factsheet.  The model of a fact consists of value, status,
    user-specified note, and tag along with identity information.

    The value of a fact depends on its context, that is, its topic (for
    example, True for associative property of modular addition, 0 for
    the size of the empty set, or the elements in a set).  The fact's
    status indicates whether the user has checked the fact and, if so,
    whether the fact's value is defined.

    A fact tag serves to uniquely identify the fact at run time.  See
    :class:`.IdCore` for persistent identity information.

    Each fact provides one or more aspects. An aspect presents a fact's
    value in a particular format.

    .. admonition:: About Equality

        Two facts are equivalent when they have the same status, value,
        aspects, note, and identity attributes.  Transient aspects of
        the facts (like tags and views) are not compared and may be
        different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same topic, value, status, note,
        aspects, and identity information.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._topic != p_other._topic:
            return False

        if self._aspects != p_other._aspects:
            return False

        if self._names_aspects != p_other._names_aspects:
            return False

        if self._note != p_other._note:
            return False

        if self._status != p_other._status:
            return False

        if self._value != p_other._value:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return fact in form pickle can persist.

        Persistent form of fact excludes run-time information.
        """
        state = super().__getstate__()
        del state['_tag']
        return state

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 p_topic: TopicOpaque, **kwargs: typing.Any
                 ) -> None:
        """Initialize fact with topic and identity information.

        :param p_name: short identifier for fact.
        :param p_summary: description of fact, which adds detail to
            title.
        :param p_title: one-line description of fact.
        :param p_topic: context for fact.
        """
        super().__init__(
            p_name=p_name, p_summary=p_summary, p_title=p_title, **kwargs)
        self._aspects: typing.MutableMapping[str, MASPECT.Aspect] = dict()
        self._aspect_missing = AspectValuePlain()
        WARNING = 'This fact does not support the aspect you requested'
        self._aspect_missing.set_presentation(p_subject=WARNING)
        self._names_aspects = NamesAspects()
        self._note = NoteFact()
        self._status = StatusOfFact.UNDEFINED
        self._aspect_status = AspectStatus()
        self._aspect_status.set_presentation(p_subject=self._status.name)
        self._tag = TagFact(id(self))
        self._aspect_tag = AspectTagFact()
        self._aspect_tag.set_presentation(p_subject=self._tag)
        self._topic = p_topic
        self._value: typing.Optional[ValueOpaque] = None
        self.add_aspect_value(p_name='Plain', p_aspect=AspectValuePlain())

    def __setstate__(self, p_state: typing.Dict) -> None:
        """Reconstruct fact from state pickle loads.

        Reconstructed fact is marked fresh.

        :param p_state: unpickled state of stored fact.
        """
        super().__setstate__(p_state)
        self._tag = TagFact(id(self))

    def add_aspect_value(
            self, p_name: str, p_aspect: MASPECT.Aspect[ValueOpaque]):
        """Add aspect to present value.

        :param p_name: name of presentation.
        :param p_aspect: presentation to add.
        """
        self._aspects[p_name] = p_aspect
        self._names_aspects.insert_before(p_item=p_name)

    def check(self) -> StatusOfFact:
        """Mark fact stale and sync each presentation with fact value.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should determine fact value, set status accordingly, and then
        call base class method.
        """
        self.set_stale()
        for aspect in self._aspects.values():
            aspect.set_presentation(self._value)
        return self._status

    def clear(self) -> StatusOfFact:
        """Mark fact as stale and clear fact value and presentations.

        Subclasses must extend :meth:`~.Fact.check` method.  A subclass
        should set fact status and call base class method.
        """
        self.set_stale()
        self._value = None
        for aspect in self._aspects.values():
            aspect.clear_presentation()
        return self._status

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to fact."""
        if super().is_stale():
            return True

        if self.note.is_stale():
            self._stale = True
            return True

        return False

    def _new_model(self) -> typing.Tuple[NameFact, SummaryFact, TitleFact]:
        """Return (name, summary, title) store."""
        name = NameFact()
        summary = SummaryFact()
        title = TitleFact()
        return name, summary, title

    def new_view_aspect(self, p_name_aspect: str) -> BUI.ViewAny:
        """Return view of aspect with given name or placeholder if name
        not found.

        :param p_name_aspect: name of desired aspect.
        """
        aspect = self._aspects.get(p_name_aspect, self._aspect_missing)
        return aspect.new_view()

    def new_view_names_aspects(self) -> ViewNamesAspects:
        """Return view of names of aspects for the fact."""
        return self._names_aspects.new_view()

    def new_view_note(self) -> ViewNoteFact:
        """Return view of fact's note."""
        return self._note.new_view()

    def new_view_status(self) -> ViewAspectStatus:
        """Return view of fact's status."""
        return self._aspect_status.new_view()

    def new_view_tag(self) -> ViewAspectTagFact:
        """Return view of fact's tag."""
        return self._aspect_tag.new_view()

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
    def tag(self) -> TagFact:
        """Return fact identifier. """
        return self._tag

    @property
    def value(self) -> typing.Optional[ValueOpaque]:
        """Return fact value."""
        return self._value
