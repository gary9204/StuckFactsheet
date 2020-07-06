"""
Unit tests for template selection class.  See :mod:`.query_template`.
"""
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content.note import note_spec as XNOTE_SPEC
from factsheet.content.note import note_topic as XNOTE
from factsheet.view import query_template as QTEMPLATES
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
        PATH_ASSIST = str(Path(XNOTE_SPEC.__file__).parent / 'note_spec.ui')
        MODEL_TOPIC = XNOTE.Note
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

        item = XNOTE_SPEC.SpecNote(
            p_name='name_0xx', p_title='title_0xx', p_summary='summary_0xx',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        i_0xx = model.append(None, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_00x', p_title='title_00x', p_summary='summary_00x',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        i_00x = model.append(
            i_0xx, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_000', p_title='title_000', p_summary='summary_000',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        _i_000 = model.append(i_00x, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_01x', p_title='title_01x', p_summary='summary_01x',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        i_0xx = model.append(i_0xx, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_1xx', p_title='title_1xx', p_summary='summary_1xx',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        i_1xx = model.append(None, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_10x', p_title='title_10x', p_summary='summary_10x',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        _i_10x = model.append(i_1xx, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_11x', p_title='title_11x', p_summary='summary_11x',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        i_11x = model.append(i_1xx, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_110', p_title='title_110', p_summary='summary_110',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        _i_110 = model.append(i_11x, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_111', p_title='title_111', p_summary='summary_111',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        _i_111 = model.append(i_11x, [item])
        item = XNOTE_SPEC.SpecNote(
            p_name='name_112', p_title='title_112', p_summary='summary_112',
            p_path_assist=PATH_ASSIST, p_model=MODEL_TOPIC)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_outline(new_outline_model):
    outline = UI.FACTORY_SHEET.new_model_outline_templates()
    outline._gtk_model = new_outline_model()
    return outline


class TestQueryTemplate:
    """Unit tests for :class:`.QueryTemplate`."""

    def test_attr(self):
        """Confirm class attributes are defined."""
        # Setup
        target = QTEMPLATES.QueryTemplate
        # Test
        assert isinstance(target.NO_SUMMARY, str)
        assert target.NO_SUMMARY
        assert isinstance(target.NAME_FILE_QUERY_UI, str)
        assert target.NAME_FILE_QUERY_UI

    def test_init(self):
        """Confirm initialization."""
        # Setup
        WIN = Gtk.Window()
        NAME_CANCEL = 'Cancel'
        NAME_SPEC = 'Specify'
        NAME_SEARCH = 'edit-find-symbolic'
        NAME_INFO = 'dialog-information-symbolic'
        # Test
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        assert isinstance(target._dialog, Gtk.Dialog)
        dialog = target._dialog
        assert dialog.get_transient_for() is WIN
        assert dialog.get_destroy_with_parent()

        header_bar = dialog.get_header_bar()
        button_cancel, button_spec, button_search, button_info = (
            tuple(header_bar.get_children()))

        assert isinstance(button_cancel, Gtk.Button)
        assert NAME_CANCEL == button_cancel.get_label()

        assert isinstance(target._button_specify, Gtk.Button)
        assert target._button_specify is button_spec
        assert NAME_SPEC == button_spec.get_label()
        assert not target._button_specify.get_sensitive()
        style = target._button_specify.get_style_context()
        assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        assert isinstance(button_info, Gtk.ToggleButton)
        assert button_info.get_visible()
        image = button_info.get_image()
        name_image, _size_image = image.get_icon_name()
        assert NAME_INFO == name_image

        assert isinstance(button_search, Gtk.ToggleButton)
        assert button_search.get_visible()
        image = button_search.get_image()
        name_image, _size_image = image.get_icon_name()
        assert NAME_SEARCH == name_image

        assert isinstance(target._outline, ASHEET.AdaptTreeViewTemplate)
        assert target._outline.scope_search is ~ASHEET.FieldsTemplate.VOID
        assert target._outline.gtk_view.get_search_entry() is not None
        assert isinstance(target._cursor, Gtk.TreeSelection)

        assert isinstance(target._summary_current, Gtk.Label)
        assert target._summary_current.get_label() == target.NO_SUMMARY
        # Teardown
        del WIN

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_cursor', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        WIN = Gtk.Window()
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        attribute = getattr(target, NAME_ATTRIBUTE)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers
        # Teardown
        del WIN

    def test_call(self, patch_dialog_run, monkeypatch, patch_outline):
        """| Confirm template selection.
        | Case: template selected.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '1:1:0'
        i_item = OUTLINE._gtk_model.get_iter_from_string(PATH_ITEM)
        item = OUTLINE.get_item(i_item)
        target._cursor.select_iter(i_item)
        # Test
        assert target() is item
        assert not target._dialog.get_visible()
        assert target.NO_SUMMARY == target._summary_current.get_label()
        # Teardown
        del WIN

    def test_call_cancel(
            self, patch_dialog_run, monkeypatch, patch_outline):
        """| Confirm template selection.
        | Case: selected canceled.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '1:1:0'
        i_item = OUTLINE._gtk_model.get_iter_from_string(PATH_ITEM)
        target._cursor.select_iter(i_item)

        target._button_specify.set_sensitive(False)
        target._summary_current.set_markup(target.NO_SUMMARY)
        # Test
        assert target() is None
        assert not target._dialog.get_visible()
        # Teardown
        del WIN

    def test_on_changed_cursor(self, patch_outline):
        """| Confirm updates when current template changes.
        | Case: change to specification template
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '0:0:0'
        i_item = OUTLINE._gtk_model.get_iter_from_string(PATH_ITEM)
        target._cursor.select_iter(i_item)
        item = OUTLINE.get_item(i_item)

        target._button_specify.set_sensitive(False)
        target._summary_current.set_markup(target.NO_SUMMARY)
        # Test
        target.on_changed_cursor(target._cursor)
        assert item.summary == target._summary_current.get_label()
        assert target._button_specify.get_sensitive()
        # Teardown
        del WIN

    def test_on_changed_cursor_to_heading(self, patch_outline):
        """| Confirm updates when current template changes.
        | Case: change to heading template.
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        BLANK = ''
        SUMMARY = 'Something completely different.'
        heading = XHEADING.Heading(
            p_name=BLANK, p_summary=SUMMARY, p_title=BLANK)
        PATH_ITEM = '0:0:0'
        i_item = OUTLINE._gtk_model.get_iter_from_string(PATH_ITEM)
        OUTLINE._gtk_model.set_value(
            i_item, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM, heading)
        target._cursor.select_iter(i_item)

        TEXT = 'The Spanish Inquisition'
        target._summary_current.set_markup(TEXT)
        target._button_specify.set_sensitive(True)
        # Test
        target.on_changed_cursor(target._cursor)
        assert SUMMARY == target._summary_current.get_label()
        assert not target._button_specify.get_sensitive()
        # Teardown
        del WIN

    def test_on_changed_cursor_to_empty(self, patch_outline):
        """| Confirm updates when current template changes.
        | Case: change to template None.
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '0:0:0'
        i_item = OUTLINE._gtk_model.get_iter_from_string(PATH_ITEM)
        OUTLINE._gtk_model.set_value(
            i_item, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM, None)
        target._cursor.select_iter(i_item)

        TEXT = 'The Spanish Inquisition'
        target._summary_current.set_markup(TEXT)
        target._button_specify.set_sensitive(True)
        # Test
        target.on_changed_cursor(target._cursor)
        assert target.NO_SUMMARY == target._summary_current.get_label()
        assert not target._button_specify.get_sensitive()
        # Teardown
        del WIN

    def test_on_changed_cursor_to_none(self, patch_outline):
        """| Confirm updates when current template changes.
        | Case: change to no current template
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        TEXT = 'The Spanish Inquisition'
        target._cursor.unselect_all()

        target._button_specify.set_sensitive(True)
        target._summary_current.set_markup(TEXT)
        # Test
        target.on_changed_cursor(target._cursor)
        assert target.NO_SUMMARY == target._summary_current.get_label()
        assert not target._button_specify.get_sensitive()
        # Teardown
        del WIN

    def test_on_toggle_search_field_inactive(self, patch_outline):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        SEARCH_ALL = ~ASHEET.FieldsTemplate.VOID
        target._outline.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTemplate.NAME)
        assert not target._outline.scope_search & ASHEET.FieldsTemplate.NAME
        assert target._outline.scope_search & ASHEET.FieldsTemplate.TITLE
        # Teardown
        del WIN

    def test_on_toggle_search_field_active(self, patch_outline):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        WIN = Gtk.Window()
        target = QTEMPLATES.QueryTemplate(px_parent=WIN)
        SEARCH_NONE = ASHEET.FieldsTemplate.VOID
        target._outline.scope_search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTemplate.TITLE)
        assert target._outline.scope_search & ASHEET.FieldsTemplate.TITLE
        assert not target._outline.scope_search & ASHEET.FieldsTemplate.NAME
        # Teardown
        del WIN
