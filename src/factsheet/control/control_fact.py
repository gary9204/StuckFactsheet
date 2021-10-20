"""
Defines control to add and remove views of :class:`~.Fact' attributes.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  This module defines the control
class for the fact layer.
"""
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.model.fact as MFACT


class ControlFact(CIDCORE.ControlIdCore[
        MFACT.ViewNameFact, MFACT.ViewSummaryFact, MFACT.ViewTitleFact]):
    """Mediates addition and removal of views of fact attributes.

    :param p_fact: add and remove views of this model.
    """

    def __init__(self, p_fact: MFACT.Fact) -> None:
        self._fact = p_fact

    def new_view_aspect(self, p_name_aspect: str) -> BUI.ViewAny:
        """Return view of aspect with given name or placeholder if name
        not found.

        :param p_name_aspect: name of desired aspect.
        """
        return self._fact.new_view_aspect(p_name_aspect)

    def new_view_names_aspects(self) -> MFACT.ViewNamesAspects:
        """Return view of names of aspects for the fact."""
        return self._fact.new_view_names_aspects()

    def new_view_name_active(self) -> MFACT.ViewNameFact:
        """Return view to display name."""
        return self._fact.new_view_name_active()

    def new_view_note(self) -> MFACT.ViewNoteFact:
        """Return view of fact's note."""
        return self._fact.new_view_note()

    def new_view_status(self):
        """Return view of fact's status."""
        return self._fact.new_view_status()

    def new_view_summary_active(self) -> MFACT.ViewSummaryFact:
        """Return view to display summary."""
        return self._fact.new_view_summary_active()

    def new_view_tag(self):
        """Return view of fact's tag."""
        return self._fact.new_view_tag()

    def new_view_title_active(self) -> MFACT.ViewTitleFact:
        """Return view to display title."""
        return self._fact.new_view_title_active()
