"""
Defines class to create a heading in Factsheet template outline.
"""
from factsheet.abc_types import abc_sheet as ABC_SHEET


class Heading(ABC_SHEET.AbstractTemplate):
    """Heading in Factsheet Template outline.

    The class call interface always returns None, since a heading does
    not define a topic.
    """

    def __init__(
            self, *, p_name: str, p_summary: str, p_title: str) -> None:
        self._name = p_name
        self._summary = p_summary
        self._title = p_title
        return

    def __call__(self) -> None:
        """Returns None, since heading does not define a topic."""
        pass

    @property
    def name(self) -> str:
        """Return heading name. """
        return self._name

    @property
    def summary(self) -> str:
        """Return heading summary. """
        return self._summary

    @property
    def title(self) -> str:
        """Return heading title. """
        return self._title
