"""
Abstract component factory for a user interface toolkit feature."""
import abc
import typing

ControlGeneric = typing.TypeVar('ControlGeneric')
ControlTrackGeneric = typing.TypeVar('ControlTrackGeneric')
ModelGeneric = typing.TypeVar('ModelGeneric')


class NewComponentAbc(abc.ABC, typing.Generic[
        ControlGeneric, ControlTrackGeneric, ModelGeneric]):
    """Abstract component factory for a user interface toolkit feature.

    .. data:: ControlGeneric

        Type variable for control of a toolkit feature.

    .. data:: ControlTrackGeneric

        Type variable for control of a toolkit feature.  The control
        tracks changes in the corresponding model.

    .. data:: ModelGeneric

        Type variable for model facade of a toolkit feature.
    """

    @abc.abstractmethod
    def new_control(self, p_model: ModelGeneric = None
                    ) -> ControlGeneric:
        """Return component factory for feature control."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_control_track(self, p_model: ModelGeneric = None
                          ) -> ControlTrackGeneric:
        """Return component factory for feature control with track changes."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_model(self) -> ModelGeneric:
        """Return component factory for feature model facade."""
        raise NotImplementedError
