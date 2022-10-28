"""
Abstract component factory for user interface toolkit features.
See :mod:`~.factsheet.ui_bricks.ui_abc`.
"""
import abc

import factsheet.ui_bricks.ui_abc.new_markup_abc as NEWMARKUPABC


class NewBrickAbc(abc.ABC):
    """Abstract component factory for user interface toolkit features.

    The factory is an aggregation of component factories for each
    toolkit feature. Each feature factory defines methods as needed to
    constuct model facades for the feature along with corresponding
    control objects and view facades.
    """

    @property
    @abc.abstractmethod
    def markup(self) -> NEWMARKUPABC.NewMarkupAbc:
        """Return component factory for text with manually entered markup."""
        raise NotImplementedError
