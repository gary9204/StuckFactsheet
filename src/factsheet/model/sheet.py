"""
Defines data representation of a factsheet.
"""


from factsheet.abc_types import abc_sheet as ASHEET


class Sheet:
    """Data representation of a factsheet.

    Model class Sheet represents an entire factsheet document.  A model
    sheet consists of a hierarchy of topics along with descriptive
    information (see model class Header.)  Each topic represents a
    collection of facts about a specific subject.
    """

    def __init__(self):
        self._observers = dict()
        self._unsaved_changes = False

    def add_observer(self, px_observer: ASHEET.ObserverSheet):
        """Add observer to notification list.

        $param px_observer$ observer to notify"""
        self._observers[id(px_observer)] = px_observer

    def delete(self):
        """Send delete notice to all observers and remove all observers."""
        while self._observers:
            _id_obs, obs = self._observers.popitem()
            obs.detach()

    def remove_observer(self, px_observer: ASHEET.ObserverSheet):
        """Remove observer from notification list.

        $param px_observer$ stop notifying this observer"""
        _ = self._observers.pop(id(px_observer))

    def unsaved_changes(self):
        """Return True when factsheet contains unsaved changes."""
        return self._unsaved_changes
