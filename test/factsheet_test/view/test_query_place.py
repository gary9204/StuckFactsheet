"""
Unit tests for topic placement class.  See :mod:`.query_place`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.view import query_place as QPLACE
from factsheet.view import types_view as VTYPES
# from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_view_topics(new_outline_topics):
    """Pytest fixture returns view of topic outline."""
    outline = VTYPES.ViewOutlineTopics()
    topics = new_outline_topics()
    ui_model = topics._ui_model
    outline.gtk_view.set_model(ui_model)
    return outline


class TestQueryPlace:
    """Unit tests for :class:`.QueryPlace`."""

    def gtk_to_text(self, px_buffer: Gtk.TextBuffer) -> str:
        """Extracts buffer contents."""
        begin, end = px_buffer.get_bounds()
        INCLUDE_HIDDEN = True
        return px_buffer.get_text(begin, end, INCLUDE_HIDDEN)

    def test_attr(self):
        """Confirm class attributes are defined."""
        # Setup
        target = QPLACE.QueryPlace
        # Test
        assert isinstance(target.NO_SUMMARY, str)
        assert target.NO_SUMMARY
        assert isinstance(target.NAME_FILE_QUERY_UI, str)
        assert target.NAME_FILE_QUERY_UI

    def test_init(self, patch_view_topics):
        """Confirm initialization."""
        # Setup
        WIN = Gtk.Window()
        VIEW_TOPICS = patch_view_topics
        NAME_CANCEL = 'Cancel'
        NAME_PLACE = 'Place'
        NAME_SEARCH = 'edit-find-symbolic'
        NAME_INFO = 'dialog-information-symbolic'
        # Test
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=VIEW_TOPICS)
        assert isinstance(target._dialog, Gtk.Dialog)
        dialog = target._dialog
        assert dialog.get_transient_for() is WIN
        assert dialog.get_destroy_with_parent()

        header_bar = dialog.get_header_bar()
        button_cancel, button_place, button_search, button_info = (
            tuple(header_bar.get_children()))

        assert isinstance(button_cancel, Gtk.Button)
        assert NAME_CANCEL == button_cancel.get_label()

        assert isinstance(target._button_place, Gtk.Button)
        assert NAME_PLACE == button_place.get_label()
        assert target._button_place is button_place
        style = target._button_place.get_style_context()
        assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        assert not target._button_place.get_sensitive()

        assert isinstance(button_search, Gtk.ToggleButton)
        assert button_search.get_visible()
        image = button_search.get_image()
        name_image, _size_image = image.get_icon_name()
        assert NAME_SEARCH == name_image

        assert isinstance(button_info, Gtk.ToggleButton)
        assert button_info.get_visible()
        image = button_info.get_image()
        name_image, _size_image = image.get_icon_name()
        assert NAME_INFO == name_image

        assert isinstance(target._view_topics, ASHEET.AdaptTreeViewTopic)
        assert target._view_topics.scope_search is ~ASHEET.FieldsTopic.VOID
        gtk_view = target._view_topics.gtk_view
        assert gtk_view is VIEW_TOPICS.gtk_view
        assert gtk_view.get_parent() is not None
        assert gtk_view.get_search_entry() is not None
        assert gtk_view.get_visible()

        assert target._cursor is gtk_view.get_selection()

        assert isinstance(target._summary_current, Gtk.TextBuffer)
        text = self.gtk_to_text(target._summary_current)
        assert text == target.NO_SUMMARY

        assert target._order is QPLACE.Order.AFTER
        # Teardown
        del WIN

    def test_call(self, patch_dialog_run, monkeypatch, patch_view_topics):
        """| Confirm template selection.
        | Case: template selected.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._dialog.show()
        target._view_topics.gtk_view.expand_all()

        PATH_ITEM = '1:1:1'
        model = DONOR.gtk_view.get_model()
        i_item = model.get_iter_from_string(PATH_ITEM)
        target._cursor.select_iter(i_item)
        ORDER = QPLACE.Order.BEFORE
        target._order = ORDER
        # Test
        place_anchor, place_order = target()
        place_path = model.get_string_from_iter(place_anchor)
        assert PATH_ITEM == place_path
        assert ORDER == place_order
        assert patch_dialog.called
        assert not target._dialog.get_visible()
        text = self.gtk_to_text(target._summary_current)
        assert target.NO_SUMMARY == text
        # Teardown
        del WIN

    def test_call_cancel(
            self, patch_dialog_run, monkeypatch, patch_view_topics):
        """| Confirm template selection.
        | Case: selection canceled.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._dialog.show()
        target._view_topics.gtk_view.expand_all()

        PATH_ITEM = '1:1:1'
        model = DONOR.gtk_view.get_model()
        i_item = model.get_iter_from_string(PATH_ITEM)
        target._cursor.select_iter(i_item)
        ORDER = QPLACE.Order.BEFORE
        target._order = ORDER
        # Test
        assert target() is None
        assert not target._dialog.get_visible()
        # Teardown
        del WIN

    def test_on_changed_cursor(self, patch_view_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._view_topics.gtk_view.expand_all()

        PATH_ITEM = '0:1'
        model = DONOR.gtk_view.get_model()
        i_item = model.get_iter_from_string(PATH_ITEM)
        item = AOUTLINE.get_item_gtk(model, i_item)
        target._cursor.select_iter(i_item)

        target._button_place.set_sensitive(False)
        target._summary_current.set_text(target.NO_SUMMARY)
        # Test
        target.on_changed_cursor(target._cursor)
        text = self.gtk_to_text(target._summary_current)
        assert item._infoid.summary == text
        assert target._button_place.get_sensitive()
        # Teardown
        del WIN

    def test_on_changed_cursor_to_none(self, patch_view_topics):
        """| Confirm updates when current topic changes.
        | Case: change to no current topic.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._view_topics.gtk_view.expand_all()

        target._cursor.unselect_all()
        target._button_place.set_sensitive(True)
        TEXT = 'The Spanish Inquisition'
        target._summary_current.set_text(TEXT)
        # Test
        target.on_changed_cursor(target._cursor)
        text = self.gtk_to_text(target._summary_current)
        assert target.NO_SUMMARY == text
        assert not target._button_place.get_sensitive()
        # Teardown
        del WIN

    def test_on_changed_cursor_no_topic(self, patch_view_topics):
        """| Confirm updates when current topic changes.
        | Case: change to a topic is that is None.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._view_topics.gtk_view.expand_all()

        PATH_ITEM = '0:1'
        model = DONOR.gtk_view.get_model()
        i_item = model.get_iter_from_string(PATH_ITEM)
        model[i_item][AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM] = None
        target._cursor.select_iter(i_item)

        target._button_place.set_sensitive(True)
        TEXT = 'The Spanish Inquisition'
        target._summary_current.set_text(TEXT)
        # Test
        target.on_changed_cursor(target._cursor)
        text = self.gtk_to_text(target._summary_current)
        assert target.NO_SUMMARY == text
        assert not target._button_place.get_sensitive()
        # Teardown
        del WIN

    @pytest.mark.parametrize(
        'ORDER_OLD, IS_ACTIVE, ORDER_NEW, ORDER_EXPECT', [
            (QPLACE.Order.CHILD, False, QPLACE.Order.AFTER,
             QPLACE.Order.CHILD),
            (QPLACE.Order.CHILD, True, QPLACE.Order.AFTER,
             QPLACE.Order.AFTER),
            (QPLACE.Order.AFTER, True, QPLACE.Order.BEFORE,
             QPLACE.Order.BEFORE),
            (QPLACE.Order.BEFORE, True, QPLACE.Order.CHILD,
             QPLACE.Order.CHILD),
            ])
    def test_on_toggle_order(self, ORDER_OLD, IS_ACTIVE, ORDER_NEW,
                             ORDER_EXPECT, patch_view_topics):
        """Confirm order field set."""
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        target._order = ORDER_OLD
        button = Gtk.ToggleButton(active=IS_ACTIVE)
        # Test
        target.on_toggle_order(button, ORDER_NEW)
        assert target._order is ORDER_EXPECT
        # Teardown
        del WIN

    def test_on_toggle_search_field_inactive(self, patch_view_topics):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        SEARCH_ALL = ~ASHEET.FieldsTopic.VOID
        target._view_topics.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTopic.NAME)
        assert not target._view_topics.scope_search & ASHEET.FieldsTopic.NAME
        assert target._view_topics.scope_search & ASHEET.FieldsTopic.TITLE
        # Teardown
        del WIN

    def test_on_toggle_search_field_active(self, patch_view_topics):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_view_topics
        target = QPLACE.QueryPlace(p_parent=WIN, p_view_topics=DONOR)
        SEARCH_NONE = ASHEET.FieldsTopic.VOID
        target._view_topics.scope_search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test - not active
        target.on_toggle_search_field(button, ASHEET.FieldsTopic.TITLE)
        assert target._view_topics.scope_search & ASHEET.FieldsTopic.TITLE
        assert not target._view_topics.scope_search & ASHEET.FieldsTopic.NAME
        # Teardown
        del WIN
