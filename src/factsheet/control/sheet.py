"""
factsheet.control.control - mediates from view to model of s factsheet.
"""

from factsheet.types_abstract import abc_sheet as ASHEET
from factsheet.model import sheet as MSHEET


class Sheet(object):
    """Mediates user actions at view to model updates for a factsheet.

    Control class Sheet translates user requests in a factsheet view
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).
    """

    def __init__(self):
        self._model = None

    def attach_view(self, px_view):
        """Add model observer."""
        pass

    def delete(self):
        """Delete factsheet unconditionally."""
        pass

    def delete_safe(self):
        """Delete factsheet provided no changes will be lost."""
        return ASHEET.ALLOWED

    def detach_view(self, px_view):
        """Remove model observer unconditionally."""
        pass

    def detach_view_safe(self, px_view):
        """Remove model observer provided no changes will be lost."""
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
