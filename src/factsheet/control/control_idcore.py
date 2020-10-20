"""
Defines generic control to add and remove views of :class:`~.IdCore`
identity attributes.
"""
import typing   # noqa

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.model.idcore as MIDCORE

ViewNameAdapt = typing.TypeVar('ViewNameAdapt', ADAPT.ViewTextFormat,
                               ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)
ViewSummaryAdapt = typing.TypeVar('ViewSummaryAdapt', ADAPT.ViewTextFormat,
                                  ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)
ViewTitleAdapt = typing.TypeVar('ViewTitleAdapt', ADAPT.ViewTextFormat,
                                ADAPT.ViewTextMarkup, ADAPT.ViewTextStatic)


class ControlIdCore(
        typing.Generic[ViewNameAdapt, ViewSummaryAdapt, ViewTitleAdapt]):
    """Provides addition and removal of views of identity attributes.

    :param p_model: add and remove views of this model component.
    """

    def __init__(self, p_model: MIDCORE.IdCore, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        self._model = p_model

    def attach_name(self, p_view: ViewNameAdapt) -> None:
        """Add view to model component name.

        :param p_view: to add.
        """
        self._model.name.attach_view(p_view)

    def detach_name(self, p_view: ViewNameAdapt) -> None:
        """Remove view from model component name.

        :param p_view: view to remove.
        """
        self._model.name.detach_view(p_view)

    def attach_summary(self, p_view: ViewSummaryAdapt) -> None:
        """Add view to model component summary.

        :param p_view: to add.
        """
        self._model.summary.attach_view(p_view)

    def detach_summary(self, p_view: ViewSummaryAdapt) -> None:
        """Remove view from model component summary.

        :param p_view: view to remove.
        """
        self._model.summary.detach_view(p_view)

    def attach_title(self, p_view: ViewTitleAdapt) -> None:
        """Add view to model component title.

        :param p_view: to add.
        """
        self._model.title.attach_view(p_view)

    def detach_title(self, p_view: ViewTitleAdapt) -> None:
        """Remove view from model component title.

        :param p_view: view to remove.
        """
        self._model.title.detach_view(p_view)
