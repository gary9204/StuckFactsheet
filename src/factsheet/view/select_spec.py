"""
Defines class for selecting a specification of a new topic.
"""
import gi   # type: ignore[import]
from pathlib import Path
import typing

# import factsheet.content.man_content as XMAN_CONTENT
# from factsheet.content import heading as XHEADING
# from factsheet.view import types_view as VTYPES
import factsheet.view.ui as UI

from factsheet.spec import g_specs

gi.require_version('Gtk', '3.0')
# from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class SelectSpec:
    """Provides mechanism for user to select from available templates.

    A Select Template dialog presents a user with an outline of
    available templates.  The user selects a template for specifying a
    new topic.  A user may cancel the dialog without selecting a
    template.

    :param p_parent: parent window for Select Template dialog.

    .. attribute:: NAME_FILE_QUERY_UI

       Path to user interface defintion of template query.

    .. attribute:: NO_SUMMARY

       Summary text query displays when no template is current.
    """

    NO_SUMMARY = 'Please select a <b>topic specification.</b>'

    # STUB Glade patch - begin
    #    <property name="use-header-bar">1</property>
    # STUB Glade patch - end
    # NAME_FILE_QUERY_UI = 'Oops!'  # str(UI.DIR_UI / 'query_template.ui')

    def __init__(self, p_parent: Gtk.Window,
                 p_new_view_topics: typing.Any) -> None:
        print('Enter: __init__')
        path_ui = Path(__file__).with_suffix('.ui')
        get_ui_element = UI.GetUiElementByPath(p_path_ui=path_ui)

    def _init_dialog(self) -> None:
        """Initialize the top-level visual element."""
        print('Enter: ')
        # builder = Gtk.Builder.new_from_file(self.NAME_FILE_QUERY_UI)
        # get_object = builder.get_object
        # self._dialog = get_object('ui_dialog_select_template')
        # self._dialog.set_transient_for(p_parent)
        # self._dialog.set_destroy_with_parent(True)
        #
        # _ = self._dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        # self._button_specify = self._dialog.add_button(
        #     'Specify', Gtk.ResponseType.APPLY)
        # style_specify = self._button_specify.get_style_context()
        # style_specify.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        # self._button_specify.set_sensitive(False)
        #
        # instructions = get_object('ui_info')
        # instructions.hide()
        # image_show_info = Gtk.Image.new_from_icon_name(
        #     'dialog-information-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        # button_show_info = Gtk.ToggleButton()
        # button_show_info.set_image(image_show_info)
        # _binding = button_show_info.bind_property(
        #     'active', instructions, 'visible',
        #     GO.BindingFlags.BIDIRECTIONAL)
        # button_show_info.show()
        #
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
        #
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
        #
        # self._summary_current = get_object('ui_summary_current')
        # self._summary_current.set_markup(self.NO_SUMMARY)

    def __call__(self) -> typing.Optional[Gtk.TreeIter]:
        """Presents Select Template dialog and return template user
        selects or None.

        Return none when user cancels dialog.
        """
        print('Enter: __call__')
        item = None
        # response = self._dialog.run()
        # self._dialog.hide()
        # item = None
        # if response == Gtk.ResponseType.APPLY:
        #     model, index = self._cursor.get_selected()
        #     item = AOUTLINE.get_item_gtk(model, index)
        #     self._cursor.unselect_all()
        return item

    def on_changed_cursor(self, px_cursor: Gtk.TreeSelection) -> None:
        """Changes summary text and Specify button to match current
        template.

        :param px_cursor: identifies now-current template.
        """
        print('Enter: on_changed_cursor')
        # model, index = px_cursor.get_selected()
        # if index is None:
        #     self._on_changed_cursor_invalid()
        #     return
        #
        # item = AOUTLINE.get_item_gtk(model, index)
        # if item is None:
        #     self._on_changed_cursor_invalid()
        #     return
        #
        # self._summary_current.set_markup(item.summary)
        # is_template = not isinstance(item, XHEADING.Heading)
        # self._button_specify.set_sensitive(is_template)

    def _on_changed_cursor_invalid(self) -> None:
        """Changes summary text and Specify button if there is no template.

        This is a helper method to consistently handle multiple cases.
        """
        print('Enter: _on_changed_cursor_invalid')
        # self._summary_current.set_markup(self.NO_SUMMARY)
        # self._button_specify.set_sensitive(False)

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
