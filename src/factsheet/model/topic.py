"""
Defines topic-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``topic`` defines
the base class representing the model of a topic.  Additional classes
specialize the model for sets, operations, and so on.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.model import infoid as MINFOID

logger = logging.getLogger('Main.model.topic')


class Topic(ABC_TOPIC.AbstractTopic):
    """Topic component of Factsheet :mod:`~factsheet.model`.

    Class ``Topic`` represents a specific subject within a Factsheet.
    A model topic consists of an outline of facts along with
    identification information (see :class:`.InfoId`.) Each fact
    represents statement about the topic's subject.

    :param p_name: name of topic.
    :param p_summary: summary of topic.
    :param p_title: title of topic.

    .. admonition:: About Equality

        Two topics are equivalent when they have the same fact outlines
        and identification information. Transient aspects of the topics
        (like views) are not compared and may be different.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same topic information.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, Topic):
            return False

        if self._infoid != px_other._infoid:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return topic model in form pickle can persist.

        Persistent form of topic excludes run-time information.
        """
        state = self.__dict__.copy()
        del state['_views']
        del state['_stale']
        return state

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', **_kwargs: typing.Dict) -> None:
        self._infoid = MINFOID.InfoId(
            p_name=p_name, p_summary=p_summary, p_title=p_title)
        self._state_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct topic model from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored topic model.
        """
        self.__dict__.update(px_state)
        self._state_transient()

    def _state_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._stale = False
        self._views: typing.Dict[int, ABC_TOPIC.InterfaceFormTopic] = dict()

    def attach_view(self, pm_view: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Add view to update display when topic changes.

        Log warning when requested view is already attached.

        :param pm_view: view to add.

        """
        id_view = id(pm_view)
        if id_view in self._views.keys():
            logger.warning(
                'Duplicate view: {} ({}.{})'.format(
                    hex(id_view),
                    self.__class__.__name__, self.attach_view.__name__))
            return

        self._infoid.attach_view(pm_view.get_infoid())
        self._views[id_view] = pm_view

    def detach_all(self) -> None:
        """Detach all views from topic."""
        while self._views:
            _id_view, view = self._views.popitem()
            self._detach_attribute_views(view)

    def detach_view(self, px_view: ABC_TOPIC.InterfaceFormTopic) -> None:
        """Remove one view from topic.

        Log warning when requested view is not attached.

        :param px_view: view to remove.
        """
        id_view = id(px_view)
        try:
            self._views.pop(id_view)
        except KeyError:
            logger.warning(
                'Missing view: {} ({}.{})'.format(
                    hex(id_view),
                    self.__class__.__name__, self.detach_view.__name__))
            return

        self._detach_attribute_views(px_view)

    def _detach_attribute_views(
            self, pm_view: ABC_TOPIC.InterfaceFormTopic) -> None:
        """For each topic attribute with a distinct view, remove the
        view for the attribute.

        :param pm_view: view of topic as a whole.
        """
        self._infoid.detach_view(pm_view.get_infoid())

    @property
    def id_topic(self) -> ABC_TOPIC.IdTopic:
        """Return topic identifier. """
        return ABC_TOPIC.IdTopic(self._infoid.id_model)

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to topic."""
        if self._stale:
            return False

        if self._infoid.is_stale():
            self._stale = True
            return False

        return True

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        topic.
        """
        if self._stale:
            return True

        if self._infoid.is_stale():
            self._stale = True
            return True

        return False

    @property
    def name(self) -> str:
        """Return topic name."""
        return self._infoid.name

    def set_fresh(self) -> None:
        """Mark topic in memory consistent with file contents."""
        self._stale = False
        self._infoid.set_fresh()

    def set_stale(self) -> None:
        """Mark topic in memory changed from file contents."""
        self._stale = True

    @property
    def summary(self) -> str:
        """Return topic summary."""
        return self._infoid.summary

    @property
    def title(self) -> str:
        """Return topic title."""
        return self._infoid.title
