"""
Defines abstract data types classes for factsheet documents.
"""
import abc
import enum

from factsheet.view import view_infoid as VINFOID

ALLOWED = True


class EffectSafe(enum.Enum):
    """Constants to identify the effect of a call to a safe method (such
    as :meth:`.control.Sheet.detach_page_safe` and
    :meth:`.control.Sheet.delete_safe`).
    """
    #: Method call completed request.
    COMPLETED = enum.auto()
    #: Method call had no effect.
    NO_EFFECT = enum.auto()


class InterfacePageSheet(abc.ABC):
    """Defines interface for :class:`.model.Sheet` to signal
    :class:`.view.PageSheet`.
    """

    @abc.abstractmethod
    def close_page(self) -> None:
        """Respond to notice to close_page view from model."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        raise NotImplementedError

    @abc.abstractmethod
    def update_name(self) -> None:
        """Respond to notice of factsheet name change."""
        raise NotImplementedError
