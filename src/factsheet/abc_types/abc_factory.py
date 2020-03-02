"""
Defines abstract factory classes.
"""


import abc

from factsheet.abc_types import abc_head as ABC_HEAD
from factsheet.abc_types import abc_view as ABC_VIEW


class FactoryHead(abc.ABC):
    """Defines abstract factory to produce components for `Head`
    classes.
    """

    @abc.abstractmethod
    def new_title_model(
            self, p_text: str = '') -> ABC_HEAD.AbstractTextModel:
        """Return new instance of :mod:`~.factsheet.model` title for
        :class:`.Head`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_title_view(self) -> ABC_VIEW.AbstractTextView:
        """Return new instance of :mod:`~.factsheet.view` title for
        :class:`.PageHead`.
        """
        raise NotImplementedError
