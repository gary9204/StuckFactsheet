"""
Defines identity attributes common to Factsheet model components.
See :mod:`~factsheet.model`

.. data:: NameAdapt

    Type hint for text adpter for name attribute of model component.

.. data:: SummaryAdapt

    Type hint for text adpter for summary attribute of model component.

.. data:: TitleAdapt

    Type hint for text adpter for title attribute of model component.
"""
import abc
import typing

import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.adapt_gtk.adapt as ADAPT

NameAdapt = typing.TypeVar('NameAdapt', ADAPT.AdaptTextFormat,
                           ADAPT.AdaptTextMarkup, ADAPT.AdaptTextStatic)
SummaryAdapt = typing.TypeVar('SummaryAdapt', ADAPT.AdaptTextFormat,
                              ADAPT.AdaptTextMarkup, ADAPT.AdaptTextStatic)
TitleAdapt = typing.TypeVar('TitleAdapt', ADAPT.AdaptTextFormat,
                            ADAPT.AdaptTextMarkup, ADAPT.AdaptTextStatic)


class IdCore(typing.Generic[NameAdapt, SummaryAdapt, TitleAdapt],
             ABC_STALE.InterfaceStaleFile, abc.ABC):
    """Defines identity attributes common to Factsheet model components.

    .. admonition:: About Equality

        Two `IdCore` instances are equivalent when their names, titles,
        and summaries are the equal. Transient aspects of the instances
        (like views) are not compared and may be different.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has equal name, summary, and title.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, type(self)):
            return False

        if self.name != px_other.name:
            return False

        if self.summary != px_other.summary:
            return False

        if self.title != px_other.title:
            return False

        return True

    def __init__(self, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        self._stale = False

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to identity."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        identity.
        """
        if self._stale:
            return True

        if self.name.is_stale():
            self._stale = True
            return True

        if self.summary.is_stale():
            self._stale = True
            return True

        if self.title.is_stale():
            self._stale = True
            return True

        return False

    @property
    @abc.abstractmethod
    def name(self) -> NameAdapt:
        """Return component name adapter."""
        raise NotImplementedError

    def set_fresh(self):
        """Mark identity in memory consistent with file contents."""
        self._stale = False
        self.name.set_fresh()
        self.summary.set_fresh()
        self.title.set_fresh()

    def set_stale(self):
        """Mark identity in memory changed from file contents."""
        self._stale = True

    @property
    @abc.abstractmethod
    def summary(self) -> SummaryAdapt:
        """Return component summary adapter."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> TitleAdapt:
        """Return component title adapter."""
        raise NotImplementedError
