"""
Defines class for selecting a specification of a new topic.

.. data:: FactoryDisplaySummary

    TBD


.. data:: ModelSummary

    TBD

.. data:: ViewOutlineSpec

    TBD
"""
import gi   # type: ignore[import]
from pathlib import Path
import typing

# import factsheet.content.man_content as XMAN_CONTENT
# from factsheet.content import heading as XHEADING
# from factsheet.view import types_view as VTYPES
import factsheet.bridge_ui as BUI
import factsheet.spec as SPECS
import factsheet.spec.base_s as SBASE
import factsheet.view.ui as UI


gi.require_version('Gtk', '3.0')
# from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
ModelSummary = BUI.ModelTextStyled
ViewOutlineSpec = BUI.ViewOutline


class SelectSpec:
    """Provides the means to select the specification for a new topic.

    Select Specification dialog allows a user to select the
    specification for a new topic from an outline of available
    speciications.  A user may cancel the dialog without selecting a
    specification.

    .. attribute:: NO_SUMMARY

       Summary text displayed when no specification is selected.
    """

    NO_SUMMARY = 'Please choose a specification for a new topic.'

    # STUB Glade patch - begin
    #    <property name="use-header-bar">1</property>
    # STUB Glade patch - end

    def __init__(self, p_parent: Gtk.Window) -> None:
        """Initialize

        :param p_parent: parent window for Select Specification dialog.
        """
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_element = UI.GetUiElementByPath(p_path_ui=path_ui)
        self._specs = SPECS.g_specs
        self._init_dialog(p_parent, get_ui_element)
        self._init_outline_specs(get_ui_element)
        self._init_summary(get_ui_element)

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

    # def _init_instructions(self) -> None:
    #     """Initialize instructions for specification selection."""
    #     print('Enter: _init_instructions')
    #     # instructions = get_object('ui_info')
    #     # instructions.hide()
    #     # image_show_info = Gtk.Image.new_from_icon_name(
    #     #     'dialog-information-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
    #     # button_show_info = Gtk.ToggleButton()
    #     # button_show_info.set_image(image_show_info)
    #     # _binding = button_show_info.bind_property(
    #     #     'active', instructions, 'visible',
    #     #     GO.BindingFlags.BIDIRECTIONAL)
    #     # button_show_info.show()

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

    def _init_summary(self, p_get_ui_element: UI.GetUiElement):
        """Initialize display for summary of chosen specification.

        :param p_get_ui_element: gets visual element from UI description.
        """
        self._summary = ModelSummary(p_text=SelectSpec.NO_SUMMARY)
        factory_display = FactoryDisplaySummary(self._summary)
        display_summary = factory_display()
        # display_summary = DisplaySummary(buffer=self._summary.ui_model)
        display_summary.show()
        display_summary.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        site_summary = p_get_ui_element('ui_site_summary')
        site_summary.add(display_summary)

    def _init_search(self):
        """Initialize search bar and buttons."""
        print('Enter: _init_search')
        # search_bar = get_object('ui_search_bar')
        # image_show_search = Gtk.Image.new_from_icon_name(
        #     'edit-find-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        # button_show_search = Gtk.ToggleButton()
        # button_show_search.set_image(image_show_search)
        # _binding = button_show_search.bind_property(
        #     'active', search_bar, 'search-mode-enabled',
        #     GO.BindingFlags.BIDIRECTIONAL)
        # button_show_search.show()
        #
        # header_bar = get_object('ui_header_bar')
        # header_bar.pack_end(button_show_search)
        # header_bar.pack_end(button_show_info)
        #
        # button_by_name = get_object('ui_search_by_name')
        # _ = button_by_name.connect('toggled', self.on_toggle_search_field,
        #                            ASHEET.FieldsTemplate.NAME)
        # button_by_title = get_object('ui_search_by_title')
        # _ = button_by_title.connect('toggled', self.on_toggle_search_field,
        #                             ASHEET.FieldsTemplate.TITLE)

    def __call__(self) -> typing.Optional[SBASE.Base]:
        """Return spec user chooses from Select Specification dialog.

        Return None when user cancels without selecting a specification..
        """
        print('Enter: __call__')
        # Issue #249 stub
        spec = SBASE.Base(p_name='Cheese Shop',
                          p_summary='Please select any cheese in the shop!',
                          p_title='Cheese Specification')
        response = self._dialog.run()
        self._dialog.hide()
        # item = None
        # if response == Gtk.ResponseType.APPLY:
        #     model, index = self._cursor.get_selected()
        #     item = AOUTLINE.get_item_gtk(model, index)
        #     self._cursor.unselect_all()
        return spec

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

    def on_changed_selection(self, _selection: Gtk.TreeSelection) -> None:
        """Changes summary text and Specify button to match chosen spec.

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
        """Set summary and Specify button if no spec chosen."""
        self._summary.text = self.NO_SUMMARY
        self._button_select.set_sensitive(False)

    def on_toggle_search_field(self, px_button: Gtk.ToggleButton, p_field:
                               typing.Any) -> None:
        """Sets search to match active field button.

        :param px_button: button user toggled.
        :param p_field: search field of toggled button.
        """
        print('Enter: on_toggle_search_field')
        # if px_button.get_active():
        #     self._outline.scope_search |= p_field
        # else:
        #     self._outline.scope_search &= ~p_field
