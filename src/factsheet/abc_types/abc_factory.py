"""
Defines abstract factory classes.
"""


import abc

from factsheet.abc_types import abc_header as ABC_HEADER
from factsheet.abc_types import abc_view as ABC_VIEW


class FactoryHeader(abc.ABC):
    """Defines abstract factory to produce components for Header classes."""

    @abc.abstractmethod
    def new_title_model(
            self, p_text: str = '') -> ABC_HEADER.AbstractTextModel:
        """Return new instance of Model class Title."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_title_view(self) -> ABC_VIEW.AbstractTextView:
        """Return new instance of View class Title
        (:data:`.AbstractTextView`)."""
        raise NotImplementedError
