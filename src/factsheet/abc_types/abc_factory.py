"""
Defines abstract factory classes.

:doc:`../guide/devel_notes` describes the use of abstract classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_factory`` defines abstract factories for
component classes of :class:`.InfoId`.
"""
import abc
import typing

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.abc_types import abc_outline as ABC_OUTLINE


class FactoryInfoId(abc.ABC):
    """Defines abstract factory to produce identification information
    components for :class:`~.InfoId` and :class:`~.ViewInfoId`.
    """

    @abc.abstractmethod
    def new_model_name(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of name for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_model_summary(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of summary for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_model_title(
            self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
        """Return new instance of title for :class:`.InfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_name(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of name for :class:`.ViewInfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_summary(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of summary for :class:`.ViewInfoId`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_title(self) -> ABC_INFOID.AbstractTextView:
        """Return new instance of title for :class:`.ViewInfoId`.
        """
        raise NotImplementedError


class FactorySheet(abc.ABC):
    """Defines abstract factory to produce factsheet components for
    :class:`~.model.sheet.Sheet` and :class:`.PageSheet`.
    """

    @abc.abstractmethod
    def new_model_outline_templates(self) -> ABC_OUTLINE.AbstractOutline:
        """Return new instance of template outline class for
        :class:`~.model.sheet.Sheet`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view_outline_templates(self) -> ABC_OUTLINE.AbstractViewOutline:
        """Return new instance of template view outline class for
        :class:`.PageSheet`.
        """
        raise NotImplementedError
