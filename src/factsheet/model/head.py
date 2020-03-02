"""
Defines common base class for Factsheet model components.
"""

from factsheet.abc_types import abc_head as ABC_HEAD
from factsheet.view import page_head as VPHEAD

from factsheet.adapt_gtk import adapt_factory as AFACTORY

FACTORY_HEADER = AFACTORY.FactoryHead()


class Head(ABC_HEAD.InterfaceStaleFile):
    """Represents content and methods common to Factsheet model
    components.

    The Factsheet model includes components for factsheets, topics, and
    facts.  These components have identification, description, and
    management functions in common.  Model class Head represents these
    comment elements, which consist of the following.

     * ID: component identifier that is unique for lifetime of header.
     * Aspect: identifies contribution of component (for example, set).
     * Name: short identifier (suitable, for example, as label).
     * Title: one-line description of model contents.
     * Summary: description of model, which adds detail to title.
    """

    def __init__(self):
        pass

    def attach_view(self, pm_view: VPHEAD.PageHead):
        """Add view to update display when header attributes change."""
        raise NotImplementedError

    def detach_view(self, pm_view: VPHEAD.PageHead):
        """Remove view of changes to header attributes."""
        raise NotImplementedError

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to header."""
        raise NotImplementedError

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to header."""
        raise NotImplementedError

    def set_fresh(self):
        """Mark header in memory consistent with file contents."""
        raise NotImplementedError

    def set_stale(self):
        """Mark header in memory changed from file contents."""
        raise NotImplementedError
