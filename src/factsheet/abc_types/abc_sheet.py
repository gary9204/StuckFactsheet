"""
Defines abstract data types classes for factsheet documents.
"""
import abc
import enum

from factsheet.abc_types import abc_infoid as ABC_INFOID

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
        """Close page in response to notice from model."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of factsheet identification information."""
        raise NotImplementedError

#     @abc.abstractmethod
#     def present(self) -> None:
#         """Make the page visible to user.
# 
#         Presents page to user even when page is an icon or covered by
#         other windows.
#         """
#         raise NotImplementedError

    @abc.abstractmethod
    def update_name(self) -> None:
        """Respond to notice of factsheet name change."""
        raise NotImplementedError
