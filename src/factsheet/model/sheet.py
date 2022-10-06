"""
Defines factsheet-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``sheet`` defines
class representing the model of a factsheet.

.. data:: Name

    Type alias for name of Factsheet.  See :data:`~.control_sheet.DisplayName`
    and :data:`~.control_sheet.EditorName`.

.. data:: Summary

    Type alias for summary of Factsheet.  See
    :data:`~.control_sheet.DisplaySummary` and
    :data:`~.control_sheet.EditorSummary`.

.. data:: Title

    Type alias for title of Factsheet.  See
    :data:`~.control_sheet.DisplayTitle` and
    :data:`~.control_sheet.EditorTitle`.

.. data:: Topics

    Type alias for topics of Factsheet.  See
    :data:`~.control_sheet.ViewTopics`.
"""
import logging
import typing

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE
import factsheet.model.topic as MTOPIC

logger = logging.getLogger('Main.model.sheet')

Name = BUI.x_b_t_ModelTextMarkup
Summary = BUI.ModelTextStyled
OutlineTopics = BUI.ModelOutlineMulti[MTOPIC.Topic]
Title = BUI.x_b_t_ModelTextMarkup
TagSheet = typing.NewType('TagSheet', int)


class Sheet(MIDCORE.IdCore[Name, Summary, Title]):
    """Factsheet document :mod:`~factsheet.model`.

    Class ``Sheet`` represents an entire Factsheet document.  A model
    factsheet consists of a outline of topics along with identification
    information (see :class:`.IdCore`). Each topic represents a
    collection of facts about a specific subject.

    .. admonition:: About Equality

        Each factsheet model has persistent identification information
        and a topic outline.  In addition, a factsheet model may have
        transient aspects such as change state with respect to file
        storage,

        Two factsheet are equal when their identification information
        are equal and their topic outlines are equal.  Transient
        aspects of the factsheets are not compared and may be different.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has same topics and identity
        information.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._topics != p_other._topics:
            return False

        return True

    def __init__(self, *, p_name: str = 'Unnamed',
                 p_summary: str = 'Edit factsheet description here.',
                 p_title: str = 'New Factsheet',
                 **kwargs: typing.Any) -> None:
        """Initialize factsheet with given identity and no topics.

        :param p_name: name of factsheet.
        :param p_summary: summary of factsheet.
        :param p_title: title of factsheet.
        :param kwargs: superclass keyword parameters.
        """
        self._name = Name(p_text=p_name)
        self._summary = Summary(p_text=p_summary)
        self._title = Title(p_text=p_title)
        self._topics = OutlineTopics()
        super().__init__(**kwargs)

    def clear(self) -> None:
        """Mark topics outline stale and remove all topics from outline."""
        self.set_stale()
        self._topics.clear()

    def get_tag(self, p_line: BUI.LineOutline) -> MTOPIC.TagTopic:
        """Return tag of topic at given line in topics outline.

        :param p_line: line of desired topic.
        """
        NO_TOPIC = 0
        tag = MTOPIC.TagTopic(NO_TOPIC)
        topic = self._topics.get_item(p_line)
        if topic is not None:
            tag = topic.tag
        return tag

    def insert_topic_after(self, p_topic: MTOPIC.Topic,
                           p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Adds topic to topics outline after topic at given line.

        If line is None, adds topic at beginning of outline.

        :param p_topic: new topic to add.
        :param p_line: line of topic to precede new topic.
        :returns: line of newly-added topic.
        """
        self.set_stale()
        return self._topics.insert_after(p_topic, p_line)

    def insert_topic_before(self, p_topic: MTOPIC.Topic,
                            p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Adds topic to topics outline before topic at given line.

        If line is None, adds topic at end of outline.

        :param p_topic: new topic to add.
        :param p_line: line of topic to follow new topic.
        :returns: line of newly-added topic.
        """
        self.set_stale()
        return self._topics.insert_before(p_topic, p_line)

    def insert_topic_child(self, p_topic: MTOPIC.Topic,
                           p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Adds topic to topics outline as child of topic at given line.

        Adds topic after all existing children.  If line is None, it
        adds topic at end of outline.

        :param p_topic: new topic to add.
        :param p_line: line of parent topic for new topic.
        :returns: line of newly-added topic.
        """
        self.set_stale()
        return self._topics.insert_child(p_topic, p_line)

    def has_not_changed(self) -> bool:
        """Return True when there are no unsaved changes to factsheet."""
        return not self.is_stale()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        factsheet.

        Log warning when a topic is missing from the topics outline.
        """
        if super().is_stale():
            return True

        for topic in self._topics.items():
            if topic is None:
                logger.warning(
                    'Topics outline contains line with no topic ({}.{})'
                    ''.format(self.__class__.__name__, self.is_stale.__name__))
            elif topic.is_stale():
                self._stale = True
                return True

        return False

    @property
    def outline_topics(self) -> OutlineTopics:
        """Return topics outline."""
        return self._topics

    def remove_topic(self, p_line: BUI.LineOutline) -> None:
        """Mark topics outline stale and remove topic from outline.

        Removes topic and all its descendents.

        :param p_line: line of topic to remove.  If line is None or
            invalid, remove no topics but mark sheet as stale nonetheless.
        """
        self.set_stale()
        self._topics.remove(p_line)

    def set_fresh(self) -> None:
        """Mark factsheet in memory consistent with file contents."""
        super().set_fresh()
        for topic in self._topics.items():
            if topic is None:
                logger.warning('Topics outline contains line with no '
                               'topic ({}.{})'.format(self.__class__.__name__,
                                                      self.set_fresh.__name__))
            else:
                topic.set_fresh()

    @property
    def tag(self) -> TagSheet:
        """Return unique identifier of sheet."""
        return TagSheet(id(self))

    def topics(self, p_line: BUI.LineOutline = None
               ) -> typing.Iterator[MTOPIC.Topic]:
        """Return iterator over topics in section of topics outline.

        The iterator is recursive (that is, includes topic at given
        line along with all its descendants).

        Log warning when a topic is missing from the topics outline.

        :param p_line: line of parent item of section.  Default
            iterates over entire outline.
        """
        for topic in self._topics.items_section(p_line):
            if topic is None:
                logger.warning(
                    'Topics outline contains line with no topic ({}.{})'
                    ''.format(self.__class__.__name__, self.topics.__name__))
            else:
                yield topic
