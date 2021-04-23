"""
Defines identity attributes common to Factsheet model components.
See :mod:`~factsheet.model`

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

ViewName = typing.TypeVar(
    'ViewName', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewSummary = typing.TypeVar(
    'ViewSummary', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)
ViewTitle = typing.TypeVar(
    'ViewTitle', BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)


class IdCore(ABC_STALE.InterfaceStaleFile,
             typing.Generic[ViewName, ViewSummary, ViewTitle], abc.ABC):
    """Defines identity attributes common to Factsheet model components.

    A descendant class must extend :meth:`~.__init__` to define stores
    for each identity attribute.

    .. admonition:: About Equality

        Two :class:`~.IdCore` instances are equivalent when their names,
        titles, and summaries are the equal. Transient aspects of the
        instances (like views) are not compared and may be different.
    """

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

    def __init__(self, *, p_name: str, p_summary: str, p_title: str,
                 **kwargs: typing.Any) -> None:
        """Initialize instance.

        :param p_name: short identifier for component (suitable, for
            example, as a label).
        :param p_summary: description of component, which adds detail to
            title.
        :param p_title: one-line description of component.
        """
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        self._name, self._summary, self._title = self._new_model()
        self._name.text = p_name
        self._summary.text = p_summary
        self._title.text = p_title
        self.set_fresh()

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

    @abc.abstractmethod
    def _new_model(self) -> typing.Tuple[
            BUI.BridgeText, BUI.BridgeText, BUI.BridgeText]:
        """Return (name, summary, title) store."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        """Return component name as text."""
        return self._name.text

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

    @property
    def summary(self) -> str:
        """Return component summary as text."""
        return self._summary.text

    @property
    def title(self) -> str:
        """Return component title as text."""
        return self._title.text
