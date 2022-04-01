"""
Defines class for selecting a item from an outline.

.. data:: ButtonFind

    Type for button to show and hide search of item outline.

.. data:: FactoryDisplaySummary

    Factory class for display of item summary.

.. data:: ModelSummary

    Type for model of item summary.

.. data:: UiChooserItem

    Type for visual element of :class:`ChooserItem`.

.. data:: ViewOutlineItem

    Type for view of outline of items.
"""
import enum
import gi   # type: ignore[import]
import logging
from pathlib import Path
import typing

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE
import factsheet.view.ui as UI


gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


ButtonFind = typing.Union[Gtk.ToggleButton]
FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
ModelOutline = BUI.ModelOutlineMulti[MIDCORE.IdCore]
ModelSummary = BUI.ModelTextStyled
UiChooserItem = typing.Union[Gtk.Paned]
ViewOutlineItem = BUI.ViewOutline

logger = logging.getLogger('Main.VSELECT_ITEM')


class FieldsId(enum.Flag):
    """Identifies search fields for :class:`.IdCore`.

    A search may combine fields using logical operators.

    .. data:: NAME

       Denotes name field.

    .. data:: TITLE

       Denotes title field.

    .. data:: SUMMARY

       Denotes summary field.

    .. data:: VOID

       Denotes no field.
    """
    VOID = 0
    NAME = enum.auto()
    SUMMARY = enum.auto()
    TITLE = enum.auto()


