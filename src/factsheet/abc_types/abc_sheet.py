"""
Defines abstract data types classes for factsheet documents.
"""
import abc

from factsheet.view import view_infoid as VINFOID

ALLOWED = True
CONTINUE_GTK = False


class InterfacePageSheet(abc.ABC):
    """Defines interface for :class:`.model.Sheet` to signal
    :class:`.view.PageSheet`.
    """

    @abc.abstractmethod
    def detach(self) -> None:
        """Respond to notice to detach view from model."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of factsheet identification information."""
        raise NotImplementedError

    @abc.abstractmethod
    def update_name(self) -> None:
        """Respond to notice of factsheet name change."""
        raise NotImplementedError
