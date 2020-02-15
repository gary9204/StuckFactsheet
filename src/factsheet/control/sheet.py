"""
factsheet.control.control - mediates from view to model of s factsheet.
"""


class Sheet(object):
    """Mediates user actions at view to model updates for a factsheet.

    Control class Sheet translates user requests in a factsheet view
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).
    """

    def __init__(self, params):
        pass

    def add_view(self, px_view):
        """Binds view to model and adds it to the collection of views."""
        pass

    def delete_sheet(self):
        """Remove all sheet views and release sheet model and control."""
        pass

    def remove_view(self, px_view):
        """Unbinds view from model and removes it from collection of views."""
        pass

    def unsaved_changes(self):
        """Return True when factsheet contains unsaved changes."""
        pass
