"""
Defines abstract classes and interfaces for identification information.

:doc:`../guide/devel_notes` describes the use of abstract classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_infoid`` defines abstract text attribute
classes for :class:`.InfoId` and :class:`.ViewInfoId`.

See :class:`.InfoId`, :class:`.ViewInfoId`, and derived classes.

.. data:: TagOpaque

    Type hint for generic tag to identify a model component.

.. data:: TextViewOpaque

    Type hint for generic presentation element of a text attribute such
    as a factsheet name or summary.
"""
import abc
import typing

from factsheet.abc_types import abc_stalefile as ABC_STALE

TagOpaque = typing.TypeVar('TagOpaque')
TextViewOpaque = typing.TypeVar('TextViewOpaque')


class AbstractIdentity(abc.ABC, typing.Generic[TagOpaque]):
    """Defines interfaces for identification information of Factsheet
    model components :class:`.Sheet`, :class:`.Topic`, and
    :class:`.Fact.

    The Factsheet model includes components for factsheets, topics, and
    facts.  These components have identification information in common.
    The information consists of the following.

    .. attribute:: name

        Short, editable identifier (suitable, for example, as label).

    .. attribute:: summary

        Editable description of component, which adds detail to title.

    .. attribute:: tag

        Identifier that is unique for lifetime of the component.

    .. attribute:: title

        One-line, editable description of component contents.
    """

    @abc.abstractmethod
    def init_identity(self, *, p_name: str = '', p_summary: str = '',
                      p_title: str = '') -> None:
        """Assign initial name, title, and summary for a model component.

        :param p_name: name for component.
        :param p_summary: summary for component.
        :param p_title: title for component.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return component name."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def summary(self) -> str:
        """Return component summary."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def tag(self) -> TagOpaque:
        """Return tag identifing component."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """Return component title."""
        raise NotImplementedError


class AbstractTextModel(
        ABC_STALE.InterfaceStaleFile, typing.Generic[TextViewOpaque]):
    """Defines interfaces common to model text attributes.

    .. tip:: Two text attributes are equivalent when their string
       representations are the same.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when other is text attribute with same string
        representation.
        """
        if not isinstance(px_other, AbstractTextModel):
            return False

        return str(self) == str(px_other)

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return attribute contents as text."""
        raise NotImplementedError

    @abc.abstractmethod
    def attach_view(self, pm_view: TextViewOpaque):
        """Add view to update display when text changes.

        :param pm_view: view to add.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def detach_view(self, pm_view: TextViewOpaque):
        """Remove view of changes to text.

        :param pm_view: view to removes.
        """
        raise NotImplementedError


class InterfaceViewInfoId(abc.ABC, typing.Generic[TextViewOpaque]):
    """Defines interface to attach identification information view
    (:class:`.ViewInfoId`) to the model (:class:`.InfoId`).
    """

    @abc.abstractmethod
    def get_view_name(self) -> TextViewOpaque:
        """Return view's name display element."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_summary(self) -> TextViewOpaque:
        """Return view's summary display element."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_title(self) -> TextViewOpaque:
        """Return view's title display element."""
        raise NotImplementedError
