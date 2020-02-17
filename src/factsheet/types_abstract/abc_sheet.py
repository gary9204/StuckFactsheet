"""
factsheet.types_abstract.abc_sheet - defines abstract data types classes
    for sheets.
"""


class ObserverSheet:
    """Defines interface for class observing sheet model.

    .. note:: ObserverSheet is an abstract interface for an Observer
       pattern.  View classes that implement the interface may derive
       from GTK base classes, which conflict with ABC.  Hence, it is not
       possible to derive ObserverSheet from abc.ABC.
    """

    def on_changed_name_sheet(self) -> None:
        """Respond to change in sheet name.

        The default behavior is to do nothing.
        """
        pass

    def on_delete_model_sheet(self) -> None:
        """Respond to deletion of model for sheet.

        The default behavior is to do nothing.
        """
        pass
