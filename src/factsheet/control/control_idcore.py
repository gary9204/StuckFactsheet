"""
Defines generic control to add and remove views of :class:`~.IdCore`
identity attributes.

.. data:: ViewName

    Type hint for view of name.

.. data:: ViewSummary

    Type hint for view of summary.

.. data:: ViewTitle

    Type hint for view of title attribute.
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
    """Mediates addition of views of identity attributes."""

    def new_view_name(self) -> ViewName:
        """Return view associated with model component name."""
        return self.idcore.name.new_view()

    def new_view_summary(self) -> ViewSummary:
        """Return view associated with model component summary."""
        return self.idcore.summary.new_view()

    def new_view_title(self) -> ViewTitle:
        """Return view associated with model component title."""
        return self.idcore.title.new_view()

    @property
    @abc.abstractmethod
    def idcore(self) -> MIDCORE.IdCore:
        """Return identity model of component."""
        raise NotImplementedError
