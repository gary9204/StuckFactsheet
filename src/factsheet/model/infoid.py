"""
Defines identification information for Factsheet :mod:`~factsheet.model`
components.
"""

import typing

from factsheet.abc_types import abc_stalefile as ABC_STALE
from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.model import types_model as MTYPES
# from factsheet.view import ui as UI


class InfoId(ABC_STALE.InterfaceStaleFile):
    """Defines identification information common to Factsheet components.

    The Factsheet model includes components for factsheets, topics, and
    facts.  These components have identification information in common.
    The information represented by ``InfoId`` is as follows.

     * *ID:* identifier that is unique for lifetime of the component.
     * *Name:* short, editable identifier (suitable, for example, as
       label).
     * *Summary:* editable description of component, which adds detail
       to title.
     * *Title:* one-line, editable description of component contents.

    .. admonition:: About Equality

        Two `InfoId` instances are equivalent when their names, titles,
        and summaries are the equal. Transient aspects of the instances
        (like views) are not compared and may be different.
    """

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '') -> None:
        self._id_model = id(self)
        self._stale = False
        self._name = MTYPES.ModelName(p_name)
        self._summary = MTYPES.ModelSummary(p_summary)
        self._title = MTYPES.ModelTitle(p_title)

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same name, summary, and title.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, InfoId):
            return False

        if str(self._name) != str(px_other._name):
            return False

        if str(self._summary) != str(px_other._summary):
            return False

        if str(self._title) != str(px_other._title):
            return False

        return True

    def attach_view(self, pm_view: ABC_INFOID.InterfaceViewInfoId) -> None:
        """Add view to update display when identification information
        changes.

        :param pm_view: view to add
        """
        self._name.attach_view(pm_view.get_view_name())
        self._summary.attach_view(pm_view.get_view_summary())
        self._title.attach_view(pm_view.get_view_title())

    def detach_view(self, pm_view: ABC_INFOID.InterfaceViewInfoId) -> None:
        """Remove view of identification information.

        :param pm_view: view to remove
        """
        self._name.detach_view(pm_view.get_view_name())
        self._summary.detach_view(pm_view.get_view_summary())
        self._title.detach_view(pm_view.get_view_title())

    @property
    def id_model(self) -> int:
        """Return component identifier."""
        return self._id_model

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to
        identification information.
        """
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        identification information.
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
    def name(self) -> str:
        """Return text of component name."""
        return str(self._name)

    def set_fresh(self):
        """Mark identification information in memory consistent with
        file contents.
        """
        self._stale = False
        self._name.set_fresh()
        self._summary.set_fresh()
        self._title.set_fresh()

    def set_stale(self):
        """Mark identification information in memory changed from file
        contents.
        """
        self._stale = True

    @property
    def summary(self) -> str:
        """Return text of component summary."""
        return str(self._summary)

    @property
    def title(self) -> str:
        """Return text of component title."""
        return str(self._title)
