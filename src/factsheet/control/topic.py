"""
Defines class that mediates topic-level interaction from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
class representing the control of a topic.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.model import topic as MTOPIC

logger = logging.getLogger('Main.CSHEET')


class Topic:
    """Mediates user actions at view to model updates for a topic.

    Class ``Topic`` translates user requests in a topic view into
    changes in the topic model.
    """

    def __init__(self) -> None:
        self._model: typing.Optional[MTOPIC.Topic] = None

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

    @classmethod
    def new(cls) -> 'Topic':
        """Create and return control with default model.

        :returns: Newly created control.
        """
        control = Topic()
        control._model = MTOPIC.Topic()
        return control

    @classmethod
    def open(cls, pm_model: MTOPIC.Topic) -> 'Topic':
        """Create control with given model.

        :param pm_model: model for new control.
        :returns: Newly created control.
        """
        control = Topic()
        control._model = pm_model
        return control
