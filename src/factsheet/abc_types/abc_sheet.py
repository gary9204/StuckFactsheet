"""
Defines abstract data types classes for factsheet documents.
"""
import abc

ALLOWED = True
CONTINUE_GTK = False


class InterfaceSignalsSheet(abc.ABC):
    """Defines interface for :class:`.model.Sheet` to signal
    :class:`.view.PageSheet`.
    """

    @abc.abstractmethod
    def update_name(self) -> None:
        """Respond to notice of factsheet name change."""
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self) -> None:
        """Respond to notice to detach view from model."""
        raise NotImplementedError
