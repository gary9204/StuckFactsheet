"""
Defines identity attributes common to Factsheet model components.
See :mod:`~factsheet.model`

.. data:: ModelName

    Type hint for model for component name.

.. data:: ModelSummary

    Type hint for model for component summary.

.. data:: ModelTitle

    Type hint for model for component title.
"""
# import abc
import typing

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.bridge_ui as BUI

ModelName = typing.TypeVar(
    'ModelName', BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)
ModelSummary = typing.TypeVar(
    'ModelSummary', BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)
ModelTitle = typing.TypeVar(
    'ModelTitle', BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)


class IdCore(ABC_STALE.InterfaceStaleFile,
             typing.Generic[ModelName, ModelSummary, ModelTitle]):
    """Defines identity attributes common to Factsheet model components.

    Common identity atttributes are name, summary, and title.

        *Name:* short identifier for component (suitable, for
        example, as a label).

        *Summary:* description of component, which adds detail to
        title.

        *Title:* one-line description of component.
    """

    _name: ModelName
    _summary: ModelSummary
    _title: ModelTitle

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has equal name, summary, and title.

        :param p_other: object to compare with self.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self._name != p_other._name:
            return False

        if self._summary != p_other._summary:
            return False

        if self._title != p_other._title:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return identity in form pickle can persist.

        Persistent form of identity excludes run-time information.
        """
        state = self.__dict__.copy()
        del state['_stale']
        return state

    def __init__(self, **kwargs: typing.Any) -> None:
        """Initialize instance.

        Subclasses must define attributes for name, summary, and title
        before calling :meth:`.IdCore.__init__`.

        :param kwargs: superclass keyword parameters.
        """
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        type_hints = typing.get_type_hints(self.__class__)
        for name, hint in type_hints.items():
            if not hasattr(self, name):
                raise AttributeError(
                    '{}: IdCore subclasses must define {} attribute '
                    'with type {} and then call super().__init__()'
                    ''.format(self.__class__.__name__, name, hint))
        self._stale: bool
        self.set_fresh()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct identity from state pickle loads.

        Reconstructed identity is marked fresh.

        :param px_state: unpickled state of stored identity.
        """
        self.__dict__.update(px_state)
        self.set_fresh()

    def has_not_changed(self) -> bool:
        """Return True when there are no unsaved changes to identity."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        identity.
        """
        if self._stale:
            return True

        if self._name.is_stale():
            self._stale = True
            return True

        if self._summary.is_stale():
            self._stale = True
            return True

        if self._title.is_stale():
            self._stale = True
            return True

        return False

    @property
    def name(self) -> ModelName:
        """Return name model."""
        return self._name

    def set_fresh(self) -> None:
        """Mark identity in memory consistent with file contents."""
        self._stale = False
        self._name.set_fresh()
        self._summary.set_fresh()
        self._title.set_fresh()

    def set_stale(self):
        """Mark identity in memory changed from file contents."""
        self._stale = True

    @property
    def summary(self) -> ModelSummary:
        """Return summary model."""
        return self._summary

    @property
    def title(self) -> ModelTitle:
        """Return title model."""
        return self._title
