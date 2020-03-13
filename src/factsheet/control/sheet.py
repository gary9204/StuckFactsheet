"""
Defines class to mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet.
"""
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.model import sheet as MSHEET


class Sheet(object):
    """Mediates user actions at view to model updates for a factsheet.

    Class 'Sheet` translates user requests in a factsheet page
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).
    """

    def __init__(self) -> None:
        self._model: typing.Optional[MSHEET.Sheet] = None

    def attach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Add page to model."""
        assert self._model is not None
        self._model.attach_page(pm_page)

    def delete_force(self) -> None:
        """Delete factsheet unconditionally."""
        assert self._model is not None
        self._model.detach_all()

    def delete_safe(self) -> ABC_SHEET.EffectSafe:
        """Delete factsheet provided no changes will be lost."""
        assert self._model is not None
        if self._model.is_stale():
            return ABC_SHEET.EffectSafe.NO_EFFECT

        self._model.detach_all()
        return ABC_SHEET.EffectSafe.COMPLETED

    def detach_page_force(self, pm_page) -> None:
        """Remove page unconditionally."""
        assert self._model is not None
        self._model.detach_page(pm_page)

    def detach_page_safe(self, pm_page) -> ABC_SHEET.EffectSafe:
        """Remove page provided no changes will be lost."""
        assert self._model is not None
        if self._model.is_fresh():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        if 1 < self._model.n_pages():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        return ABC_SHEET.EffectSafe.NO_EFFECT

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
