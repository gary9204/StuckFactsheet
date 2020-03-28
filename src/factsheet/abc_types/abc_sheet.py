"""
Defines abstract data types classes for factsheet documents.
"""
import abc
import enum
from pathlib import Path
import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID


class EffectSafe(enum.Enum):
    """Constants to identify the effect of a call to a safe method (such
    as :meth:`.control.Sheet.detach_page_safe` and
    :meth:`.control.Sheet.delete_safe`).
    """
    #: Method call completed request.
    COMPLETED = enum.auto()
    #: Method call had no effect.
    NO_EFFECT = enum.auto()


class InterfaceControlSheet(abc.ABC):
    """Defines interface class to break import cycle between
    :class:`~.control.sheet.Sheet` and :class:`.PoolSheets`.
    """
    @property
    @abc.abstractmethod
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        raise NotImplementedError


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

    @abc.abstractmethod
    def present(self, p_time: int) -> None:
        """Make the page visible to user.

        Presents page to user even when page is an icon or covered by
        other windows.

        :param p_time: timestamp of event requesting presentation.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_titles(self, p_subtitle: str) -> None:
        """Set title and subtitle of page's window.

        The page's title is the factsheet name.

        :param p_subtitle: subtitle for window.
        """
        raise NotImplementedError
