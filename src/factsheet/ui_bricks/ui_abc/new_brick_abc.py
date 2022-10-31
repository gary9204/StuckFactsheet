"""
Abstract component factory for user interface toolkit features.
See :mod:`~.factsheet.ui_bricks.ui_abc`.
"""
import abc
import typing

import factsheet.ui_bricks.ui_abc.new_component_abc as NCOMPABC

ControlMarkupGeneric = typing.TypeVar('ControlMarkupGeneric')
ControlMarkupTrackGeneric = typing.TypeVar('ControlMarkupTrackGeneric')
ModelMarkupGeneric = typing.TypeVar('ModelMarkupGeneric')


class NewBrickAbc(abc.ABC, typing.Generic[
        ControlMarkupGeneric, ControlMarkupTrackGeneric, ModelMarkupGeneric,
        ]):
    """Abstract factory for user interface toolkit features.

    The factory is an aggregation of component factories for each
    toolkit feature. Each feature factory defines methods as needed to
    constuct model facades for the feature along with corresponding
    control objects and view facades.
    """

    @property
    @abc.abstractmethod
    def markup(self) -> NCOMPABC.NewComponentAbc[
            ControlMarkupGeneric, ControlMarkupTrackGeneric, ModelMarkupGeneric
            ]:
        """Return component factory for text with manually entered markup.

    .. data:: ControlMarkupGeneric

        Type variable for control of markup text.

    .. data:: ControlMarkupTrackGeneric

        Type variable for control of markup text.  The control
        tracks changes in the corresponding model.

    .. data:: ModelMarkupGeneric

        Type variable for model facade of markup text.
        """
        raise NotImplementedError
