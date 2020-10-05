"""
Defines interface to track factsheet file contents against in-memory
model.
"""
import abc


class InterfaceStaleFile(abc.ABC):
    """Interface to detect when a stored model is out of date."""

    @abc.abstractmethod
    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to model."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to model."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_fresh(self):
        """Mark model in memory consistent with file contents."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_stale(self):
        """Mark model in memory changed from file contents."""
        raise NotImplementedError
