"""
Defines GTK-based classes that implement abstract factory classes.

See :mod:`.abc_factory`.
"""


from factsheet.abc_types import abc_factory as ABC_FACTORY
from factsheet.adapt_gtk import adapt_text as ATEXT
from factsheet.adapt_gtk import adapt_view as AVIEW


class FactoryHeaderGtk(ABC_FACTORY.FactoryHeader):
    """Implements GTK-based factory for abstract factory class
    :class:`.FactoryHeader`."""

    def new_title_model(self, p_text: str = '') -> ATEXT.AdaptEntryBuffer:
        """Return new instance of Gtk-based Title model."""
        return ATEXT.AdaptEntryBuffer(p_text=p_text)

    def new_title_view(self) -> AVIEW.AdaptEntry:
        """Return new instance of GTK-based Title view
        (:data:`.AdaptEntry`)."""
        return AVIEW.AdaptEntry()
