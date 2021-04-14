"""
Defines generic control to add and remove views of :class:`~.IdCore`
identity attributes.
"""
import typing   # noqa

import factsheet.model.idcore as MIDCORE


class ControlIdCore(typing.Generic[
        MIDCORE.ViewName, MIDCORE.ViewSummary, MIDCORE.ViewTitle]):
    """Mediates addition of views of identity attributes.

    :param p_id_core: identity model.
    """

    def __init__(self, p_idcore: MIDCORE.IdCore) -> None:
        self._idcore = p_idcore

    def new_view_name(self) -> MIDCORE.ViewName:
        """Return view to display name."""
        return self._idcore.new_view_name()

    def new_view_summary(self) -> MIDCORE.ViewSummary:
        """Return view to display summary."""
        return self._idcore.new_view_summary()

    def new_view_title(self) -> MIDCORE.ViewTitle:
        """Return view to display title."""
        return self._idcore.new_view_title()
