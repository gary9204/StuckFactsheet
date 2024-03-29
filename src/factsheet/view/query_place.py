"""
Defines class for selecting a place in a topic outline for a new topic.
"""
import collections as COL
import enum
import gi   # type: ignore[import]
import typing

from factsheet.view import types_view as VTYPES
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


Placement = COL.namedtuple('Placement', ['anchor', 'order'])
"""Specifies placement of an item into an outline relative to an item
already in the outline.

.. attribute:: anchor

    Index of reference item already in the outline.

.. attribute:: order

    Order of item relative to anchor.  See :class:`.Order`.
"""


class Order(enum.Enum):
    """Enumeration that identifies order relative to an outline item.

    .. attribute:: AFTER

        Position immediately after an outline item.

    .. attribute:: BEFORE

        Position immediately before an outline item.

    .. attribute:: CHILD

        Position as outline item child after any other children.
    """
    AFTER = enum.auto()
    BEFORE = enum.auto()
    CHILD = enum.auto()


class QueryPlace:
    """Provides mechanism for user to select a place for a new topic in
    a topic outline.

    A Place New Topic dialog presents a user with an outline of existing
    topics.  The user selects a reference topic and relative order for
    the new topic.  See :class:`.Placement`. A user may cancel the
    dialog without selecting a placement.

    :param p_parent: parent window for Place New Topic dialog.
    :param p_view_topics: existing view of topics outline.

    .. attribute:: NAME_FILE_QUERY_UI

       Path to user interface defintion of Place New Topic dialog.

    .. attribute:: NO_SUMMARY

       Summary text query displays when no topic is current.
    """

    NO_SUMMARY = 'Please select a topic.'

    # STUB Glade patch - begin
    #    <property name="use-header-bar">1</property>
    # STUB Glade patch - end
    NAME_FILE_QUERY_UI = str(UI.DIR_UI / 'query_place.ui')

    def __init__(self, p_parent: Gtk.Window, p_view_topics:
                 VTYPES.ViewOutlineTopics) -> None:
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_QUERY_UI)
        get_object = builder.get_object
        self._dialog = get_object('ui_dialog_query_place')
        self._dialog.set_transient_for(p_parent)
        self._dialog.set_destroy_with_parent(True)

        header_bar = get_object('ui_header_bar')
        _ = self._dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)

        self._button_place = self._dialog.add_button(
            'Place', Gtk.ResponseType.APPLY)
        style_place = self._button_place.get_style_context()
        style_place.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self._button_place.set_sensitive(False)

        search_bar = get_object('ui_search_bar')
        image_show_search = Gtk.Image.new_from_icon_name(
            'edit-find-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        button_show_search = Gtk.ToggleButton()
        button_show_search.set_image(image_show_search)
        header_bar.pack_end(button_show_search)
        button_show_search.show()
        _binding = button_show_search.bind_property(
            'active', search_bar, 'search-mode-enabled',
            GO.BindingFlags.BIDIRECTIONAL)

        instructions = get_object('ui_info')
        instructions.hide()
        image_show_info = Gtk.Image.new_from_icon_name(
            'dialog-information-symbolic', Gtk.IconSize.SMALL_TOOLBAR)
        button_show_info = Gtk.ToggleButton()
        button_show_info.set_image(image_show_info)
        header_bar.pack_end(button_show_info)
        button_show_info.show()
        _binding = button_show_info.bind_property(
            'active', instructions, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

        button_by_name = get_object('ui_search_by_name')
        _ = button_by_name.connect(
            'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.NAME)
        button_by_title = get_object('ui_search_by_title')
        _ = button_by_title.connect(
            'toggled', self.on_toggle_search_field, ASHEET.FieldsTopic.TITLE)

        self._view_topics = p_view_topics
        self._view_topics.scope_search = ~ASHEET.FieldsTopic.VOID
        gtk_view = self._view_topics.gtk_view
        context_view_topics = get_object('ui_context_view_topics')
        context_view_topics.add(gtk_view)
        context_view_topics.show_all()
        self._cursor = gtk_view.get_selection()
        _ = self._cursor.connect('changed', self.on_changed_cursor)

        search_entry = get_object('ui_search_entry')
        gtk_view.set_search_entry(search_entry)

        self._summary_current = get_object('ui_summary_current')
        self._summary_current.set_text(self.NO_SUMMARY)

        self._order = Order.AFTER
        button_after = get_object('ui_order_after')
        _ = button_after.connect('toggled', self.on_toggle_order, Order.AFTER)
        button_before = get_object('ui_order_before')
        _ = button_before.connect('toggled', self.on_toggle_order,
                                  Order.BEFORE)
        button_child = get_object('ui_order_child')
        _ = button_child.connect('toggled', self.on_toggle_order, Order.CHILD)

    def __call__(self) -> typing.Optional[Placement]:
        """Presents Place New Topic dialog and return placement user
        selects or None.

        Return None when user cancels dialog.
        """
        response = self._dialog.run()
        self._dialog.hide()
        place = None
        if response == Gtk.ResponseType.APPLY:
            _model, index = self._cursor.get_selected()
            place = Placement(index, self._order)
            self._cursor.unselect_all()
        return place

    def on_changed_cursor(self, p_cursor: Gtk.TreeSelection) -> None:
        """Changes summary text and Place button to match current topic.

        :param p_cursor: identifies now-current topic.
        """
        model, index = p_cursor.get_selected()
        if index is None:
            self._on_changed_cursor_invalid()
            return

        item = AOUTLINE.get_item_gtk(model, index)
        if item is None:
            self._on_changed_cursor_invalid()
            return

        self._summary_current.set_text(item._infoid.summary)
        self._button_place.set_sensitive(True)

    def _on_changed_cursor_invalid(self) -> None:
        """Changes summary text and Place button if there is no topic.

        This is a helper method to consistently handle multiple cases.
        """
        self._summary_current.set_text(self.NO_SUMMARY)
        self._button_place.set_sensitive(False)

    def on_toggle_order(self, p_button: Gtk.ToggleButton,
                        p_order: Order) -> None:
        """Sets order to match active order button.

        :param p_button: button user toggled.
        :param p_order: order of toggled button.
        """
        if p_button.get_active():
            self._order = p_order

    def on_toggle_search_field(self, p_button: Gtk.ToggleButton, p_field:
                               ASHEET.FieldsTopic) -> None:
        """Sets search to match active field buttons.

        :param p_button: button user toggled.
        :param p_field: search field of toggled button.
        """
        if p_button.get_active():
            self._view_topics.scope_search |= p_field
        else:
            self._view_topics.scope_search &= ~p_field
