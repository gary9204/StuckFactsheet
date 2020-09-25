"""
Defines class that mediates topic-level interaction from
:class:`~.FormTopic` to :class:`~.Topic`.

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
    """Translates user requests in topic form to updates in topic model.

    :param p_topic: topic model.
    """

    def __init__(self, p_model: MTOPIC.Topic) -> None:
        self._model = p_model

    def attach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Add topic form to model.

        :param p_form: form to add.
        """
        assert self._model is not None
        self._model.attach_form(p_form)

    def detach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Remove topic form from model.

        :param p_form: form to remove.
        """
        assert self._model is not None
        self._model.detach_form(p_form)
