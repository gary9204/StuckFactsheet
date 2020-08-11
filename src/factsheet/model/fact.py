"""
Defines fact-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``fact`` defines
the base class representing the model of a fact.  Additional classes
specialize the model for facts about sets, operations, and so on.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_fact as ABC_FACT
from factsheet.model import infoid as MINFOID

logger = logging.getLogger('Main.model.fact')

ValueAny = typing.TypeVar('ValueAny')
StatusOfFact = ABC_FACT.StatusOfFact


class Fact(typing.Generic[ValueAny]):
    """Fact component of Factsheet :mod:`~factsheet.model`.

    Class ``Fact`` represents a fact about a specific subject within a
    Factsheet. A model fact consists of value along with identification
    information (see :class:`.InfoId`.) A fact's value may be unknown or
    undefined.  A fact value that is both known and defined depends on
    the fact in context of its topic (for example, True for associateive
    property of modular addition, 0 for the size of the empty set, or
    the elements in a set).

    :param p_name: name of fact.
    :param p_summary: summary of fact.
    :param p_title: title of fact.

    .. admonition:: About Equality

        Two facts are equivalent when they have the same value
        attributes and identification information. Transient aspects of
        the facts (like views) are not compared and may be different.
    """

    def __call__(self) -> typing.Optional[ValueAny]:
        """Return fact value or None.

        Return None when the the user has not checked the fact or the
        fact value is not defined.
        """
        if self._state_of_check is not ABC_FACT.StatusOfFact.DEFINED:
            return None

        return self._value

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same fact information.

        :param px_other: object to compare with self.
        """
        raise NotImplementedError
        # if not isinstance(px_other, Topic):
        #     return False

        # if self._infoid != px_other._infoid:
        #    return False

        # return True

    def __getstate__(self) -> typing.Dict:
        """Return fact model in form pickle can persist.

        Persistent form of fact excludes run-time information.
        """
        raise NotImplementedError
        # state = self.__dict__.copy()
        # del state['_views']
        # del state['_stale']
        # return state

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', **_kwargs: typing.Dict) -> None:
        self._infoid = MINFOID.InfoId(
            p_name=p_name, p_summary=p_summary, p_title=p_title)
        self._value: typing.Optional[ValueAny] = None
        self._state_of_check = ABC_FACT.StatusOfFact.UNCHECKED
        self._set_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct fact model from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored fact model.
        """
        raise NotImplementedError
        # self.__dict__.update(px_state)
        # self._set_transient()

    def _set_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._stale = False
        self._views: typing.Dict[int, ABC_FACT.InterfacePaneFact] = dict()

    def attach_view(self, pm_view: ABC_FACT.InterfacePaneFact) -> None:
        """Add view to show fact status and value.

        Log warning when requested view is already attached.

        :param pm_view: view to add.
        """
        raise NotImplementedError
        # id_view = id(pm_view)
        # if id_view in self._views.keys():
        #     logger.warning(
        #         'Duplicate view: {} ({}.{})'.format(
        #             hex(id_view),
        #             self.__class__.__name__, self.attach_view.__name__))
        #     return

        # self._infoid.attach_view(pm_view.get_infoid())
        # self._views[id_view] = pm_view

    def check(self, **_kwargs: typing.Mapping[str, typing.Any]
              ) -> ABC_FACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._state_of_check = ABC_FACT.StatusOfFact.UNDEFINED
        self.set_stale()
        return self._state_of_check

    def clear(self, **_kwargs: typing.Mapping[str, typing.Any]) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._state_of_check = ABC_FACT.StatusOfFact.UNCHECKED
        self.set_stale()

    def detach_all(self) -> None:
        """Detach all views from topic."""
        raise NotImplementedError
        # while self._views:
        #     _id_view, view = self._views.popitem()
        #     self._detach_attribute_views(view)

    def detach_view(self, px_view: ABC_FACT.InterfacePaneFact) -> None:
        """Remove one view from fact.

        Log warning when requested view is not attached.

        :param px_view: view to remove.
        """
        raise NotImplementedError
        # id_view = id(px_view)
        # try:
        #     self._views.pop(id_view)
        # except KeyError:
        #     logger.warning(
        #         'Missing view: {} ({}.{})'.format(
        #             hex(id_view),
        #             self.__class__.__name__, self.detach_view.__name__))
        #     return

        # self._detach_attribute_views(px_view)

    def _detach_attribute_views(self, pm_view: ABC_FACT.InterfacePaneFact
                                ) -> None:
        """For each fact attribute with a distinct view, remove the
        view for the attribute.

        :param pm_view: view of topic as a whole.
        """
        raise NotImplementedError
        # self._infoid.detach_view(pm_view.get_infoid())

    @property
    def id_fact(self) -> ABC_FACT.IdFact:
        """Return fact identifier. """
        return ABC_FACT.IdFact(self._infoid.id_model)

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to fact."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        fact.
        """
        if self._stale:
            return True

        if self._infoid.is_stale():
            self._stale = True
            return True

        return False

    @property
    def state_of_check(self) -> ABC_FACT.StatusOfFact:
        """Return status of fact check."""
        return self._state_of_check

    # @property
    def name(self) -> str:
        """Return fact name."""
        raise NotImplementedError
        # return self._infoid.name

    # @property
    def note(self) -> str:
        """Return user note for fact."""
        raise NotImplementedError
        # return self._note

    def set_fresh(self) -> None:
        """Mark fact in memory consistent with file contents."""
        self._stale = False
        self._infoid.set_fresh()

    def set_stale(self) -> None:
        """Mark fact in memory changed from file contents."""
        self._stale = True

    # @property
    def summary(self) -> str:
        """Return fact summary."""
        raise NotImplementedError
        # return self._infoid.summary

    # @property
    def title(self) -> str:
        """Return fact title."""
        raise NotImplementedError
        # return self._infoid.title
