"""
Defines class to display identification information for Factsheet pages.
"""
import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.adapt_gtk import adapt_infoid as AINFOID


class ViewInfoId(ABC_INFOID.InterfaceViewInfoId):
    """Provides display elements for page identification information.

    The identification information is common to `factesheet`, `topic`,
    and `fact` pages.  The class provides display element for a page's
    name, title, and summary.

    :param px_get_object: returns named object from user interface
        object definition.

    .. data:: UI_ID_TITLE

        ID in user interface file for element to display page title.
    """

    UI_ID_TITLE: typing.ClassVar[str] = 'ui_title_infoid'

    def __init__(self, px_get_object: typing.Callable, **_kwargs) -> None:
        self._view_title = px_get_object(self.UI_ID_TITLE)

    def get_view_title(self) -> AINFOID.AdaptEntry:
        """Return view's title display element."""
        return self._view_title

    @property
    def title(self) -> str:
        """Return text of title."""
        return self._view_title.get_text()
