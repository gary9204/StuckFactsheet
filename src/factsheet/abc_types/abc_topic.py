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


class InterfacePaneTopic(abc.ABC):
    """Defines interface for :class:`~.model.topic.Topic` model to
    signal :class:`~.view.pane_topic.PaneTopic`.
    """

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of topic identification information."""
        raise NotImplementedError
