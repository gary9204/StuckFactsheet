"""
Defines control to add and remove views of :class:`~.Fact' attributes.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  This module defines the control
class for the fact layer.
"""
import logging
import typing   # noqa

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.control.control_idcore as CIDCORE
import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE

logger = logging.getLogger('Main.control_fact')

ViewNameFact = ADAPT.ViewTextMarkup
ViewNamesFormats = typing.TypeVar('ViewNamesFormats')
ViewNoteFact = ADAPT.ViewTextFormat
ViewSummaryFact = ADAPT.ViewTextFormat
ViewTitleFact = ADAPT.ViewTextMarkup


class ControlFact(
        CIDCORE.ControlIdCore[ViewNameFact, ViewSummaryFact, ViewTitleFact]):
    """Mediates addition and removal of views of fact attributes.

    :param p_fact: add and remove views of this model.
    """

    def __init__(self, p_fact: MFACT.Fact) -> None:
        self._fact = p_fact

    def attach_format_plain(self, p_aspect: ADAPT.AspectValuePlain) -> None:
        """Ask fact to add aspect to plain format.

        :param p_aspect: aspect to add.
        """
        NAME = 'Plain'
        format_value = self._fact.get_format(NAME)
        if format_value is None:
            logger.error('Format missing for {}.{}'.format(
                type(self).__name__, self.attach_format_plain.__name__))
            return

        format_value.attach_aspect(p_aspect)

    def attach_names_formats(self, p_view: ViewNamesFormats) -> None:
        """Ask fact to add view to names of formats.

        :param p_view: view to add.
        """
        raise NotImplementedError
        # self.fact.names_format.attach_view(p_view)

    def attach_note(self, p_view: ViewNoteFact) -> None:
        """Ask fact to add view to note.

        :param p_view: to add.
        """
        self.fact.note.attach_view(p_view)

    def detach_format_plain(self, p_aspect: ADAPT.AspectValuePlain) -> None:
        """Ask fact to remove aspect from plain format.

        :param p_aspect: aspect to remove.
        """
        NAME = 'Plain'
        format_value = self._fact.get_format(NAME)
        if format_value is None:
            logger.error('Format missing for {}.{}'.format(
                type(self).__name__, self.detach_format_plain.__name__))
            return

        format_value.detach_aspect(p_aspect)

    def detach_names_formats(self, p_view) -> None:
        """Ask fact to remove view from names of formats.

        :param p_view: view to remove.
        """
        raise NotImplementedError
        # self.fact.names_format.attach_view(p_view)

    def detach_note(self, p_view: ViewNoteFact) -> None:
        """Ask fact to remove view from note.

        :param p_view: view to remove.
        """
        self.fact.note.detach_view(p_view)

    @property
    def fact(self) -> MFACT.Fact:
        """Return fact."""
        return self._fact

    @property
    def idcore(self) -> MIDCORE.IdCore:
        """Return identity of fact."""
        return self._fact
