"""
Defines GTK-based classes implementing abstract factsheet component
classes.

See :mod:`.abc_sheet`.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html
"""
import enum
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.adapt_gtk import adapt_outline as AOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class AdaptTreeStoreTemplate(
        AOUTLINE.AdaptTreeStore[ABC_SHEET.AbstractTemplate]):
    """Specializes :class:`.AdaptTreeStore` with
    :class:`.AbstractTemplate` items.
    """

    def find_name(self, px_target: str,
                  px_i_after: AOUTLINE.AdaptIndex = None
                  ) -> AOUTLINE.AdaptIndex:
        """Return index of first template where the target value equals
        the template name, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this name.
        :param px_i_after: start search immediately after item at this
            index. Default starts search at top item in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda item: item.name)

    def find_title(self, px_target: str,
                   px_i_after: AOUTLINE.AdaptIndex = None
                   ) -> AOUTLINE.AdaptIndex:
        """Return index of first template where the target value equals
        the template title, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this title.
        :param px_i_after: start search immediately after item at this
            index. Default starts search at top item in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda item: item.title)


class AdaptTreeStoreTopic(
        AOUTLINE.AdaptTreeStore[ABC_TOPIC.AbstractTopic]):
    """Specializes :class:`.AdaptTreeStore` with
    :class:`~.outline.topic.Topic` items.
    """

    def find_name(self, px_target: str,
                  px_i_after: AOUTLINE.AdaptIndex = None
                  ) -> AOUTLINE.AdaptIndex:
        """Return index of first topic where the target value equals the
        topic name, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this name.
        :param px_i_after: start search immediately after topic at this
            index. Default starts search at top topic in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda topic: topic.name)

    def find_title(self, px_target: str,
                   px_i_after: AOUTLINE.AdaptIndex = None
                   ) -> AOUTLINE.AdaptIndex:
        """Return index of first topic where the target value equals the
        topic title, or None if no match.

        Search covers entire outline by wrapping at end if necessary.

        :param px_target: search for this title.
        :param px_i_after: start search immediately after topic at this
            index. Default starts search at top topic in outline.

        .. warning:: The current implementation does not address risk
            user modifies outline during search.
        """
        return self.find_next(
            px_target, px_i_after, lambda topic: topic.title)


class AdaptTreeViewTemplate(AOUTLINE.AdaptTreeView):
    """Specializes :class:`.AdaptTreeView` with name and title columns
    for :class:`.AbstractTemplate` items.
    """
    def __init__(self):
        """Initialize view for template outline."""
        super().__init__()
        self._gtk_view.set_search_equal_func(self._test_field_ne, None)
        self._active_field = FieldsTemplate.NAME

    def _name_cell_data(self, _column: Gtk.TreeViewColumn,
                        pm_renderer: Gtk.CellRenderer,
                        px_store: Gtk.TreeStore,
                        px_index: AOUTLINE.AdaptIndex,
                        _data: typing.Any = None) -> None:
        """Adapter to diaplay template name in a `Gtk.TreeIter`_ column.

        Formal Parameters
            _column: `Gtk.TreeIter`_ column to display name.
            pm_renderer: cell renderer to display topic name.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        template = px_store[px_index][AdaptTreeStoreTemplate.N_COLUMN_ITEM]
        pm_renderer.set_property('markup', template.name)

    def _test_field_ne(self, px_model: Gtk.TreeModel, p_n_column: int,
                       p_value: str, px_index: Gtk.TreeIter, _user_data):
        """Return True when value is not equal to the contents of the
        active search field.

        Implements `Gtk.TreeViewSearchEqualFunc`_ for name and title
        search.

        .. _`Gtk.TreeViewSearchEqualFunc`::

            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        template = px_model[px_index][p_n_column]
        if self._active_field is FieldsTemplate.NAME:
            value = template.name
        elif self._active_field is FieldsTemplate.TITLE:
            value = template.title
        else:
            return True

        if value.startswith(p_value):
            return False

        path = px_model.get_path(px_index)
        self._gtk_view.expand_row(path, False)
        return True

    def _title_cell_data(self, _column: Gtk.TreeViewColumn,
                         pm_renderer: Gtk.CellRenderer,
                         px_store: Gtk.TreeStore,
                         px_index: AOUTLINE.AdaptIndex,
                         _data: typing.Any = None) -> None:
        """Adapter to display template title in a `Gtk.TreeIter`_
        column.

        Formal Parameters
            _column: `Gtk.TreeIter`_ column to display name.
            pm_renderer: cell renderer to display topic title.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        template = px_store[px_index][AdaptTreeStoreTemplate.N_COLUMN_ITEM]
        pm_renderer.set_property('markup', template.title)


