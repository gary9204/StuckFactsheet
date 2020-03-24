"""
Defines abstract factory classes.
"""


import abc

from factsheet.abc_types import abc_infoid as ABC_INFOID


class FactoryInfoId(abc.ABC):
    """Defines abstract factory to produce identification information
    components for :class:`.model.InfoId`.
    """

    @abc.abstractmethod
    def new_model_title(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of title for :class:`.model.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_title(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of title for :class:`.view.ViewInfoId`.
        """
        raise NotImplementedError
