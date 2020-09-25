"""
Defines abstract interfaces for topics.

:doc:`../guide/devel_notes` describes the use of abstract classes to
break ``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_topic`` defines interface for topic view (:class:`.FormTopic`) for
encapsulation.

.. data:: TagTopic

    Type for topic identifiers.
"""
import abc
import typing

import factsheet.abc_types.abc_infoid as ABC_INFOID
import factsheet.abc_types.abc_stalefile as ABC_STALE

from factsheet.abc_types.abc_outline import IndexOpaque


TagTopic = typing.NewType('TagTopic', int)


class AbstractTopic(
        ABC_INFOID.AbstractIdentity[TagTopic], ABC_STALE.InterfaceStaleFile):
    """Defines interfaces common to topic model components."""

    @abc.abstractmethod
    def check_fact(self, p_tag_fact: IndexOpaque) -> None:
        """Check a fact.

        :param p_tag_fact: determines which fact to check.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def clear_all(self) -> None:
        """Clear all of topic's facts. """
        raise NotImplementedError

    @abc.abstractmethod
    def clear_fact(self, p_tag_fact: IndexOpaque) -> None:
        """Clear a fact.

        :param p_tag_fact: determines which fact to clear.
        """
        raise NotImplementedError


class InterfaceFormTopic(abc.ABC):
    """Defines interface for :class:`.Topic` to signal :class:`.FormTopic`."""

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of topic identification information."""
        raise NotImplementedError
