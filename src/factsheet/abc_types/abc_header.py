"""
Defines abstract data type classes for factsheet headers.
"""

import abc
import typing

from factsheet.abc_types import abc_view as AVIEW


class InterfaceStaleFile(abc.ABC):
    """Defines interfaces to detect when a stored model is out of date."""

    @abc.abstractmethod
    def is_fresh(self):
        """Return True when there are no unsaved changes to model."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_stale(self):
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


class AbstractTextModel(InterfaceStaleFile):
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


class FactoryHeader(abc.ABC):
    """Defines abstract factory to produce components for Header classes."""

    @abc.abstractmethod
    def new_title_model(self):
        """Return new instance of Model class Title."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_title_view(self):
        """Return new instance of View class Title."""
        raise NotImplementedError
