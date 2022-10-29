"""
Abstract component factory for a user interface toolkit feature.

.. data:: ControlOpaque

    Type variable for control of a toolkit feature.  The type variable
    serves as parameter for generic class.

.. data:: ControlTrackOpaque

    Type variable for control of a toolkit feature.  The control tracks
    changes in the corresponding model.  The type variable serves as
    parameter for generic class.

.. data:: ModelOpaque

    Type variable for model facade of a toolkit feature.  The type
    variable serves as parameter for generic class.
"""
import abc
import typing

ControlOpaque = typing.TypeVar('ControlOpaque')
ControlTrackOpaque = typing.TypeVar('ControlTrackOpaque')
ModelOpaque = typing.TypeVar('ModelOpaque')


class NewComponentAbc(abc.ABC, typing.Generic[
        ControlOpaque, ControlTrackOpaque, ModelOpaque]):
    """Abstract component factory for a user interface toolkit feature."""

    @abc.abstractmethod
    def new_control(self, p_model: ModelOpaque = None
                    ) -> ControlOpaque:
        """Return component factory for feature control."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_control_track(self, p_model: ModelOpaque = None
                          ) -> ControlTrackOpaque:
        """Return component factory for feature control with track changes."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_model(self) -> ModelOpaque:
        """Return component factory for feature model facade."""
        raise NotImplementedError
