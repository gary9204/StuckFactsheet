"""
Defines abstract interfaces for facts.

:doc:`../guide/devel_notes` describes the use of abstract classes to
break ``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_fact`` defines interface for fact view (:class:`.PaneFact`) for
encapsulation.
"""
import abc
import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_stalefile as ABC_STALE


IdFact = typing.NewType('IdFact', int)


class AbstractFact(ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to fact model components."""

    @property
    @abc.abstractmethod
    def id_fact(self) -> IdFact:
        """Return fact identifier. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return fact name. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def summary(self) -> str:
        """Return fact summary. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """Return fact title. """
        raise NotImplementedError


class InterfacePaneFact(abc.ABC):
    """Defines interface for :class:`~.Fact` model to
    signal :class:`~.PaneFact`.
    """

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of fact identification information."""
        raise NotImplementedError
