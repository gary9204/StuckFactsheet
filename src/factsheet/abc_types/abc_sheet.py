"""
Defines abstract interfaces for factsheet documents.

:doc:`../guide/devel_notes` describes the use of abstract classes break
``import`` cycles and to encapsulate dependencies of
:mod:`~factsheet.model` on a user interface widget toolkit.  Module
``abc_sheet`` defines an abstract interface for factsheet control
(:class:`~.ControlSheet`) to break an ``import`` cycle. It
defines an interface for factsheet view (:class:`.PageSheet`) for
encapsulation. In addition, the module defines an enumeration for
factsheet control method results.
"""
import abc
import enum
from pathlib import Path
import typing



class AbstractTemplate(abc.ABC):
    """Defines interfaces common to templates for model components.

    A template creates a topic in a factsheet topic outline.  See
    :mod:`abc_sheet` and :mod:`abc_outline`.
    """

    @abc.abstractmethod
    def __call__(self) -> typing.Optional[ABC_TOPIC.AbstractTopic]:
        """Return topic based on user's input or None when user cancels."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return template name. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def summary(self) -> str:
        """Return template summary. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """Return template title. """
        raise NotImplementedError


class EffectSafe(enum.Enum):
    """Constants to identify the effect of a call to a safe method (such
    as :meth:`.Sheet.detach_page_safe` and :meth:`.Sheet.delete_safe`).
    """
    #: Method call completed request.
    COMPLETED = enum.auto()
    #: Method call had no effect.
    NO_EFFECT = enum.auto()


class InterfaceControlSheet(abc.ABC):
    """Defines interface class to break import cycle between control
    :class:`~.ControlSheet` and view :class:`.PoolSheets`.
    """

    @property
    @abc.abstractmethod
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        raise NotImplementedError

    @abc.abstractmethod
    def present_factsheet(self, p_time: int) -> None:
        """Make all factsheet pages visible to user.

        :param p_time: timestamp of event requesting presentation.
        """
        raise NotImplementedError


class InterfacePageSheet(
        abc.ABC, typing.Generic[ABC_OUTLINE.ViewOutlineOpaque]):
    """Defines interface for :class:`~.model.sheet.Sheet` model to
    signal :class:`~.view.page_sheet.PageSheet`.
    """

    @abc.abstractmethod
    def close_page(self) -> None:
        """Close page in response to notice from model."""
        raise NotImplementedError

    @abc.abstractmethod
    def close_topic(self, p_id: ABC_TOPIC.TagTopic) -> None:
        """Close topic form in response to notice from model.

        Closing a topic form removes the form from the factsheet page.

        :param p_id: identity of topic form to close.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of factsheet identification information."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_view_topics(self) -> ABC_OUTLINE.ViewOutlineOpaque:
        """Return view of factsheet's topic outline."""
        raise NotImplementedError

    @abc.abstractmethod
    def present(self, p_time: int) -> None:
        """Make the page visible to user.

        Presents page to user even when page is an icon or covered by
        other windows.

        :param p_time: timestamp of event requesting presentation.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_titles(self, p_subtitle: str) -> None:
        """Set title and subtitle of page's window.

        The page's title is the factsheet name.

        :param p_subtitle: subtitle for window.
        """
        raise NotImplementedError
