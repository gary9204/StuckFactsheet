"""
Defines class for selecting a specification of a new topic.

.. data:: FactoryDisplaySummary

    Factory class for display of specification summary.

.. data:: ModelSummary

    Type for model of specification summary.

.. data:: ViewOutlineSpec

    Type for view of specification outline.
"""
import enum
import gi   # type: ignore[import]
import logging
from pathlib import Path
import typing

import factsheet.bridge_ui as BUI
import factsheet.spec as SPECS
import factsheet.spec.base_s as SBASE
import factsheet.view.ui as UI


gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
ModelSummary = BUI.ModelTextStyled
ViewOutlineSpec = BUI.ViewOutline

logger = logging.getLogger('Main.VSELECT_SPEC')


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


class SelectSpec:
    """Provides the means to select the specification for a new topic.

    Select Specification dialog allows a user to select the
    specification for a new topic from an outline of available
    specications.  A user may cancel the dialog without selecting a
    specification.

    .. attribute:: NO_SUMMARY

       Summary text displayed when no specification is selected.
    """

    NO_SUMMARY = 'Please choose a specification for a new topic.'

    # STUB Glade patch - begin
    #    <property name="use-header-bar">1</property>
    # STUB Glade patch - end

    def __call__(self) -> typing.Optional[SBASE.Base]:
        """Return spec user chooses from Select Specification dialog.

        Return None when user cancels without selecting a specification..
        """
        response = self._dialog.run()
        self._dialog.hide()
        _model, line = self._ui_selection.get_selected()
        spec = None
        if response == Gtk.ResponseType.APPLY:
            spec = self._specs.get_item(line)
        self._ui_selection.unselect_all()
        return spec

    def __init__(self, p_parent: Gtk.Window) -> None:
        """Initialize Select Specification dialog with its fields.

        :param p_parent: parent window for Select Specification dialog.
        """
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_element = UI.GetUiElementByPath(p_path_ui=path_ui)
        self._specs = SPECS.g_specs
        self._init_dialog(p_parent, get_ui_element)
        self._init_outline_specs(get_ui_element)
        self._init_summary(get_ui_element)
        self._init_search(get_ui_element)

    def _init_dialog(self, p_parent: Gtk.Window, p_get_ui_element:
                     UI.GetUiElement) -> None:
        """Initialize the top-level visual element.

        :param p_parent: parent window for Select Specification dialog.
        :param p_get_ui_element: gets visual element from UI description.
        """
        self._dialog = p_get_ui_element('ui_select_spec')
        self._dialog.set_transient_for(p_parent)
        self._dialog.set_destroy_with_parent(True)
        _ = self._dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self._button_select = self._dialog.add_button(
            'Select', Gtk.ResponseType.APPLY)
        style_specify = self._button_select.get_style_context()
        style_specify.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self._button_select.set_sensitive(False)

    def _init_outline_specs(self, p_get_ui_element: UI.GetUiElement):
        """Initialize specifications outline.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._ui_outline_specs = ViewOutlineSpec()
        self._ui_outline_specs.set_model(self._specs.ui_model)
        self._ui_outline_specs.show()
        site_specs = p_get_ui_element('ui_site_outline_specs')
        site_specs.add(self._ui_outline_specs)

        self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
        self._ui_outline_specs.append_column(self._column_name)
        self._column_title = (
            UI.new_column_stock('Title', self._markup_cell_title))
        self._ui_outline_specs.append_column(self._column_title)
        self._ui_selection = self._ui_outline_specs.get_selection()
        self._ui_selection.connect('changed', self.on_changed_selection)

        # # self._outline = UI.FACTORY_SHEET.new_view_outline_templates()
        # self._outline = VTYPES.ViewOutlineTemplates()
        # self._outline.scope_search = ~ASHEET.FieldsTemplate.VOID
        # templates = XMAN_CONTENT.new_templates(p_new_view_topics)
        # templates.attach_view(self._outline)
        # view = self._outline.gtk_view
        # view.show_all()
        # context_outline = get_object('ui_context_outline_templates')
        # context_outline.add(view)
        # context_outline.show_all()
        # self._cursor = view.get_selection()
        # _ = self._cursor.connect('changed', self.on_changed_cursor)
        #
        # search_entry = get_object('ui_search_entry')
        # view.set_search_entry(search_entry)

    def _init_summary(self, p_get_ui_element: UI.GetUiElement) -> None:
        """Initialize display for summary of chosen specification.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._summary = ModelSummary(p_text=SelectSpec.NO_SUMMARY)
        factory_display = FactoryDisplaySummary(self._summary)
        display_summary = factory_display()
        display_summary.show()
        display_summary.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        site_summary = p_get_ui_element('ui_site_summary')
        site_summary.add(display_summary)

    def _init_search(self, p_get_ui_element: UI.GetUiElement) -> None:
        """Initialize search bar and buttons.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._scope_search = FieldsId.NAME
        search_bar = p_get_ui_element('ui_search')
        button_find = Gtk.ToggleButton(label='Find')
        _binding = button_find.bind_property(
            'active', search_bar, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL)
        button_find.show()

        header_bar = p_get_ui_element('ui_header')
        header_bar.pack_start(button_find)

        button_in_name = p_get_ui_element('ui_search_in_name')
        _ = button_in_name.connect(
            'toggled', self.on_changed_search_scope, FieldsId.NAME)
        button_in_summary = p_get_ui_element('ui_search_in_summary')
        _ = button_in_summary.connect(
            'toggled', self.on_changed_search_scope, FieldsId.SUMMARY)
        button_in_title = p_get_ui_element('ui_search_in_title')
        _ = button_in_title.connect(
            'toggled', self.on_changed_search_scope, FieldsId.TITLE)

        self._ui_outline_specs.set_enable_search(True)
        C_FIRST = 0
        self._ui_outline_specs.set_search_column(C_FIRST)
        entry_search = p_get_ui_element('ui_search_entry')
        self._ui_outline_specs.set_search_entry(entry_search)
        self._ui_outline_specs.set_search_equal_func(
            self._match_spec_ne, None)

    def _markup_cell_name(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            _ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for name cell in the specs outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param _model: contains cell content (unused).
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        spec = self._specs.get_item(p_line)
        name = 'Missing'
        if spec is not None:
            name = spec.name.text
        p_render.set_property('markup', name)

    def _markup_cell_title(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            _ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for title cell in the specs outline view.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param _model: contains cell content (unused).
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        spec = self._specs.get_item(p_line)
        title = 'Missing'
        if spec is not None:
            title = spec.title.text
        p_render.set_property('markup', title)

    def _match_spec_ne(
            self, _model: Gtk.TreeModel, _n_column: int, p_match_key: str,
            p_line: BUI.LineOutline, _extra: None):
        """Return False when given key is found with scope of search.

        Implements `Gtk.TreeViewSearchEqualFunc`_. Search scope can
        include any combination of spec name, summary, or title.

        :param _model: storage for spec outline visual element (unused).
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

        spec = self._specs.get_item(p_line)
        if spec is None:
            logger.warning('Spec outline contains None for spec ({}.{})'
                           ''.format(self.__class__.__name__,
                                     self._match_spec_ne.__name__))
            return True

        if (self._scope_search & FieldsId.NAME):
            if p_match_key in spec.name.text:
                return False

        if (self._scope_search & FieldsId.SUMMARY):
            if p_match_key in spec.summary.text:
                return False

        if (self._scope_search & FieldsId.TITLE):
            if p_match_key in spec.title.text:
                return False

        path = self._specs.ui_model.get_path(p_line)
        _ = self._ui_outline_specs.expand_row(path, False)
        return True

    def on_changed_selection(self, _selection: Gtk.TreeSelection) -> None:
        """Changes summary text and Select button to match chosen spec.

        :param _selection: identifies chosen spec (unused).
        """
        _model, line = self._ui_selection.get_selected()
        if line is None:
            self._set_no_spec()
            return

        spec = self._specs.get_item(line)
        if spec is None:
            self._set_no_spec()
            return

        self._summary.text = spec.summary.text
        self._button_select.set_sensitive(True)

    def _set_no_spec(self) -> None:
        """Set summary and Select button if no spec chosen."""
        self._summary.text = self.NO_SUMMARY
        self._button_select.set_sensitive(False)

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
