"""
Defines generic control to produce views of :class:`~.IdCore`
identity attributes.
"""
import abc
import typing   # noqa

import factsheet.model.idcore as MIDCORE


class ControlIdCore(typing.Generic[
        MIDCORE.ViewNameActive, MIDCORE.ViewSummaryActive, MIDCORE.ViewTitleActive],
        abc.ABC):
    """Mediates addition of views of identity attributes.

    :param p_id_core: identity model.
    """

    # def __init__(self, p_idcore: MIDCORE.IdCore) -> None:
    #     self._idcore = p_idcore

    @abc.abstractmethod
    def new_view_name_active(self) -> MIDCORE.ViewNameActive:
        """Return view to display name."""
        raise NotImplementedError
        # return self._idcore.new_view_name_active()

    @abc.abstractmethod
    def new_view_summary_active(self) -> MIDCORE.ViewSummaryActive:
        """Return view to display summary."""
        raise NotImplementedError
        # return self._idcore.new_view_summary_active()

    @abc.abstractmethod
    def new_view_title_active(self) -> MIDCORE.ViewTitleActive:
        """Return view to display title."""
        raise NotImplementedError
        # return self._idcore.new_view_title_active()
