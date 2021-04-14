"""
Defines identity attributes common to Factsheet model components.
See :mod:`~factsheet.model`

.. data:: BridgeName

    Type hint for text bridge for name attribute of model.

.. data:: BridgeSummary

    Type hint for text bridge for summary attribute of model.

.. data:: BridgeTitle

    Type hint for text bridge for title attribute of model.

.. data:: ViewName

    Type hint for view of name attribute of model.

.. data:: ViewSummary

    Type hint for view of summary attribute of model.

.. data:: ViewTitle

    Type hint for view of title attribute of model.
"""
import abc
import typing

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.bridge_ui as BUI

BridgeName = typing.TypeVar('BridgeName', BUI.BridgeTextFormat,
                            BUI.BridgeTextMarkup, BUI.BridgeTextStatic)
BridgeSummary = typing.TypeVar('BridgeSummary', BUI.BridgeTextFormat,
                               BUI.BridgeTextMarkup, BUI.BridgeTextStatic)
BridgeTitle = typing.TypeVar('BridgeTitle', BUI.BridgeTextFormat,
                             BUI.BridgeTextMarkup, BUI.BridgeTextStatic)
ViewName = typing.TypeVar(
    'ViewName', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewSummary = typing.TypeVar(
    'ViewSummary', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewTitle = typing.TypeVar(
    'ViewTitle', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)


class IdCore(ABC_STALE.InterfaceStaleFile,
             typing.Generic[BridgeName, BridgeSummary, BridgeTitle],
             abc.ABC):
    """Defines identity attributes common to Factsheet model components.

    A descendant class must extend :meth:`~.__init__` to define stores
    for each identity attribute.

    .. admonition:: About Equality

        Two :class:`~.IdCore` instances are equivalent when their names,
        titles, and summaries are the equal. Transient aspects of the
        instances (like views) are not compared and may be different.

    :param kwargs: placeholder for keyword arguments in descendants.
        Should be empty.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has equal name, summary, and title.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, type(self)):
            return False

        if self._name != px_other._name:
            return False

        if self._summary != px_other._summary:
            return False

        if self._title != px_other._title:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return identity in form pickle can persist.

        Persistent form of identity excludes run-time information.
        """
        state = self.__dict__.copy()
        del state['_stale']
        return state

    @abc.abstractmethod
    def __init__(self, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        self._stale = False
        self._name: BridgeName
        self._summary: BridgeSummary
        self._title: BridgeTitle

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct identity from state pickle loads.

        Reconstructed identity is marked fresh.

        :param px_state: unpickled state of stored identity.
        """
        self.__dict__.update(px_state)
        self._stale = False

    def is_fresh(self) -> bool:
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

    def new_view_name(self) -> ViewName:
        """Return view to display name."""
        return self._name.new_view()

    def new_view_summary(self) -> ViewSummary:
        """Return view to display summary."""
        return self._summary.new_view()

    def new_view_title(self) -> ViewTitle:
        """Return view to display title."""
        return self._title.new_view()

    def set_fresh(self):
        """Mark identity in memory consistent with file contents."""
        self._stale = False
        self._name.set_fresh()
        self._summary.set_fresh()
        self._title.set_fresh()

    def set_stale(self):
        """Mark identity in memory changed from file contents."""
        self._stale = True
