"""
Defines abstract data type classes for factsheet headers.
"""

import abc


class InterfaceStaleFile(abc.ABC):
    """Defines interfaces to detect when a stored model is out of date."""

    @abc.abstractmethod
    def is_fresh(self):
        """Return True when there are not unsaved changes to model."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_stale(self):
        """Return True when there is at least one unsaved change to model."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_fresh(self):
        """Mark the model in memory consistent with model in file."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_stale(self):
        """Mark the model in memory changed from model in file."""
        raise NotImplementedError
