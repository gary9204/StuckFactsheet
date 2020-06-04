"""
Defines class for selecting a template.
"""
import gi   # type: ignore[import]
# from pathlib import Path
import typing

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
# STUB imports - begin
from factsheet.content import BUILTIN
from factsheet.content.section import section_spec as XSPEC
# from factsheet.content.section import section_topic as TOPIC
# STUB imports - end
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


# # STUB content - begin
# PATH_ASSIST = str(Path(TEMPLATE.__file__).parent / 'section_spec.ui')
# MODEL_TOPIC = TOPIC.Topic
# BUILTIN = Gtk.TreeStore(GO.TYPE_PYOBJECT)
# item = TEMPLATE.Section(
#     p_name='name_0xx', p_title='title_0xx', p_summary='Stub summary_0xx',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# i_0xx = BUILTIN.append(None, [item])
# item = TEMPLATE.Section(
#     p_name='name_00x', p_title='title_00x', p_summary='Stub summary_00x',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# i_00x = BUILTIN.append(
#     i_0xx, [item])
# item = TEMPLATE.Section(
#     p_name='name_000', p_title='title_000', p_summary='Stub summary_000',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# _i_000 = BUILTIN.append(i_00x, [item])
# item = TEMPLATE.Section(
#     p_name='name_01x', p_title='title_01x', p_summary='Stub summary_01x',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# i_0xx = BUILTIN.append(i_0xx, [item])
# item = TEMPLATE.Section(
#     p_name='name_1xx', p_title='title_1xx', p_summary='Stub summary_1xx',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# i_1xx = BUILTIN.append(None, [item])
# item = TEMPLATE.Section(
#     p_name='name_10x', p_title='title_10x', p_summary='Stub summary_10x',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# _i_10x = BUILTIN.append(i_1xx, [item])
# item = TEMPLATE.Section(
#     p_name='name_11x', p_title='title_11x', p_summary='Stub summary_11x',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# i_11x = BUILTIN.append(i_1xx, [item])
# item = TEMPLATE.Section(
#     p_name='name_110', p_title='title_110', p_summary='Stub summary_110',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# _i_110 = BUILTIN.append(i_11x, [item])
# item = TEMPLATE.Section(
#     p_name='name_111', p_title='title_111', p_summary='Stub summary_111',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# _i_111 = BUILTIN.append(i_11x, [item])
# item = TEMPLATE.Section(
#     p_name='name_112', p_title='title_112', p_summary='Stub summary_112',
#     p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
# _i_112 = BUILTIN.append(i_11x, [item])
#
#
# OUTLINE = UI.FACTORY_SHEET.new_model_outline_templates()
# OUTLINE._gtk_model = BUILTIN
# # STUB content - end


class QueryTemplate:
    """Provides mechanism for user to select from available templates.

    A Select Template dialog presents a user with an outline of
    available templates.  The user selects a template for specifying a
    new topic.  A user may cancel the dialog without selecting a
    template.

    :param px_parent: parent window for Select Template dialog.

    .. attribute:: NAME_FILE_QUERY_UI

       Path to user interface defintion of template query.

    .. attribute:: NO_SUMMARY

       Summary text query displays when no template is current.
    """

    NO_SUMMARY = 'Please select a <b>template.</b>'

    # STUB Glade patch - begin
    #    <property name="use-header-bar">1</property>
    # STUB Glade patch - end
    NAME_FILE_QUERY_UI = str(UI.DIR_UI / 'query_template.ui')

    def __init__(self, px_parent: Gtk.Window) -> None:
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_QUERY_UI)
        get_object = builder.get_object
        self._dialog = get_object('ui_dialog_select_template')
        self._dialog.set_transient_for(px_parent)
        self._dialog.set_destroy_with_parent(True)

        _ = self._dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self._button_specify = self._dialog.add_button(
            'Specify', Gtk.ResponseType.APPLY)
        style_specify = self._button_specify.get_style_context()
        style_specify.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self._button_specify.set_sensitive(False)

        instructions = get_object('ui_info')
        instructions.hide()
        image_show_info = Gtk.Image.new_from_icon_name(
            'dialog-information-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        button_show_info = Gtk.ToggleButton()
        button_show_info.set_image(image_show_info)
        _binding = button_show_info.bind_property(
            'active', instructions, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)
        button_show_info.show()

        search_bar = get_object('ui_search_bar')
        image_show_search = Gtk.Image.new_from_icon_name(
            'edit-find-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        button_show_search = Gtk.ToggleButton()
        button_show_search.set_image(image_show_search)
        _binding = button_show_search.bind_property(
            'active', search_bar, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL)
        button_show_search.show()

        header_bar = get_object('ui_header_bar')
        header_bar.pack_end(button_show_search)
        header_bar.pack_end(button_show_info)

        button_by_name = get_object('ui_search_by_name')
        _ = button_by_name.connect('toggled', self.on_toggle_search_field,
                                   ASHEET.FieldsTemplate.NAME)
        button_by_title = get_object('ui_search_by_title')
        _ = button_by_title.connect('toggled', self.on_toggle_search_field,
                                    ASHEET.FieldsTemplate.TITLE)

        self._outline = UI.FACTORY_SHEET.new_view_outline_templates()
        self._outline.scope_search = ~ASHEET.FieldsTemplate.VOID
        # STUB test content - begin
        BUILTIN.attach_view(self._outline)
#         OUTLINE.attach_view(self._outline)
        # STUB test content - end
        view = self._outline.gtk_view
        view.show_all()
        context_outline = get_object('ui_context_outline_templates')
        context_outline.add(view)
        context_outline.show_all()
        self._cursor = view.get_selection()
        _ = self._cursor.connect('changed', self.on_changed_cursor)

        search_entry = get_object('ui_search_entry')
        view.set_search_entry(search_entry)

        self._summary_current = get_object('ui_summary_current')
        self._summary_current.set_markup(self.NO_SUMMARY)

    def __call__(self) -> typing.Optional[Gtk.TreeIter]:
        """Presents Select Template dialog and returns template user
        selects or None.

        Returns none when user cancels dialog.
        """
        response = self._dialog.run()
        self._dialog.hide()
        item = None
        if response == Gtk.ResponseType.APPLY:
            model, index = self._cursor.get_selected()
            item = AOUTLINE.get_item_gtk(model, index)
            self._cursor.unselect_all()
        return item

    def on_changed_cursor(self, px_cursor: Gtk.TreeSelection) -> None:
        """Changes summary text and Specify button to match current
        template.

        :param px_cursor: identifies now-current template.
        """
        model, index = px_cursor.get_selected()
        if index is None:
            self._on_changed_cursor_invalid()
            return

        item = AOUTLINE.get_item_gtk(model, index)
        if item is None:
            self._on_changed_cursor_invalid()
            return

        self._summary_current.set_markup(item.summary)
        # Stub - begin: handling headings
        is_template = isinstance(item, XSPEC.Section)
        self._button_specify.set_sensitive(is_template)
        # Stub - end: handling headings

    def _on_changed_cursor_invalid(self) -> None:
        """Changes summary text and Specify button if there is no template.

        This is a helper method to consistently handle multiple cases.
        """
        self._summary_current.set_markup(self.NO_SUMMARY)
        self._button_specify.set_sensitive(False)

    def on_toggle_search_field(self, px_button: Gtk.ToggleButton, p_field:
                               ASHEET.FieldsTemplate) -> None:
        """Sets search to match active field button.

        :param px_button: button user toggled.
        :param p_field: search field of toggled button.
        """
        if px_button.get_active():
            self._outline.scope_search |= p_field
        else:
            self._outline.scope_search &= ~p_field
