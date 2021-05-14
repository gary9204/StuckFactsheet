"""
Defines generic control to produce views of :class:`~.IdCore`
identity attributes.
"""
import abc
import typing   # noqa

import factsheet.model.idcore as MIDCORE


class ControlIdCore(typing.Generic[
        MIDCORE.ViewName, MIDCORE.ViewSummary, MIDCORE.ViewTitle],
        abc.ABC):
    """Mediates addition of views of identity attributes.

    :param p_id_core: identity model.
    """

    # def __init__(self, p_idcore: MIDCORE.IdCore) -> None:
    #     self._idcore = p_idcore

    @abc.abstractmethod
    def new_view_name(self) -> MIDCORE.ViewName:
        """Return view to display name."""
        raise NotImplementedError
        # return self._idcore.new_view_name()

    @abc.abstractmethod
    def new_view_summary(self) -> MIDCORE.ViewSummary:
        """Return view to display summary."""
        raise NotImplementedError
        # return self._idcore.new_view_summary()

    @abc.abstractmethod
    def new_view_title(self) -> MIDCORE.ViewTitle:
        """Return view to display title."""
        raise NotImplementedError
        # return self._idcore.new_view_title()
