"""
Defines factsheet-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``sheet`` defines
class representing the model of a factsheet.
"""
import logging
import typing   # noqa

# from factsheet.abc_types import abc_outline as ABC_OUTLINE
# from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet import bridge_ui as BUI
# from factsheet.abc_types import abc_topic as ABC_TOPIC
import factsheet.model.idcore as MIDCORE
# from factsheet.model import types_model as MTYPES
# from factsheet.view import types_view as VTYPES
# from factsheet.view import ui as UI

logger = logging.getLogger('Main.model.sheet')


NameSheet = BUI.ModelGtkEntryBuffer
SummarySheet = BUI.ModelGtkTextBuffer
TitleSheet = BUI.ModelGtkEntryBuffer
ViewNameSheetActive = BUI.ViewTextMarkup
ViewNameSheetPassive = BUI.ViewTextDisplay
ViewSummarySheetActive = BUI.ViewTextTagged
ViewSummarySheetPassive = BUI.ViewTextTagged
ViewTitleSheetActive = BUI.ViewTextMarkup
ViewTitleSheetPassive = BUI.ViewTextDisplay


class Sheet(MIDCORE.IdCore[ViewNameSheetActive, ViewNameSheetPassive,
                           ViewSummarySheetActive, ViewSummarySheetPassive,
                           ViewTitleSheetActive, ViewTitleSheetPassive]):
    """Factsheet document :mod:`~factsheet.model`.

    Class ``Sheet`` represents an entire Factsheet document.  A model
    factsheet consists of a hierarchy of topics along with
    identification information (see :class:`.IdCore`.) Each topic
    represents a collection of facts about a specific subject.

    .. admonition:: About Equality

        Two factsheet are equivalent when they have the same topic
        outlines and identification information. Transient aspects of
        the factsheets (like windows) are not compared and may be
        different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same topics and identity
        information.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False
        # if not isinstance(p_other, Sheet):
        #     return False

        # if self._infoid != p_other._infoid:
        #     return False

        # if self._topics != p_other._topics:
        #     return False

        return True

    # def __getstate__(self) -> typing.Dict:
    #     """Return factsheet model in form pickle can persist.
    #
    #     Persistent form of factsheet excludes run-time information .
    #     """
    #     state = self.__dict__.copy()
    #     # del state['_pages']
    #     # del state['_stale']
    #     return state

    def __init__(self, *, p_name: str = 'Unnamed', p_summary: str = '',
                 p_title: str = '', **kwargs: typing.Any) -> None:
        """Initialize factsheet with given identity and no topics.

        :param p_name: name of factsheet.
        :param p_summary: summary of factsheet.
        :param p_title: title of factsheet.
        :param kwargs: superclass keyword parameters.
        """
        super().__init__(
            p_name=p_name, p_summary=p_summary, p_title=p_title, **kwargs)

    # def __setstate__(self, p_state: typing.Dict) -> None:
    #     """Reconstruct factsheet model from state pickle loads.
    #
    #     Reconstructed attribute is marked fresh and has no views.
    #
    #     :param p_state: unpickled state of stored factsheet model.
    #     """
    #     self.__dict__.update(p_state)
    #     # self._state_transient()

    # def _state_transient(self) -> None:
    #     """Helper ensures initialization and pickling are consistent."""
    #     raise NotImplementedError
    #     # self._stale = False
    #     # self._pages: typing.Dict[int, ABC_SHEET.InterfacePageSheet] = dict()

    # def attach_view_topics(self, p_view: VTYPES.ViewOutlineTopics) -> None:
    #     """Add view to update dialpay when topics outline changes.
    #
    #     :param p_view: topics outline view to add.
    #     """
    #     self._topics.attach_view(p_view)

    def clear(self) -> None:
        """Remove all topics from the topics outline."""
        raise NotImplementedError
        # self.set_stale()
        # self._close_topic(None)
        # self._topics.clear()

    # def detach_view_topics(self, p_view: VTYPES.ViewOutlineTopics) -> None:
    #     """Remove topics outline view.
    #
    #     :param p_view: topics outline view to remove.
    #     """
    #     self._topics.detach_view(p_view)

    def extract_topic(self, p_i: typing.Any) -> None:
        """Remove topic and all its descendants from topic outline.

        :param p_i: index of parent topic to remove along with all
            descendants.  If index is None, remove no topics.
        """
        raise NotImplementedError
        # if p_i is not None:
        #     self.set_stale()
        #     self._close_topic(p_i)
        #     self._topics.extract_section(p_i)

    def _close_topic(self, p_i: typing.Any) -> None:
        """Signal all pages to close panes for a topic and all its descendants.

        :parm p_i: index of parent topic to close form along with all
            descendants.  If index is None, close all topic panes.
        """
        raise NotImplementedError
        # for index in self._topics.indices(p_i):
        #     topic = self._topics.get_item(index)
        #     assert topic is not None
        #     id_topic = topic.tag
        #     for page in self._pages.values():
        #         page.close_topic(id_topic)

    def insert_topic_after(self, p_topic: typing.Any,
                           p_i: typing.Any) -> typing.Any:
        """Adds topic to topics outline after topic at given index.

        If index is None, adds topic at beginning of outline.

        :param p_topic: new topic to add.
        :param p_i: index of topic to precede new topic.
        :returns: index of newly-added topic.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._topics.insert_after(p_topic, p_i)

    def insert_topic_before(self, p_topic: typing.Any,
                            p_i: typing.Any) -> typing.Any:
        """Adds topic to topics outline before topic at given index.

        If index is None, adds topic at end of outline.

        :param p_topic: new topic to add.
        :param p_i: index of topic to follow new topic.
        :returns: index of newly-added topic.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._topics.insert_before(p_topic, p_i)

    def insert_topic_child(self, p_topic: typing.Any,
                           p_i: typing.Any) -> typing.Any:
        """Adds topic to topic outline as child of topic at given index.

        Method adds topic after all existing children.  If index is
        None, it adds topic at end of outline.

        :param p_topic: new topic to add.
        :param p_i: index of parent topic for new topic.
        :returns: index of newly-added topic.
        """
        raise NotImplementedError
        # self.set_stale()
        # return self._topics.insert_child(p_topic, p_i)

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to factsheet."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        factsheet.
        """
        if super().is_stale():
            return True

        # for index in self._topics.indices():
        #     topic = self._topics.get_item(index)
        #     assert topic is not None
        #     if topic.is_stale():
        #         self._stale = True
        #         return True

        return False

    def _new_model(self) -> typing.Tuple[NameSheet, SummarySheet, TitleSheet]:
        """Return (name, summary, title) store."""
        name = NameSheet()
        summary = SummarySheet()
        title = TitleSheet()
        return name, summary, title

    def set_fresh(self) -> None:
        """Mark factsheet in memory consistent with file contents."""
        super().set_fresh()
        # for index in self._topics.indices():
        #     topic = self._topics.get_item(index)
        #     assert topic is not None
        #     topic.set_fresh()

    # def set_stale(self) -> None:
    #     """Mark factsheet in memory changed from file contents."""
    #     raise NotImplementedError
    #     self._stale = True

    def topics(self, p_index: typing.Any = None
               ) -> typing.Iterator[typing.Any]:
        """Return iterator over topics in topics outline.

        The iterator is recursive (that is, includes topic at given
        index along with all its descendants).

        :param p_index: index of parent item of section.  Default
            iterates over entire outline.
        """
        raise NotImplementedError
        # for index in self._topics.indices(p_index):
        #     topic = self._topics.get_item(index)
        #     assert topic is not None
        #     yield topic
