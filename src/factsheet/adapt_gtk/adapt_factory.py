"""
Defines GTK-based classes that implement abstract factories in
:mod:`.abc_factory`.
"""
import typing

from factsheet.abc_types import abc_factory as ABC_FACTORY
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET


class FactoryInfoId(ABC_FACTORY.FactoryInfoId):
    """Implements GTK-based factory for abstract factory
    :class:`.abc_factory.FactoryInfoId`."""

    def new_model_name(self, p_text: str = '') -> AINFOID.AdaptEntryBuffer:
        """Return new instance of Gtk-based :mod:`~factsheet.model` name."""
        return AINFOID.AdaptEntryBuffer(p_text=p_text)

    def new_model_summary(self, p_text: str = '') -> AINFOID.AdaptTextBuffer:
        """Return new instance of Gtk-based :mod:`~factsheet.model`
        summary.
        """
        return AINFOID.AdaptTextBuffer(p_text=p_text)

    def new_model_title(self, p_text: str = '') -> AINFOID.AdaptEntryBuffer:
        """Return new instance of Gtk-based :mod:`~factsheet.model` title."""
        return AINFOID.AdaptEntryBuffer(p_text=p_text)

    def new_view_name(self) -> AINFOID.AdaptEntry:
        """Return new instance of GTK-based :mod:`~factsheet.view` name."""
        return AINFOID.AdaptEntry()

    def new_view_summary(self) -> AINFOID.AdaptTextView:
        """Return new instance of GTK-based :mod:`~factsheet.view`
        summary.
        """
        return AINFOID.AdaptTextView()

    def new_view_title(self) -> AINFOID.AdaptEntry:
        """Return new instance of GTK-based :mod:`~factsheet.view` title.."""
        return AINFOID.AdaptEntry()


class FactorySheet(ABC_FACTORY.FactorySheet):
    """Implements GTK-based factory for abstract factory
    :class:`.abc_factory.FactorySheet`."""

    def get_type_index(self) -> typing.Type[AOUTLINE.AdaptIndex]:
        """Returns type for index of an item within an outline."""
        return AOUTLINE.AdaptIndex

    def new_model_outline_templates(self) -> ASHEET.AdaptTreeStoreTemplate:
        """Return new instance of Gtk-based template outline"""
        return ASHEET.AdaptTreeStoreTemplate()

    def new_model_outline_topics(self) -> ASHEET.AdaptTreeStoreTopic:
        """Return new instance of Gtk-based topic outline"""
        return ASHEET.AdaptTreeStoreTopic()

    def new_view_outline_templates(self) -> ASHEET.AdaptTreeViewTemplate:
        """Return new instance of Gtk-based template view outline.
        """
        return ASHEET.AdaptTreeViewTemplate()

    def new_view_outline_topics(self) -> ASHEET.AdaptTreeViewTopic:
        """Return new instance of Gtk-based topic view outline.
        """
        return ASHEET.AdaptTreeViewTopic()
