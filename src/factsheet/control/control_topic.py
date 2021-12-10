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

# import factsheet.bridge_ui as BUI
import factsheet.model.topic as MTOPIC
# import factsheet.control.control_fact as CFACT
# import factsheet.control.control_idcore as CIDCORE
# import factsheet.model.fact as MFACT
# import factsheet.model.idcore as MIDCORE

# from factsheet.model.types_model import IndexFact
# from factsheet.view.types_view import ViewOutlineFacts

# logger = logging.getLogger('Main.control_fact')

# ViewNameTopic = BUI.ViewTextMarkup
# ViewSummaryTopic = BUI.ViewTextTagged
# ViewTitleTopic = BUI.ViewTextMarkup


class ControlTopic:
    """Translates user requests in topic view to updates in topic model.
    """

    def __init__(self, p_model: MTOPIC.Topic) -> None:
        """Initialize model and view factories.

        :param p_model: topic model.
        """
        self._model = p_model
        self._factory_display_name = (
            MTOPIC.FactoryDisplayName(self._model.name))
        self._factory_editor_name = (
            MTOPIC.FactoryEditorName(self._model.name))

        self._factory_display_summary = (
            MTOPIC.FactoryDisplaySummary(self._model.summary))
        self._factory_editor_summary = (
            MTOPIC.FactoryEditorSummary(self._model.summary))

        self._factory_display_title = (
            MTOPIC.FactoryDisplayTitle(self._model.title))
        self._factory_editor_title = (
            MTOPIC.FactoryEditorTitle(self._model.title))

        # self._controls_fact: typing.MutableMapping[
        #     MTYPES.TagFact, CFACT.ControlFact] = dict()
        # for fact in self._model.facts():
        #     control_new = CFACT.ControlFact(fact)
        #     self._controls_fact[fact.tag] = control_new

    def check_fact(self, p_i: int) -> None:
        """Request topic check a fact.

        :param p_i: index of fact to check.
        """
        raise NotImplementedError
        # assert self._model is not None
        # self._model.check_fact(p_i)

    def clear_all(self) -> None:
        """Request topic clear all of topic's facts. """
        raise NotImplementedError
        # assert self._model is not None
        # self._model.clear_all()

    def clear_fact(self, p_i: int) -> None:
        """Request topic clear a fact.

        :param p_i: index of fact to clear.
        """
        raise NotImplementedError
        # assert self._model is not None
        # self._model.clear_fact(p_i)

    # def detach_form(self, p_form: ABC_TOPIC.InterfaceFormTopic) -> None:
    #     """Remove topic form from model.

    #     :param p_form: form to remove.
    #     """
    #     assert self._model is not None
    #     self._model.detach_form(p_form)

    def get_control_fact(self, p_fact: str) -> typing.Optional[typing.Any]:
        """Return fact control for given fact or None when no control.

        :param p_fact: fact corresponding to desired control.
        """
        raise NotImplementedError
        # id_control = p_fact.tag
        # try:
        #     return self._controls_fact[id_control]
        # except KeyError:
        #     return None

    # @property
    # def name(self) -> str:
    #     """Return sheet name without markup errors."""
    #     name = BUI.escape_text_markup(self._model.name.text)
    #     return name

    @property
    def new_display_name(self) -> MTOPIC.DisplayName:
        """Return factory for displays of topic names."""
        return self._factory_display_name

    @property
    def new_editor_name(self) -> MTOPIC.EditorName:
        """Return factory for editors of topic names."""
        return self._factory_editor_name

    @property
    def new_display_summary(self) -> MTOPIC.DisplaySummary:
        """Return factory for displays of topic summaries."""
        return self._factory_display_summary

    @property
    def new_editor_summary(self) -> MTOPIC.EditorSummary:
        """Return factory for editors of topic summaries."""
        return self._factory_editor_summary

    @property
    def new_display_title(self) -> MTOPIC.DisplayTitle:
        """Return factory for displays of topic titles."""
        return self._factory_display_title

    @property
    def new_editor_title(self) -> MTOPIC.EditorTitle:
        """Return factory for editors of topic titles."""
        return self._factory_editor_title

    # @property
    # def topic(self) -> MTOPIC.Topic:
    #     """Return topic."""
    #     return self._model

    # @property
    # def idcore(self) -> MIDCORE.IdCore:
    #     """Return identity of topic."""
    #     return self._model
