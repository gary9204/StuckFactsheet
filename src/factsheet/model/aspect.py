"""
Defines classes for presentation of fact attributes.

.. data:: SubjectAny

    Type hint for arbitrary attribute of a fact.

.. data:: ViewAspectPlain

    Type hint for plain text presentation of a fact attribute.
"""
import abc
import typing

import factsheet.bridge_ui as BUI

SubjectAny = typing.Any
SubjectOpaque = typing.TypeVar('SubjectOpaque')
# ViewAspectBridge = typing.TypeVar('ViewAspectBridge')
# ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = BUI.ViewTextStatic


class Aspect(abc.ABC, typing.Generic[SubjectOpaque]):
    """Presentation for an attribute of a fact.

    A fact has attributes of interest to a user including fact status
    and value.  There may be multiple ways to present the value of a
    fact.  For example, a fact value may have presentations as plain
    text, formatted text, a list, or a table.  Class :class:`~.Aspect`
    puts a fact attribute into a form suitable for a presentation and
    manages views of that presentation.
    """

    @abc.abstractmethod
    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has comparable type.

        :param p_other: object to compare with self.
        """
        if not isinstance(p_other, type(self)):
            return False

        return True

    @abc.abstractmethod
    def __init__(self) -> None:
        """Initialize with default presentation."""
        raise NotImplementedError

    @abc.abstractmethod
    def clear_presentation(self) -> None:
        """Clear presentation to default.

        Typically, the default presentation is blank text or empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view(self) -> BUI.ViewAny:
        """Return new view of the presentation."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_presentation(self, p_subject: SubjectOpaque) -> None:
        """Set presentation to match given attribute.

        :param p_subject: fact attribute to use for presentation.
        """
        raise NotImplementedError


# class AspectBridge(Aspect[BasisBridge, ViewAspectBridge],
#                    typing.Generic[ViewAspectBridge]):
#     """Adapts a fact aspect stored as a bridge class."""
#
#     def __eq__(self, p_other: typing.Any) -> bool:
#         """Return True when p_other is comparable type with same
#         content.
#
#         :param p_other: object to compare with self.
#         """
#         if not super().__eq__(p_other):
#             return False
#
#         if self._presentation != p_other._basis:
#             return False
#
#         return True
#
#     def __init__(self, p_subject: BasisBridge) -> None:
#         """Initialize instance.
#
#         :param p_subject: aspect of fact to use for presentation.
#         """
#         self._presentation = p_subject
#
#     def new_view(self) -> ViewAspectBridge:
#         """Return new view of fact presentation."""
#         return self._presentation.new_view()
#
#     def set_presentation(self) -> None:
#         """Synchronize presentation with fact information."""
#         pass


class AspectPlain(Aspect[SubjectAny]):
    """Plain text presentation of a fact attribute."""

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other is comparable type with same text.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._presentation != p_other._presentation:
            return False

        return True

    def __init__(self) -> None:
        """Initialize blank text presentation."""
        self._presentation = BUI.BridgeTextStatic()
        self.clear_presentation()

    def clear_presentation(self) -> None:
        """Clear presentation to blank text."""
        self._presentation.text = ''

    def new_view(self) -> ViewAspectPlain:
        """Return new view of presentation."""
        return self._presentation.new_view()

    def set_presentation(self, p_subject: SubjectAny) -> None:
        """Set presentation to match given attribute.

        :param p_subject: fact attribute to use for presentation.
        """
        self._presentation.text = str(p_subject)
