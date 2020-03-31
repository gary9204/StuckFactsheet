"""
Defines abstract factory classes.
"""


import abc

from factsheet.abc_types import abc_infoid as ABC_INFOID


class FactoryInfoId(abc.ABC):
    """Defines abstract factory to produce identification information
    components for :class:`~.InfoId`. and :class:`~.ViewInfoId`.
    """

    @abc.abstractmethod
    def new_model_name(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of name for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_model_summary(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of summary for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_model_title(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of title for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_name(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of name for :class:`.ViewInfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_summary(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of summary for :class:`.ViewInfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_title(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of title for :class:`.ViewInfoId`.
        """
        raise NotImplementedError
