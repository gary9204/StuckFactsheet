"""
Unit tests for topic placement class.  See :mod:`.query_place`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content.outline import topic as TOPIC
from factsheet.view import query_place as QPLACE
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def new_outline_model():
    """Pytest fixture returns outline model factory.  The structure of
    each model is as follows.

        | name_0xx | title_0xx | summary_0xx
        |     name_00x | title_00x | summary_00x
        |         name_000 | title_000 | summary_000
        |     name_01x | title_01x | summary_01x
        | name_1xx | title_1xx | summary_1xx
        |     name_10x | title_10x | summary_10x
        |     name_11x | title_11x | summary_11x
        |         name_110 | title_110 | summary_110
        |         name_111 | title_111 | summary_111
        |         name_112 | title_112 | summary_112
    """
    def new_model():
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

        item = TOPIC.Topic(
            p_name='name_0xx', p_title='title_0xx', p_summary='summary_0xx')
        i_0xx = model.append(None, [item])
        item = TOPIC.Topic(
            p_name='name_00x', p_title='title_00x', p_summary='summary_00x')
        i_00x = model.append(
            i_0xx, [item])
        item = TOPIC.Topic(
            p_name='name_000', p_title='title_000', p_summary='summary_000')
        _i_000 = model.append(i_00x, [item])
        item = TOPIC.Topic(
            p_name='name_01x', p_title='title_01x', p_summary='summary_01x')
        i_0xx = model.append(i_0xx, [item])
        item = TOPIC.Topic(
            p_name='name_1xx', p_title='title_1xx', p_summary='summary_1xx')
        i_1xx = model.append(None, [item])
        item = TOPIC.Topic(
            p_name='name_10x', p_title='title_10x', p_summary='summary_10x')
        _i_10x = model.append(i_1xx, [item])
        item = TOPIC.Topic(
            p_name='name_11x', p_title='title_11x', p_summary='summary_11x')
        i_11x = model.append(i_1xx, [item])
        item = TOPIC.Topic(
            p_name='name_110', p_title='title_110', p_summary='summary_110')
        _i_110 = model.append(i_11x, [item])
        item = TOPIC.Topic(
            p_name='name_111', p_title='title_111', p_summary='summary_111')
        _i_111 = model.append(i_11x, [item])
        item = TOPIC.Topic(
            p_name='name_112', p_title='title_112', p_summary='summary_112')
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_donor_outline(new_outline_model):
    """Pytest fixture returns view of topic outline."""
    outline = UI.FACTORY_SHEET.new_view_outline_topics()
    gtk_model = new_outline_model()
    outline.gtk_view.set_model(gtk_model)
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

    def test_init(self, patch_donor_outline):
        """Confirm initialization."""
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        NAME_CANCEL = 'Cancel'
        NAME_PLACE = 'Place'
        NAME_SEARCH = 'edit-find-symbolic'
        NAME_INFO = 'dialog-information-symbolic'
        # Test
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
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

        assert isinstance(target._outline, ASHEET.AdaptTreeViewTopic)
        gtk_view = target._outline.gtk_view
        assert gtk_view is not DONOR.gtk_view
        assert gtk_view.get_model() is DONOR.gtk_view.get_model()
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

    def test_call(self, patch_dialog_run, monkeypatch, patch_donor_outline):
        """| Confirm template selection.
        | Case: template selected.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._dialog.show()
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '1:1:1'
        model = DONOR.gtk_view.get_model()
        i_item = model.get_iter_from_string(PATH_ITEM)
        item = AOUTLINE.get_item_gtk(model, i_item)
        target._cursor.select_iter(i_item)
        ORDER = QPLACE.Order.BEFORE
        target._order = ORDER
        # Test
        assert (item, ORDER) == target()
        assert patch_dialog.called
        assert not target._dialog.get_visible()
        text = self.gtk_to_text(target._summary_current)
        assert target.NO_SUMMARY == text
        # Teardown
        del WIN

    def test_call_cancel(
            self, patch_dialog_run, monkeypatch, patch_donor_outline):
        """| Confirm template selection.
        | Case: selection canceled.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._dialog.show()
        target._outline.gtk_view.expand_all()

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

    def test_on_changed_cursor(self, patch_donor_outline):
        """| Confirm updates when current topic changes.
        | Case: change to topic.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._outline.gtk_view.expand_all()

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

    def test_on_changed_cursor_to_none(self, patch_donor_outline):
        """| Confirm updates when current topic changes.
        | Case: change to no current topic.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._outline.gtk_view.expand_all()

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

    def test_on_changed_cursor_no_topic(self, patch_donor_outline):
        """| Confirm updates when current topic changes.
        | Case: change to a topic is that is None.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._outline.gtk_view.expand_all()

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
                             ORDER_EXPECT, patch_donor_outline):
        """Confirm order field set."""
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        target._order = ORDER_OLD
        button = Gtk.ToggleButton(active=IS_ACTIVE)
        # Test
        target.on_toggle_order(button, ORDER_NEW)
        assert target._order is ORDER_EXPECT
        # Teardown
        del WIN

    def test_on_toggle_search_field_inactive(self, patch_donor_outline):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        SEARCH_ALL = ~ASHEET.FieldsTopic.VOID
        target._outline._search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTopic.NAME)
        assert not target._outline._search & ASHEET.FieldsTopic.NAME
        assert target._outline._search & ASHEET.FieldsTopic.TITLE
        # Teardown
        del WIN

    def test_on_toggle_search_field_active(self, patch_donor_outline):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        WIN = Gtk.Window()
        DONOR = patch_donor_outline
        target = QPLACE.QueryPlace(px_parent=WIN, px_donor_outline=DONOR)
        SEARCH_NONE = ASHEET.FieldsTopic.VOID
        target._outline._search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test - not active
        target.on_toggle_search_field(button, ASHEET.FieldsTopic.TITLE)
        assert target._outline._search & ASHEET.FieldsTopic.TITLE
        assert not target._outline._search & ASHEET.FieldsTopic.NAME
        # Teardown
        del WIN
