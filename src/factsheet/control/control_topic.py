"""
Defines control to mediate topic-level interaction from
:mod:`~.factsheet.view` to :mod:`~.factsheet.model`.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
class representing the control of a topic.
"""
# import logging
import typing   # noqa

import factsheet.bridge_ui as BUI
import factsheet.control.control_fact as CFACT
import factsheet.control.control_idcore as CIDCORE
# import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE
import factsheet.model.topic as MTOPIC

# from factsheet.model.types_model import IndexFact
# from factsheet.view.types_view import ViewOutlineFacts

# logger = logging.getLogger('Main.control_fact')

ViewNameTopic = BUI.ViewTextMarkup
ViewSummaryTopic = BUI.ViewTextFormat
ViewTitleTopic = BUI.ViewTextMarkup


class ControlTopic(CIDCORE.ControlIdCore[
        ViewNameTopic, ViewSummaryTopic, ViewTitleTopic]):
    """Translates user requests in topic form to updates in topic model.

    :param p_topic: topic model.
    """

    def __init__(self, p_topic: MTOPIC.Topic) -> None:
        self._topic = p_topic
        # self._controls_fact: typing.MutableMapping[
        #     MTYPES.TagFact, CFACT.ControlFact] = dict()
        # for fact in self._topic.facts():
        #     control_new = CFACT.ControlFact(fact)
        #     self._controls_fact[fact.tag] = control_new

    # def attach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
    #     """Add topic form to model.

    #     :param p_form: form to add.
    #     """
    #     assert self._topic is not None
    #     self._topic.attach_form(p_form)

    def check_fact(self, p_i: int) -> None:
        """Request topic check a fact.

        :param p_i: index of fact to check.
        """
        raise NotImplementedError
        # assert self._topic is not None
        # self._topic.check_fact(p_i)

    def clear_all(self) -> None:
        """Request topic clear all of topic's facts. """
        raise NotImplementedError
        # assert self._topic is not None
        # self._topic.clear_all()

    def clear_fact(self, p_i: int) -> None:
        """Request topic clear a fact.

        :param p_i: index of fact to clear.
        """
        raise NotImplementedError
        # assert self._topic is not None
        # self._topic.clear_fact(p_i)

    # def detach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
    #     """Remove topic form from model.

    #     :param p_form: form to remove.
    #     """
    #     assert self._topic is not None
    #     self._topic.detach_form(p_form)

    def get_control_fact(self, p_fact: str
                         ) -> typing.Optional[CFACT.ControlFact]:
        """Return fact control for given fact or None when no control.

        :param p_fact: fact corresponding to desired control.
        """
        raise NotImplementedError
        # id_control = p_fact.tag
        # try:
        #     return self._controls_fact[id_control]
        # except KeyError:
        #     return None

    @property
    def topic(self) -> MTOPIC.Topic:
        """Return topic."""
        return self._topic

    @property
    def idcore(self) -> MIDCORE.IdCore:
        """Return identity of topic."""
        return self._topic