class ChooserItem:
    """Provides means to choose an item from an outline.

    Visual element displays outline of items (such as specifications,
    topics, or facts).  The element identifies the element currently
    chosen along with its summary.  A visual element may register a
    button with :class:`ChooserItem` to show and hide a field to search
    the outline.

    .. attribute:: NO_SUMMARY

       Summary text displayed when no item is selected.
    """

    NO_SUMMARY = 'Please choose an item in the outline above.'

    def __init__(self, p_view_outline: ViewOutlineItem) -> None:
        """Initialize Select Specification dialog with its fields.

        :param p_view_outline: parent window for Select Specification dialog.
        """
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_element = UI.GetUiElementByPath(p_path_ui=path_ui)
        self._ui_chooser = get_ui_element('ui_choose_item')
        self._ui_view_outline = p_view_outline
        self._init_view_outline(get_ui_element)
        self._init_summary(get_ui_element)
        self._init_search(get_ui_element)
        self._ui_chooser.show_all()

    def _init_search(self, p_get_ui_element: UI.GetUiElement) -> None:
        """Initialize search bar and buttons.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._scope_search = FieldsId.NAME
        self._search_bar = p_get_ui_element('ui_search')

        button_in_name = p_get_ui_element('ui_search_in_name')
        _ = button_in_name.connect(
            'toggled', self.on_changed_search_scope, FieldsId.NAME)
        button_in_summary = p_get_ui_element('ui_search_in_summary')
        _ = button_in_summary.connect(
            'toggled', self.on_changed_search_scope, FieldsId.SUMMARY)
        button_in_title = p_get_ui_element('ui_search_in_title')
        _ = button_in_title.connect(
            'toggled', self.on_changed_search_scope, FieldsId.TITLE)

        # self._ui_view_outline.set_enable_search(True)
        C_FIRST = 0
        self._ui_view_outline.set_search_column(C_FIRST)
        entry_search = p_get_ui_element('ui_search_entry')
        self._ui_view_outline.set_search_entry(entry_search)
        EXTRA = None
        self._ui_view_outline.set_search_equal_func(
            self._match_spec_ne, EXTRA)

    def _init_summary(self, p_get_ui_element: UI.GetUiElement) -> None:
        """Initialize display for summary of chosen specification.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._summary = ModelSummary(p_text=ChooserItem.NO_SUMMARY)
        factory_display = FactoryDisplaySummary(self._summary)
        display_summary = factory_display()
        site_summary = p_get_ui_element('ui_site_summary')
        site_summary.add(display_summary)
        display_summary.show()
        display_summary.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

    def _init_view_outline(self, p_get_ui_element: UI.GetUiElement) -> None:
        """Initialize specifications outline.

        :param p_get_ui_element: gets visual element from UI description.
        """
        site_outline = p_get_ui_element('ui_site_outline')
        site_outline.add(self._ui_view_outline)

        self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
        self._ui_view_outline.append_column(self._column_name)
        self._column_title = (
            UI.new_column_stock('Title', self._markup_cell_title))
        self._ui_view_outline.append_column(self._column_title)
        self._ui_selection = self._ui_view_outline.get_selection()
        self._ui_selection.connect('changed', self.on_changed_selection)
        # self._ui_view_outline.show()

    def _markup_cell_name(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for name cell in the items outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param p_ui_model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        print('Enter: _markup_cell_name')
        item = ModelOutline.get_item_direct(p_ui_model, p_line)
        name = 'Missing'
        if item is not None:
            name = item.name.text
        p_render.set_property('markup', name)

    def _markup_cell_title(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for title cell in the items outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param _model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        item = ModelOutline.get_item_direct(p_ui_model, p_line)
        title = 'Missing'
        if item is not None:
            title = item.title.text
        p_render.set_property('markup', title)

    def _match_spec_ne(
            self, p_ui_model: Gtk.TreeModel, _n_column: int, p_match_key: str,
            p_line: BUI.LineOutline, _extra: None):
        """Return False when given key is found with scope of search.

        Implements `Gtk.TreeViewSearchEqualFunc`_. Search scope can
        include any combination of spec name, summary, or title.

        :param p_ui_model: storage for spec outline visual element.
        :param _n_column: model column to match (unused).
        :param p_match_key: key to match within search field(s).
        :param p_line: line to check for key.
        :param _extra: optional extra parameter (unused)

        .. _`Gtk.TreeViewSearchEqualFunc`::
            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        if not self._scope_search:
            return True

        item = ModelOutline.get_item_direct(p_ui_model, p_line)
        if item is None:
            line_str = p_ui_model.get_string_from_iter(p_line)
            logger.warning('Outline contains None at line "{}" ({}.{})'
                           ''.format(line_str, self.__class__.__name__,
                                     self._match_spec_ne.__name__))
            return True

        if (self._scope_search & FieldsId.NAME):
            if p_match_key in item.name.text:
                return False

        if (self._scope_search & FieldsId.SUMMARY):
            if p_match_key in item.summary.text:
                return False

        if (self._scope_search & FieldsId.TITLE):
            if p_match_key in item.title.text:
                return False

        path = p_ui_model.get_path(p_line)
        _ = self._ui_view_outline.expand_row(path, False)
        return True

    def on_changed_selection(self, _selection: Gtk.TreeSelection) -> None:
        """Changes summary text and Select button to match chosen spec.

        :param _selection: identifies chosen spec (unused).
        """
        model, line = self._ui_selection.get_selected()
        if line is None:
            self._summary.text = self.NO_SUMMARY
            return

        item = ModelOutline.get_item_direct(model, line)
        if item is None:
            self._summary.text = self.NO_SUMMARY
            return

        self._summary.text = item.summary.text

    def on_changed_search_scope(
            self, p_button: Gtk.ToggleButton, p_field: FieldsId) -> None:
        """Sets search scope to match requested change.

        :param p_button: search scope button changed by user.
        :param p_field: search field corresponding to changed button.
        """
        if p_button.get_active():
            self._scope_search |= p_field
        else:
            self._scope_search &= ~p_field

    @property
    def ui_chooser(self) -> UiChooserItem:
        """Return visual element for choosing an item.
        """
        return self._ui_chooser

    def sync_to_search(self, p_button_find: ButtonFind) -> None:
        """Sync button to show and hide search of item outline.

        :param p_button: button to sync with search.
        """
        _binding = p_button_find.bind_property(
            'active', self._search_bar, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL)
