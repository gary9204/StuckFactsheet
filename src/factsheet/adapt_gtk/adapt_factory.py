"""
Defines GTK-based classes that implement abstract factory classes.

See :mod:`.abc_factory`.
"""
from factsheet.abc_types import abc_factory as ABC_FACTORY
from factsheet.adapt_gtk import adapt_text as ATEXT
from factsheet.adapt_gtk import adapt_view as AVIEW


class FactoryInfoId(ABC_FACTORY.FactoryInfoId):
    """Implements GTK-based factory for abstract factory class
    :class:`.FactoryInfoId`."""

    def new_model_title(self, p_text: str = '') -> ATEXT.AdaptEntryBuffer:
        """Return new instance of Gtk-based :mod:`~factsheet.model` title."""
        return ATEXT.AdaptEntryBuffer(p_text=p_text)

    def new_view_title(self) -> AVIEW.AdaptEntry:
        """Return new instance of GTK-based :mod:`~factsheet.view` title.."""
        return AVIEW.AdaptEntry()
