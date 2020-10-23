"""
Defines generic control to add and remove views of :class:`~.IdCore`
identity attributes.
"""
import abc
import typing   # noqa

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.model.idcore as MIDCORE

ViewNameAdapt = typing.TypeVar('ViewNameAdapt', ADAPT.ViewTextFormat,
                               ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)
ViewSummaryAdapt = typing.TypeVar('ViewSummaryAdapt', ADAPT.ViewTextFormat,
                                  ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)
ViewTitleAdapt = typing.TypeVar('ViewTitleAdapt', ADAPT.ViewTextFormat,
                                ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)


class ControlIdCore(typing.Generic[
        ViewNameAdapt, ViewSummaryAdapt, ViewTitleAdapt], abc.ABC):
    """Mediates addition and removal of views of identity attributes."""

    def attach_name(self, p_view: ViewNameAdapt) -> None:
        """Ask model component name to add view.

        :param p_view: view to add.
        """
        self.idcore.name.attach_view(p_view)

    def attach_summary(self, p_view: ViewSummaryAdapt) -> None:
        """Ask model component summary to add view.

        :param p_view: view to add.
        """
        self.idcore.summary.attach_view(p_view)

    def attach_title(self, p_view: ViewTitleAdapt) -> None:
        """Ask model component title to add view.

        :param p_view: view to add.
        """
        self.idcore.title.attach_view(p_view)

    def detach_name(self, p_view: ViewNameAdapt) -> None:
        """Ask model component name to remove view.

        :param p_view: view to remove.
        """
        self.idcore.name.detach_view(p_view)

    def detach_summary(self, p_view: ViewSummaryAdapt) -> None:
        """Ask model component summary to remove view.

        :param p_view: view to remove.
        """
        self.idcore.summary.detach_view(p_view)

    def detach_title(self, p_view: ViewTitleAdapt) -> None:
        """Ask model component summary to remove view.

        :param p_view: view to remove.
        """
        self.idcore.title.detach_view(p_view)

    @property
    @abc.abstractmethod
    def idcore(self) -> MIDCORE.IdCore:
        """Return component identity."""
        raise NotImplementedError
