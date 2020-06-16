"""
Defines abstract classes and interfaces for identification information.

:doc:`../guide/devel_notes` describes the use of abstract classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_infoid`` defines abstract text attribute
classes for :class:`.InfoId` and :class:`.ViewInfoId`.

See :class:`.InfoId`, :class:`.ViewInfoId`, and derived classes.

.. data:: AbstractTextView

    Abstract type that represents display of a text attribute such as a
    factsheet name or summary.
"""
import abc
import typing

from factsheet.abc_types import abc_stalefile as ABC_STALE

AbstractTextView = typing.TypeVar('AbstractTextView')


class AbstractTextModel(ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to model text attributes.

    .. tip:: Two text attributes are equivalent when their string
       representations are the same.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when other is text attribute with same string
        representation.
        """
        if not isinstance(px_other, AbstractTextModel):
            return False

        return str(self) == str(px_other)

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return attribute contents as text."""
        raise NotImplementedError

    @abc.abstractmethod
    def attach_view(self, pm_view: AbstractTextView):
        """Add view to update display when text changes.

        :param pm_view: view to add.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def detach_view(self, pm_view: AbstractTextView):
        """Remove view of changes to text.

        :param pm_view: view to removes.
        """
        raise NotImplementedError


class InterfaceViewInfoId(abc.ABC):
    """Defines interface to attach identification information view
    (:class:`.ViewInfoId`) to the model (:class:`.InfoId`).
    """

    @abc.abstractmethod
    def get_view_name(self) -> AbstractTextView:
        """Return view's name display element."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_summary(self) -> AbstractTextView:
        """Return view's summary display element."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_title(self) -> AbstractTextView:
        """Return view's title display element."""
        raise NotImplementedError
