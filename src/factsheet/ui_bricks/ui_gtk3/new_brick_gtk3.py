"""
Factory for GTK 3 features.
"""
import factsheet.ui_bricks.ui_abc.new_brick_abc as NEWBRICKABC
import factsheet.ui_bricks.ui_gtk3.markup_gtk3 as BMARKUPGTK3


class NewBrickGtk3(NEWBRICKABC.NewBrickAbc[
        BMARKUPGTK3.ControlMarkupGtk3,
        BMARKUPGTK3.ControlMarkupTrackGtk3, BMARKUPGTK3.ModelMarkupGtk3,
        ]):
    """Factory for GTK 3 features.

    The factory is an aggregation of component factories for each
    GTK 3 feature.
    """

    def __init__(self) -> None:
        """Initialize component factories."""
        self._markup = BMARKUPGTK3.NewMarkupGtk3()

    @property
    def markup(self) -> BMARKUPGTK3.NewMarkupGtk3:
        """Return component factory for text with manually entered markup."""
        return self._markup
