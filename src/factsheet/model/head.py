"""
Defines identification information class for Factsheet components.
"""

import typing

from factsheet.abc_types import abc_head as ABC_HEAD
from factsheet.view import page_head as VPHEAD

from factsheet.view import ui as VUI


class Head(ABC_HEAD.InterfaceStaleFile):
    """Defines identification information common to Factsheet components.

    The Factsheet model includes components for factsheets, topics, and
    facts.  These components have identification information in common.
    The information represented by `Head` is as follows.

     * ID: component identifier that is unique for lifetime of component.
     * Aspect: identifies contribution of component (for example, set).
     * Name: short identifier (suitable, for example, as label).
     * Title: one-line description of model contents.
     * Summary: description of model, which adds detail to title.

    .. tip:: Two `Head` instances are equivalent when their aspects,
       names, titles, and summaries are the same.
    """

    def __init__(self, *, p_aspect: str, p_title: str = '', **_kwargs):
        self._aspect = p_aspect
        self._id = id(self)
        self._stale = False
        self._title = VUI.FACTORY_HEAD.new_title_model(p_title)

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same aspect name, summary, and
        title.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, Head):
            return False

        if not self._aspect == px_other._aspect:
            return False

        if str(self._title) != str(px_other._title):
            return False

        return True

    def attach_page(self, pm_page: VPHEAD.PageHead, **_kwargs):
        """Add view to update display when header attributes change."""
        self._title.attach_view(pm_page.get_title())

    def detach_page(self, pm_page: VPHEAD.PageHead, **_kwargs):
        """Remove view of changes to header attributes."""
        self._title.detach_view(pm_page.get_title())

    def get_id(self) -> int:
        """Return component identifier."""
        return self._id

    def get_aspect(self) -> str:
        """Return component contribution to model."""
        return self._aspect

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
