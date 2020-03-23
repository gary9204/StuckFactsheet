"""
Defines abstract data type classes for identification information.

See :class:`.model.InfoId` and derived classes.
"""
import abc
import typing

from factsheet.abc_types import abc_stalefile as ABC_STALE
from factsheet.abc_types import abc_view as AVIEW


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
    def attach_view(self, pm_view: AVIEW.AbstractTextView):
        """Add view to update display when text changes."""
        raise NotImplementedError

    @abc.abstractmethod
    def detach_view(self, pm_view: AVIEW.AbstractTextView):
        """Remove view of changes to text."""
        raise NotImplementedError
