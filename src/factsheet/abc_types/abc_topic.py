"""
Defines abstract interfaces for topics.

:doc:`../guide/devel_notes` describes the use of abstract classes to
break ``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_topic`` defines interface for topic view (:class:`.PaneTopic`) for
encapsulation.
"""
import abc

from factsheet.abc_types import abc_infoid as ABC_INFOID
# from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.abc_types import abc_stalefile as ABC_STALE


class AbstractTopic(ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to topic model components."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return topic name. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """Return topic title. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def summary(self) -> str:
        """Return topic summary. """
        raise NotImplementedError


class InterfacePaneTopic(abc.ABC):
    """Defines interface for :class:`~.model.topic.Topic` model to
    signal :class:`~.view.pane_topic.PaneTopic`.
    """

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of topic identification information."""
        raise NotImplementedError

#     @abc.abstractmethod
#     def get_view_facts(self) -> ABC_OUTLINE.AbstractViewOutline:
#         """Return view of topic's fact outline."""
#         raise NotImplementedError
