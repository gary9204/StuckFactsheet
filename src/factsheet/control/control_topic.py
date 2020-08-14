"""
Defines class that mediates topic-level interaction from
:class:`~.PaneTopic` to :class:`~.Topic`.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
class representing the control of a topic.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.model import topic as MTOPIC

logger = logging.getLogger('Main.control_fact')


class ControlTopic:
    """Translates user requests in topic pane to updates in topic model.

    :param pm_topic: topic model.
    """

    def __init__(self, pm_model: MTOPIC.Topic) -> None:
        self._model = pm_model

    def attach_view(self, pm_view: ABC_TOPIC.InterfacePaneTopic) -> None:
        """Add view to model.

        :param pm_view: view to add.
        """
        assert self._model is not None
        self._model.attach_view(pm_view)

    def detach_view(self, px_view: ABC_TOPIC.InterfacePaneTopic) -> None:
        """Remove view from model.

        :param px_view: view to remove.
        """
        assert self._model is not None
        self._model.detach_view(px_view)
