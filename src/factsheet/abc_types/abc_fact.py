"""
Defines abstract interfaces for facts.

:doc:`../guide/devel_notes` describes the use of abstract classes to
break ``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_fact`` defines interface for fact view (:class:`.BlockFact`) for
encapsulation.

.. data:: IdFact

    Type for fact identifiers.

.. data:: NameScene

    Type for name of presentation style for a fact value.

..
    data:: ValueAny

    Generic type for fact value without fact status.

..
    data:: ValueOpaque

    Generic type for fact value.
"""
import enum
import abc
import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_stalefile as ABC_STALE


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
    UNCHECKED = enum.auto()
    UNDEFINED = enum.auto()
    DEFINED = enum.auto()


TagFact = typing.NewType('TagFact', int)
NameScene = typing.NewType('NameScene', str)
TopicOpaque = typing.TypeVar('TopicOpaque')
ValueOpaque = typing.TypeVar('ValueOpaque')


class AbstractFact(
        ABC_INFOID.AbstractIdentity[TagFact], ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to fact model components."""

    @abc.abstractmethod
    def check(self) -> StatusOfFact:
        """Return status of fact check after setting fact value and status."""
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        """Clear fact value and status of fact."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def status(self) -> StatusOfFact:
        """Return status of fact. """
        raise NotImplementedError


class InterfaceBlockFact(abc.ABC, typing.Generic[ValueOpaque]):
    """Defines interface for :class:`~.Fact` model to signal
    :class:`~.BlockFact`.
    """

    @abc.abstractmethod
    def update(self, p_status: StatusOfFact, p_value: ValueOpaque) -> None:
        """Update view with new fact status and value.

        :param p_status: new status of fact.
        :param p_value: new value of fact.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of fact identification information."""
        raise NotImplementedError
