"""
Defines generic control to add and remove views of :class:`~.IdCore`
identity attributes.
"""
import abc
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE

ViewName = typing.TypeVar(
    'ViewName', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewSummary = typing.TypeVar(
    'ViewSummary', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewTitle = typing.TypeVar(
    'ViewTitle', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)


class ControlIdCore(typing.Generic[
        ViewName, ViewSummary, ViewTitle], abc.ABC):
    """Mediates addition and removal of views of identity attributes."""

    def attach_name(self) -> ViewName:
        """Return view associated with model component name."""
        return self.idcore.name.attach_view()

    def attach_summary(self) -> ViewSummary:
        """Return view associated with model component summary."""
        return self.idcore.summary.attach_view()

    def attach_title(self) -> ViewTitle:
        """Return view associated with model component title."""
        return self.idcore.title.attach_view()

    def detach_name(self, p_view: ViewName) -> None:
        """Disassociate view from model component name.

        :param p_view: view to detach.
        """
        self.idcore.name.detach_view(p_view)

    def detach_summary(self, p_view: ViewSummary) -> None:
        """Disassociate view from model component summary.

        :param p_view: view to detach.
        """
        self.idcore.summary.detach_view(p_view)

    def detach_title(self, p_view: ViewTitle) -> None:
        """Disassociate view from model component summary.

        :param p_view: view to detach.
        """
        self.idcore.title.detach_view(p_view)

    @property
    @abc.abstractmethod
    def idcore(self) -> MIDCORE.IdCore:
        """Return component identity."""
        raise NotImplementedError
