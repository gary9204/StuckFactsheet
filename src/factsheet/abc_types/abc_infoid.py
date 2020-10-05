"""
Defines interface for information to identify model components.

:doc:`../guide/devel_notes` describes the use of interface classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_infoid`` defines an interface for model
text attribute classes.  See :mod:`.adapt_infoid` for an implementation
of the interface with GTK.

.. data:: IdNameOpaque

    Type hint for generic name of a model component.

.. data:: IdSummaryOpaque

    Type hint for generic summary of a model component.

.. data:: IdTitleOpaque

    Type hint for generic title of a model component.

.. data:: TagOpaque

    Type hint for generic tag to identify a model component.
"""
import abc
import typing

IdNameOpaque = typing.TypeVar('IdNameOpaque')
IdSummaryOpaque = typing.TypeVar('IdSummaryOpaque')
IdTitleOpaque = typing.TypeVar('IdTitleOpaque')
TagOpaque = typing.TypeVar('TagOpaque')


class InterfaceIdentity(abc.ABC, typing.Generic[
        IdNameOpaque, IdSummaryOpaque, IdTitleOpaque, TagOpaque]):
    """Identification information of Factsheet model components
    :class:`.Sheet`, :class:`.Topic`, and :class:`.Fact`.
    """

    @property
    @abc.abstractmethod
    def name(self) -> IdNameOpaque:
        """Return component name.

        Name is a short, editable identifier (suitable, for example, as
        label).
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def summary(self) -> IdSummaryOpaque:
        """Return component summary.

        Summary is an editable description of component, which adds
        detail to title.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def tag(self) -> TagOpaque:
        """Return component tag.

        Tag is identifies a component. A tag is unique for lifetime of
        the component.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> IdTitleOpaque:
        """Return component title.

        Title is a one-line, editable description of component contents.
        """
        raise NotImplementedError
