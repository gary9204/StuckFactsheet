"""
Defines class to mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet.
"""
import typing   # noqa

from factsheet.abc_types import abc_sheet as ASHEET
from factsheet.model import sheet as MSHEET


class Sheet(object):
    """Mediates user actions at view to model updates for a factsheet.

    Class 'Sheet` translates user requests in a factsheet page
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).
    """

    def __init__(self) -> None:
        self._model: typing.Optional[MSHEET.Sheet] = None

    def attach_page(self, pm_page: ASHEET.InterfacePageSheet) -> None:
        """Add page to model."""
        assert self._model is not None
        self._model.attach_page(pm_page)

    def delete_force(self):
        """Delete factsheet unconditionally."""
        assert self._model is not None
        self._model.delete()

    def delete_safe(self):
        """Delete factsheet provided no changes will be lost."""
        return ASHEET.ALLOWED

    def detach_page_force(self, pm_page):
        """Remove page unconditionally."""
        pass

    def detach_page_safe(self, pm_page):
        """Remove page provided no changes will be lost."""
        return ASHEET.ALLOWED

    @classmethod
    def load(cls, p_path):
        """Create control with model from file."""
        pass

    @classmethod
    def new(cls):
        """Create control with default model."""
        control = Sheet()
        control._model = MSHEET.Sheet()
        return control
