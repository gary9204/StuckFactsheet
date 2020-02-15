"""
factsheet.types_abstract.abc_sheet - abstract data types for Factsheet
    classes.
"""


class ObserverSheet:
    """Observer pattern interface for a fact sheet model.

    .. note:: ObserverSheet is an abstract interface.  It is not
       possible to derive ObserverSheet from abc.ABC.  View classes that
       implement the interface derive from GTK base classes, which
       conflict with ABC.
    """

    def on_changed_name(self) -> None:
        """Respond to change in factsheet name.

        The default behavior is to do nothing.
        """
        pass

    def on_delete_sheet(self) -> None:
        """Respond to factsheet deletion.

        The default behavior is to do nothing.
        """
        pass
