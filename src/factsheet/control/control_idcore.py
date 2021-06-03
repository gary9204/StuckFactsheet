"""
Defines generic control to produce views of :class:`~.IdCore`
identity attributes.
"""
import abc
import typing   # noqa

import factsheet.model.idcore as MIDCORE


class ControlIdCore(typing.Generic[
        MIDCORE.ViewNameActive, MIDCORE.ViewNamePassive,
        MIDCORE.ViewSummaryActive, MIDCORE.ViewSummaryPassive,
        MIDCORE.ViewTitleActive, MIDCORE.ViewTitlePassive], abc.ABC):
    """Mediates addition of views of identity attributes."""

    @abc.abstractmethod
    def new_view_name_active(self) -> MIDCORE.ViewNameActive:
        """Return editable view of name."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_name_passive(self) -> MIDCORE.ViewNamePassive:
        """Return display-only view of name."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_summary_active(self) -> MIDCORE.ViewSummaryActive:
        """Return editable view of summary."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_summary_passive(self) -> MIDCORE.ViewSummaryPassive:
        """Return display-only view of summary."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_title_active(self) -> MIDCORE.ViewTitleActive:
        """Return editable view of title."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_title_passive(self) -> MIDCORE.ViewTitlePassive:
        """Return display-only view of title."""
        raise NotImplementedError
