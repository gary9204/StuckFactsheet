"""
Defines abstract interfaces for facts.

:doc:`../guide/devel_notes` describes the use of abstract classes to
break ``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_fact`` defines interface for fact view (:class:`.PaneFact`) for
encapsulation.

.. data:: IdFact

    Type for fact identifiers.

.. data:: NameScene

    Type for name of presentation style for a fact value.

.. data:: ValueAny

    Generic type for fact value without fact status.

.. data:: ValueOfFact

    Type for fact value including fact status.
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
    BLOCKED = enum.Enum
    UNCHECKED = enum.auto()
    UNDEFINED = enum.auto()
    DEFINED = enum.auto()


IdFact = typing.NewType('IdFact', int)
NameScene = typing.NewType('NameScene', str)
ValueAny = typing.TypeVar('ValueAny')
ValueOfFact = typing.Union[StatusOfFact, ValueAny]


class AbstractFact(ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to fact model components."""

    @property
    @abc.abstractmethod
    def id_fact(self) -> IdFact:
        """Return fact identifier. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def status(self) -> str:
        """Return check status of fact. """
        raise NotImplementedError

    # @property
    # @abc.abstractmethod
    # def name(self) -> str:
    #     """Return fact name. """
    #     raise NotImplementedError

    # @property
    # @abc.abstractmethod
    # def summary(self) -> str:
    #     """Return fact summary. """
    #     raise NotImplementedError

    # @property
    # @abc.abstractmethod
    # def title(self) -> str:
    #     """Return fact title. """
    #     raise NotImplementedError


class InterfacePaneFact(abc.ABC, typing.Generic[ValueAny]):
    """Defines interface for :class:`~.Fact` model to signal
    :class:`~.PaneFact`.
    """

    @abc.abstractmethod
    def checked(self, p_value: ValueOfFact) -> None:
        """Update view with new fact value.

        :param p_value: new fact value.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cleared(self, p_value: ValueOfFact) -> None:
        """Restore view to unchecked or blocked fact status.

        :param p_value: new fact status.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of fact identification information."""
        raise NotImplementedError
