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

from factsheet.abc_types.abc_fact import IdFact
from factsheet.abc_types.abc_fact import StatusOfFact
from factsheet.abc_types.abc_fact import ValueOfFact

logger = logging.getLogger('Main.model.fact')


class Fact(ABC_FACT.AbstractFact, typing.Generic[ValueOfFact]):
    """Fact component of Factsheet :mod:`~.factsheet.model`.

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

    def __call__(self) -> typing.Optional[ValueOfFact]:
        """Return fact value.

        If the user has not checked the fact or the fact value is not
        defined, return None.
        """
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
        state = self.__dict__.copy()
        del state['_blocks']
        del state['_stale']
        return state

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', **_kwargs: typing.Any) -> None:
        self._infoid = MINFOID.InfoId(
            p_name=p_name, p_summary=p_summary, p_title=p_title)
        self._value: typing.Optional[ValueOfFact] = None
        self._status = StatusOfFact.BLOCKED
        self._set_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct fact model from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored fact model.
        """
        self.__dict__.update(px_state)
        self._set_transient()

    def _set_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._stale = False
        self._blocks: typing.MutableMapping[
            int, ABC_FACT.InterfaceBlockFact] = dict()

    def attach_block(self, p_block: ABC_FACT.InterfaceBlockFact) -> None:
        """Add fact block to show fact identification, status, and value.

        Log warning when requested block is already attached.

        :param p_block: block to add.
        """
        id_block = id(p_block)
        if id_block in self._blocks.keys():
            logger.warning('Duplicate fact block: {} ({}.{})'
                           ''.format(hex(id_block), self.__class__.__name__,
                                     self.attach_block.__name__))
            return

        self._infoid.attach_view(p_block.get_infoid())
        self._blocks[id_block] = p_block

    def check(self, **_kwargs: typing.Any) -> StatusOfFact:
        """Set fact value and set corresponding state of fact check.

        Base class marks change in fact and notifies attached fact
        blocks.  Base class does not change fact status or value.
        """
        self.set_stale()
        # self._value = None
        # self._status = StatusOfFact.UNDEFINED
        self._update_blocks()
        return self._status

    def clear(self, **_kwargs: typing.Any) -> None:
        """Clear fact value and set corresponding state of fact check.

        Base class marks change in fact and notifies attached fact
        blocks.  Base class does not change fact status or value.
        """
        self.set_stale()
        # self._value = None
        # self._status = StatusOfFact.UNCHECKED
        self._update_blocks()

    def detach_all(self) -> None:
        """Detach all fact blocks from fact."""
        while self._blocks:
            _id_block, block = self._blocks.popitem()
            self._infoid.detach_view(block.get_infoid())
        #     self._detach_attribute_views(view)

    def detach_block(self, p_block: ABC_FACT.InterfaceBlockFact) -> None:
        """Remove one fact block from fact.

        Log warning when requested block is not attached.

        :param p_block: block to remove.
        """
        id_block = id(p_block)
        try:
            _ = self._blocks.pop(id_block)
        except KeyError:
            logger.warning('Missing fact block: {} ({}.{})'
                           ''.format(hex(id_block), self.__class__.__name__,
                                     self.detach_block.__name__))
            return

        # self._detach_attribute_blocks(p_block)
        self._infoid.detach_view(p_block.get_infoid())

    # def _detach_attribute_views(self, p_block: ABC_FACT.InterfaceBlockFact
    #                             ) -> None:
    #     """For each fact attribute with a distinct view, remove the
    #     view from the block.
    #
    #     :param pm_view: view of topic as a whole.
    #     """
    #     self._infoid.detach_view(p_block.get_infoid())

    @property
    def id_fact(self) -> IdFact:
        """Return fact identifier. """
        return IdFact(self._infoid.id_model)

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
    def status(self) -> StatusOfFact:
        """Return status of fact check."""
        return self._status

    @property
    def name(self) -> str:
        """Return fact name."""
        return self._infoid.name

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

    @property
    def summary(self) -> str:
        """Return fact summary."""
        return self._infoid.summary

    @property
    def title(self) -> str:
        """Return fact title."""
        return self._infoid.title

    def _update_blocks(self) -> None:
        """Notifiy all fact blocks of new status and value."""
        for block in self._blocks.values():
            block.update(self._status, self._value)
