"""
Defines abstract data types classes for sheets.
"""


ALLOWED = True
CONTINUE_GTK = False


class ObserverSheet:
    """Defines interface for class observing sheet model.

    .. note:: ObserverSheet is an abstract interface for an Observer
       pattern.  View classes that implement the interface may derive
       from GTK base classes, which conflict with ABC.  Hence, it is not
       possible to derive ObserverSheet from abc.ABC.
    """

    def update_name(self) -> None:
        """Respond to notice of sheet name change.

        The default behavior is to do nothing.
        """
        pass

    def detach(self) -> None:
        """Respond to notice to detach observer from model.

        The default behavior is to do nothing.
        """
        pass
