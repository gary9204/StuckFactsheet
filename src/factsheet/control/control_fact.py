"""
Defines control to add and remove views of :class:`~.Fact' attributes.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  This module defines the control
class for the fact layer.
"""
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.control.control_idcore as CIDCORE
import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE

ViewAspect = BUI.ViewAspectAny
ViewAspectMissing = BUI.ViewAspectMissing
ViewNameFact = BUI.ViewTextMarkup
ViewNamesAspect = BUI.ViewOutlineSelect
ViewNoteFact = BUI.ViewTextFormat
ViewSummaryFact = BUI.ViewTextFormat
ViewTitleFact = BUI.ViewTextMarkup


class ControlFact(
        CIDCORE.ControlIdCore[ViewNameFact, ViewSummaryFact, ViewTitleFact]):
    """Mediates addition and removal of views of fact attributes.

    :param p_fact: add and remove views of this model.
    """

    def __init__(self, p_fact: MFACT.Fact) -> None:
        self._fact = p_fact

    def attach_aspect(self, p_name: str) -> ViewAspect:
        """Return view associated with named fact aspect.

        If no aspect matches name, return a warning view.

        :param p_name: name of aspect to associate.
        """
        aspect = self._fact.get_aspect(p_name)
        if aspect is not None:
            view = aspect.attach_view()
        else:
            view = ViewAspectMissing()
            warning = ('Aspect \'{}\' not found. Please report omission.'
                       ''.format(p_name))
            view.set_text(warning)
        return view

    def attach_names_aspect(self) -> ViewNamesAspect:
        """Return view of names of fact's aspects."""
        return self.fact.names_aspect.attach_view()

    def attach_note(self) -> ViewNoteFact:
        """Return view of fact's note."""
        return self.fact.note.attach_view()

    def detach_aspect(self, p_name: str, p_view: ViewAspect) -> None:
        """Disassociate view from named fact aspect.

        :param p_name: name of aspect to disassociate.
        :param p_view: view to disassociate.
        """
        aspect = self._fact.get_aspect(p_name)
        if aspect is not None:
            aspect.detach_view(p_view)

    def detach_names_aspect(self, p_view: ViewNamesAspect) -> None:
        """Disassociate view from names of fact's aspects."""
        self.fact.names_aspect.detach_view(p_view)

    def detach_note(self, p_view: ViewNoteFact) -> None:
        """Disassociate view from fact's note."""
        self.fact.note.detach_view(p_view)

    @property
    def fact(self) -> MFACT.Fact:
        """Return fact."""
        return self._fact

    @property
    def idcore(self) -> MIDCORE.IdCore:
        """Return identity of fact."""
        return self._fact
