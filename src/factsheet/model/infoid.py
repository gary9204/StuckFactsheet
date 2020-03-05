"""
Defines identification information for Factsheet :mod:`~factsheet.model`
components.
"""

import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.view import view_infoid as VINFOID

from factsheet.view import ui as UI


class InfoId(ABC_INFOID.InterfaceStaleFile):
    """Defines identification information common to Factsheetcomponents.

    The Factsheet model includes components for factsheets, topics, and
    facts.  These components have identification information in common.
    The information represented by `InfoId` is as follows.

     * ID: identifier that is unique for lifetime of the component.
     * Aspect: identifies contribution of component (for example, set).
     * Name: short, editable identifier (suitable, for example, as
       label).
     * Title: one-line, editable description of component contents.
     * Summary: editable description of component, which adds detail to
       title.

    .. tip:: Two `InfoId` instances are equivalent when their aspects,
       names, titles, and summaries are the same.
    """

    def __init__(self, *, p_aspect: str, p_title: str = '') -> None:
        self._aspect = p_aspect
        self._id_model = id(self)
        self._stale = False
        self._title = UI.FACTORY_INFOID.new_model_title(p_title)

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same aspect name, summary, and
        title.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, InfoId):
            return False

        if not self._aspect == px_other._aspect:
            return False

        if str(self._title) != str(px_other._title):
            return False

        return True

    @property
    def aspect(self) -> str:
        """Return component contribution to :mod:`~factsheet.model`."""
        return self._aspect

    def attach_view(self, pm_view: VINFOID.ViewInfoId) -> None:
        """Add view to update display when identification information
        changes.
        """
        self._title.attach_view(pm_view.get_view_title())

    def detach_view(self, pm_view: VINFOID.ViewInfoId) -> None:
        """Remove view of changes to identification information."""
        self._title.detach_view(pm_view.get_view_title())

    @property
    def id_model(self) -> int:
        """Return component identifier."""
        return self._id_model

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to
        identification information.
        """
        if self._stale:
            return False

        if self._title.is_stale():
            self._stale = True
            return False

        return True

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        identification information.
        """
        if self._stale:
            return True

        if self._title.is_stale():
            self._stale = True
            return True

        return False

    def set_fresh(self):
        """Mark header in memory consistent with file contents."""
        self._stale = False
        self._title.set_fresh()

    def set_stale(self):
        """Mark header in memory changed from file contents."""
        self._stale = True

    @property
    def title(self) -> str:
        """Return text of component title."""
        return str(self._title)