class AdaptTreeViewTopic(AOUTLINE.AdaptTreeView):
    """Specializes :class:`.AdaptTreeView` with name and title columns
    for :class:`.AbstractTopic` items.
    """

    def __init__(self):
        """Initialize view for topic outline."""
        super().__init__()
        self._gtk_view.set_search_equal_func(self._test_field_ne, None)
        self._search = FieldsTopic.VOID

    def _name_cell_data(self, _column: Gtk.TreeViewColumn,
                        pm_renderer: Gtk.CellRenderer,
                        px_store: Gtk.TreeStore,
                        px_index: AOUTLINE.AdaptIndex,
                        _data: typing.Any = None) -> None:
        """Adapter to diaplay topic name in a `Gtk.TreeIter`_ column.

        Formal Parameters
            _column: `Gtk.TreeIter`_ column to display name.
            pm_renderer: cell renderer to display topic name.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        topic = px_store[px_index][AdaptTreeStoreTopic.N_COLUMN_ITEM]
        pm_renderer.set_property('markup', topic.name)

    def _test_field_ne(self, px_model: Gtk.TreeModel, p_n_column: int,
                       p_value: str, px_index: Gtk.TreeIter, _user_data):
        """Return True when value is not equal to the contents of the
        active search field.

        Implements `Gtk.TreeViewSearchEqualFunc`_ for name and title
        search.

        .. _`Gtk.TreeViewSearchEqualFunc`::

            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        if not self._search:
            return True

        topic = px_model[px_index][p_n_column]
        if self._search & FieldsTopic.NAME:
            if topic.name.startswith(p_value):
                return False

        if self._search & FieldsTopic.TITLE:
            if topic.title.startswith(p_value):
                return False

        path = px_model.get_path(px_index)
        _ = self._gtk_view.expand_row(path, False)
        return True

    def _title_cell_data(self, _column: Gtk.TreeViewColumn,
                         pm_renderer: Gtk.CellRenderer,
                         px_store: Gtk.TreeStore,
                         px_index: AOUTLINE.AdaptIndex,
                         _data: typing.Any = None) -> None:
        """Adapter to display topic title in a `Gtk.TreeIter`_ column.

        Formal Parameters
            _column: `Gtk.TreeIter`_ column to display name.
            pm_renderer: cell renderer to display topic title.
            px_store: store containing the topic.
            px_index: store index of topic.
            _data: (optional) user data for cell function.
        """
        topic = px_store[px_index][AdaptTreeStoreTopic.N_COLUMN_ITEM]
        pm_renderer.set_property('markup', topic.title)


class FieldsTemplate(enum.Flag):
    """Identifies template fields.

    .. data:: NAME

       Denotes template name field.

    .. data:: TITLE

       Denotes template title field.

    .. data:: VOID

       Denotes no field.
    """
    VOID = 0
    NAME = enum.auto()
    TITLE = enum.auto()


class FieldsTopic(enum.Flag):
    """Identifies topic fields, which may be combined.

    .. data:: NAME

       Denotes topic name field.

    .. data:: TITLE

       Denotes topic title field.

    .. data:: VOID

       Denotes no field.
    """
    VOID = 0
    NAME = enum.auto()
    TITLE = enum.auto()
