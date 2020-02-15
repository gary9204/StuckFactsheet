"""
factsheet.model.sheet - defines data representation of a factsheet.
"""


class Sheet:
    """Data representation of a factsheet.

    Model class Sheet represents an entire factsheet document.  A model
    sheet consists of a hierarchy of topics along with descriptive
    information (see model class Header.)  Each topic represents a
    collection of facts about a specific subject.
    """

    def __init__(self):
        pass

    def add_observer(self, px_observer):
        """Add observer to notification list."""
        pass

    def delete_sheet(self):
        """Send delete notice to all observers the remove all observers."""
        pass

    def remove_observer(self, px_observer):
        """Remove observer from notification list."""
        pass

    def unsaved_changes(self):
        """Return True when factsheet contains unsaved changes."""
        pass
