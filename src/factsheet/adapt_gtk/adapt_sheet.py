"""
Defines GTK-based classes implementing abstract factsheet component
classes.

See :mod:`.abc_sheet`.

.. _`Gtk.TreeIter`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeIter.html

.. data:: N_COLUMN_TEMPLATE

    Identifies column containing tamplates.

.. data:: N_COLUMN_TOPIC

    Identifies column containing tamplates.
"""
import enum
import gi   # type: ignore[import]
import typing

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.abc_types import abc_topic as ABC_TOPIC
from factsheet.adapt_gtk import adapt_outline as AOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

N_COLUMN_TEMPLATE = AOUTLINE.N_COLUMN_ITEM
N_COLUMN_TOPIC = AOUTLINE.N_COLUMN_ITEM


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


class AdaptTreeViewTemplate(
        AOUTLINE.AdaptTreeView[ABC_SHEET.AbstractTemplate]):
    """Specializes :class:`.AdaptTreeView` with name and title columns
    for :class:`.AbstractTemplate` items.
    """
    def __init__(self):
        """Initialize view for template outline."""
        self._view = Gtk.TreeView()
        self._view.set_search_equal_func(self._test_field_ne, None)
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
        template = px_store[px_index][N_COLUMN_TEMPLATE]
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
        self._view.expand_row(path, False)
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
        template = px_store[px_index][N_COLUMN_TEMPLATE]
        pm_renderer.set_property('markup', template.title)

    def set_model(self, px_outline:
                  AOUTLINE.AdaptTreeStore[ABC_SHEET.AbstractTemplate]):
        """Associate given model with view.

        Sets up columns and renderers for name and title of template
        items.
        """
        super().set_model(px_outline)
        self._view.set_search_column(N_COLUMN_TEMPLATE)
        self._view.set_enable_search(True)

        name = Gtk.TreeViewColumn(title='Name')
        self._view.append_column(name)
        name.set_clickable(True)
        name.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_name = Gtk.CellRendererText()
        name.set_cell_data_func(render_name, self._name_cell_data, None)
        name.pack_start(render_name, expand=False)

        title = Gtk.TreeViewColumn(title='Title')
        self._view.append_column(title)
        title.set_clickable(True)
        title.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_title = Gtk.CellRendererText()
        title.set_cell_data_func(render_title, self._title_cell_data, None)
        title.pack_start(render_title, expand=False)

        pad = Gtk.TreeViewColumn(title=' ')
        pad.set_expand(True)
        self._view.append_column(pad)

    @property
    def view(self) -> Gtk.TreeView:
        """Returns underlying `Gtk.TreeIter`_."""
        return self._view


class AdaptTreeViewTopic(
        AOUTLINE.AdaptTreeView[ABC_TOPIC.AbstractTopic]):
    """Specializes :class:`.AdaptTreeView` with name and title columns
    for :class:`.AbstractTopic` items.
    """

    def __init__(self):
        """Initialize view for topic outline."""
        self._view = Gtk.TreeView()
        self._view.set_search_equal_func(self._test_field_ne, None)
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
        topic = px_store[px_index][N_COLUMN_TOPIC]
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
        _ = self._view.expand_row(path, False)
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
        topic = px_store[px_index][N_COLUMN_TOPIC]
        pm_renderer.set_property('markup', topic.title)

    def set_model(self, px_outline:
                  AOUTLINE.AdaptTreeStore[ABC_TOPIC.AbstractTopic]):
        """Associate given model with view.

        Sets up columns and renderers for name and title of topic items.
        """
        super().set_model(px_outline)
        self._view.set_search_column(N_COLUMN_TOPIC)
        self._view.set_enable_search(True)

        name = Gtk.TreeViewColumn(title='Name')
        self._view.append_column(name)
        name.set_clickable(True)
        name.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_name = Gtk.CellRendererText()
        name.set_cell_data_func(render_name, self._name_cell_data, None)
        name.pack_start(render_name, expand=False)

        title = Gtk.TreeViewColumn(title='Title')
        self._view.append_column(title)
        title.set_clickable(True)
        title.set_resizable(True)
        _ = name.get_button().get_preferred_size()
        render_title = Gtk.CellRendererText()
        title.set_cell_data_func(render_title, self._title_cell_data, None)
        title.pack_start(render_title, expand=False)

        pad = Gtk.TreeViewColumn(title=' ')
        self._view.append_column(pad)
        pad.set_expand(True)

    @property
    def view(self) -> Gtk.TreeView:
        """Returns underlying `Gtk.TreeIter`_."""
        return self._view


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
