"""
Defines class that mediates fact-level interaction from
:class:`~.BlockFact` to :class:`~.Fact`.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, opic, and fact layers.  Module ``fact`` defines
class representing the control of a fact.
"""
import logging
import typing   # noqa

import factsheet.abc_types.abc_fact as ABC_FACT
import factsheet.model.fact as MFACT

from factsheet.abc_types.abc_fact import ValueOpaque

logger = logging.getLogger('Main.control_fact')


class ControlFact(typing.Generic[ValueOpaque]):
    """Translates user requests in fact block to updates in fact model.

    :param p_fact: fact model.
    """

    def __init__(self, p_fact: MFACT.Fact) -> None:
        self._fact = p_fact

    def attach_block(self, p_block: ABC_FACT.InterfaceBlockFact[ValueOpaque]
                     ) -> None:
        """Add fact block to fact model.

        :param p_block: block to add.
        """
        self._fact.attach_block(p_block)

    def detach_block(self, p_block: ABC_FACT.InterfaceBlockFact[ValueOpaque]
                     ) -> None:
        """Remove fact block from fact model.

        :param p_block: block to remove.
        """
        self._fact.detach_block(p_block)
