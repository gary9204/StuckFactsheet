"""
Unit tests for class to select a topic specification.  See
:mod:`.select_spec`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

# from factsheet.content import heading as XHEADING
# from factsheet.content import spec as XSPEC
# from factsheet.content.note import spec_note as XSPEC_NOTE
# from factsheet.content.note import topic_note as XNOTE
# from factsheet.model import types_model as MTYPES
import factsheet.bridge_ui as BUI
import factsheet.spec as SPECS
import factsheet.spec.base_s as SBASE
import factsheet.view.select_spec as VSELECT_SPEC
import factsheet.view.ui as UI

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
        model = None
        # CLASS_TOPIC = XNOTE.Note
        # PATH_ASSIST = XSPEC.StrAssist(
        #     str(Path(XSPEC_NOTE.__file__).parent / 'spec_note.ui'))
        # # VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        #
        # def ATTACH_VIEW_TOPICS(_view): pass
        #
        # model = Gtk.TreeStore(GO.TYPE_PYOBJECT)
        #
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_0xx', p_title='title_0xx', p_summary='summary_0xx',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # i_0xx = model.append(None, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_00x', p_title='title_00x', p_summary='summary_00x',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # i_00x = model.append(
        #     i_0xx, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_000', p_title='title_000', p_summary='summary_000',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # _i_000 = model.append(i_00x, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_01x', p_title='title_01x', p_summary='summary_01x',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # i_0xx = model.append(i_0xx, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_1xx', p_title='title_1xx', p_summary='summary_1xx',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # i_1xx = model.append(None, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_10x', p_title='title_10x', p_summary='summary_10x',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # _i_10x = model.append(i_1xx, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_11x', p_title='title_11x', p_summary='summary_11x',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # i_11x = model.append(i_1xx, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_110', p_title='title_110', p_summary='summary_110',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # _i_110 = model.append(i_11x, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_111', p_title='title_111', p_summary='summary_111',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # _i_111 = model.append(i_11x, [item])
        # item = XSPEC_NOTE.SpecNote(
        #     p_name='name_112', p_title='title_112', p_summary='summary_112',
        #     p_path_assist=PATH_ASSIST, p_class_topic=CLASS_TOPIC,
        #     p_attach_view_topics=ATTACH_VIEW_TOPICS)
        # _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_outline(new_outline_model):
    outline = None
    # outline = MTYPES.OutlineTemplates()
    # outline._ui_model = new_outline_model()
    return outline


# @pytest.fixture
# def patch_g_specs():
#     """Pytest fixture with teardown: Reset :data:`.g_specs`."""
#     g_specs = SPECS.g_specs
#     SPECS.g_specs = SPECS.BUI.ModelOutlineMulti[SBASE.Base]()
#     yield
#     SPECS.g_specs = g_specs


@pytest.fixture
def patch_g_specs():
    """Pytest fixture with teardown: Reset :data:`.g_specs`."""
    g_specs = SPECS.g_specs
    g_specs_saved = SPECS.BUI.ModelOutlineMulti[SBASE.Base]()
    g_specs_saved.insert_section(SPECS.g_specs)
    g_specs.clear()
    yield
    g_specs.clear()
    g_specs.insert_section(g_specs_saved)


class TestSelectSpec:
    """Unit tests for :class:`.SelectSpec`."""

    def test_no_summary(self):
        """Confirm class attribute definition."""
        # Setup
        target = VSELECT_SPEC.SelectSpec
        EXPECT = 'Please choose a specification for a new topic.'
        # Test
        assert isinstance(target.NO_SUMMARY, str)
        assert EXPECT == target.NO_SUMMARY

    def test_init(self):
        """Confirm initialization orchestration."""
        # Setup
        WIN = Gtk.Window()
        # NAME_SEARCH = 'edit-find-symbolic'
        # NAME_INFO = 'dialog-information-symbolic'
        # Test
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        assert target._specs is SPECS.g_specs
        assert target._dialog is not None
        assert target._ui_outline_specs is not None
        assert target.NO_SUMMARY == target._summary.text

    def test_init_dialog(self, monkeypatch):
        """Confirm initialization of top-level visual element.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGet:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.dialog = Gtk.Dialog(use_header_bar=True)

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.dialog

        WIN = Gtk.Window()
        I_CANCEL = 0
        NAME_CANCEL = 'Cancel'
        I_SELECT = 1
        NAME_SELECT = 'Select'
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_get = PatchGet()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_get.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_dialog(p_parent=WIN, p_get_ui_element=get_ui_element)
        assert isinstance(patch_get.dialog, Gtk.Dialog)
        assert patch_get.dialog.get_transient_for() is WIN
        assert patch_get.dialog.get_destroy_with_parent()

        header_bar = patch_get.dialog.get_header_bar()
        buttons = header_bar.get_children()
        button_cancel = buttons[I_CANCEL]
        assert isinstance(button_cancel, Gtk.Button)
        assert NAME_CANCEL == button_cancel.get_label()
        button_select = buttons[I_SELECT]
        assert isinstance(target._button_select, Gtk.Button)
        assert target._button_select is button_select
        assert NAME_SELECT == button_select.get_label()
        style = target._button_select.get_style_context()
        assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        assert not target._button_select.get_sensitive()

        # assert isinstance(button_info, Gtk.ToggleButton)
        # assert button_info.get_visible()
        # image = button_info.get_image()
        # name_image, _size_image = image.get_icon_name()
        # assert NAME_INFO == name_image

        # assert isinstance(button_search, Gtk.ToggleButton)
        # assert button_search.get_visible()
        # image = button_search.get_image()
        # name_image, _size_image = image.get_icon_name()
        # assert NAME_SEARCH == name_image

    def test_init_outline_specs(self, monkeypatch):
        """Confirm initialization of spec outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGet:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.site = Gtk.Viewport()

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.site

        WIN = Gtk.Window()
        UI_ID = 'ui_site_outline_specs'
        N_COLUMNS = 2
        C_NAME = 0
        TITLE_C_NAME = 'Name'
        C_TITLE = 1
        TITLE_C_TITLE = 'Title'
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_get = PatchGet()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_get.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_outline_specs(get_ui_element)
        assert target._ui_outline_specs.get_model() is target._specs.ui_model
        assert UI_ID == patch_get.id_ui
        assert target._ui_outline_specs is patch_get.site.get_child()
        assert target._ui_outline_specs.get_visible()
        columns = target._ui_outline_specs.get_columns()
        assert target._column_name is columns[C_NAME]
        assert TITLE_C_NAME == target._column_name.get_title()
        assert target._column_title is columns[C_TITLE]
        assert TITLE_C_TITLE == target._column_title.get_title()
        assert N_COLUMNS == len(columns)
        assert target._ui_selection is target._ui_outline_specs.get_selection()

        # assert isinstance(target._outline, ASHEET.AdaptTreeViewTemplate)
        # assert target._outline.scope_search is ~ASHEET.FieldsTemplate.VOID
        # assert target._outline.gtk_view.get_search_entry() is not None
        # assert isinstance(target._cursor, Gtk.TreeSelection)

        # assert isinstance(target._summary_current, Gtk.Label)
        # assert target._summary_current.get_label() == target.NO_SUMMARY
        # # Teardown
        # del WIN

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_ui_selection', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        WIN = Gtk.Window()
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
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

    def test_init_summary(self, monkeypatch):
        """Confirm initialization of spec summary.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGet:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.site = Gtk.Viewport()

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.site

        WIN = Gtk.Window()
        UI_ID = 'ui_site_summary'
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_get = PatchGet()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_get.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_summary(get_ui_element)
        assert UI_ID == patch_get.id_ui
        view_summary = patch_get.site.get_child()
        assert view_summary.get_visible()
        assert target._summary.ui_model is view_summary.get_buffer()
        assert view_summary.get_wrap_mode() is Gtk.WrapMode.WORD_CHAR

    @pytest.mark.skip
    def test_call(self, patch_dialog_run, monkeypatch, patch_outline):
        """| Confirm template selection.
        | Case: template selected.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        target = QTEMPLATES.QueryTemplate(
            p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '1:1:0'
        i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        item = OUTLINE.get_item(i_item)
        target._cursor.select_iter(i_item)
        # Test
        assert target() is item
        assert not target._dialog.get_visible()
        assert target.NO_SUMMARY == target._summary_current.get_label()
        # Teardown
        del WIN

    @pytest.mark.skip
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
        VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        target = QTEMPLATES.QueryTemplate(
            p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
        OUTLINE = patch_outline
        OUTLINE.attach_view(target._outline)
        target._outline.gtk_view.expand_all()

        PATH_ITEM = '1:1:0'
        i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        target._cursor.select_iter(i_item)

        target._button_specify.set_sensitive(False)
        target._summary_current.set_markup(target.NO_SUMMARY)
        # Test
        assert target() is None
        assert not target._dialog.get_visible()
        # Teardown
        del WIN

    @pytest.mark.parametrize('METHOD, I_LINE, EXPECT', [
        ('_markup_cell_name', 0, 'Name 0'),
        ('_markup_cell_name', 3, 'Name 3'),
        ('_markup_cell_title', 2, 'Title 2'),
        ('_markup_cell_title', 4, 'Title 4'),
        ])
    def test_markup_cell(self, patch_g_specs, METHOD, I_LINE, EXPECT):
        """Confirm cell data function updates column text.

        :param METHOD: markup method under test.
        :param I_LINE: index in outline of sample line.
        :param EXPECT: text to expect in cell.
        """
        # Setup
        WIN = Gtk.Window()
        specs = SPECS.g_specs
        N_SPECS = 5
        for i in range(N_SPECS):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            spec = SBASE.Base(p_name=name, p_summary='', p_title=title)
            _ = specs.insert_before(p_item=spec, p_line=None)
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        ui_model_specs = specs.ui_model
        line = ui_model_specs.get_iter_from_string(str(I_LINE))
        # Test
        target_method(None, render, ui_model_specs, line, None)
        assert EXPECT == render.get_property('text')

    @pytest.mark.parametrize('METHOD', [
        ('_markup_cell_name'),
        ('_markup_cell_title'),
        ])
    def test_markup_cell_none(self, patch_g_specs, METHOD):
        """Confirm cell data function updates column text.

        :param METHOD: markup method under test.
        """
        # Setup
        WIN = Gtk.Window()
        specs = SPECS.g_specs
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        ui_model_specs = specs.ui_model
        ui_model_specs.append(None, [None])
        line = ui_model_specs.get_iter_first()
        EXPECT = 'Missing'
        # Test
        target_method(None, render, None, line, None)
        assert EXPECT == render.get_property('text')

    def test_on_changed_selection(self, patch_g_specs):
        """| Confirm summary shown matches chosen spec.
        | Case: a spec at line choosen.
        """
        # Setup
        WIN = Gtk.Window()
        specs = SPECS.g_specs
        N_SPECS = 5
        I_SPEC = 3
        for i in range(N_SPECS):
            summary = 'Summary {}'.format(i)
            spec = SBASE.Base(p_name='', p_summary=summary, p_title='')
            line = specs.insert_before(p_item=spec, p_line=None)
            if I_SPEC == i:
                summary_expect = summary
                line_spec = line
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._ui_outline_specs.expand_all()
        target._ui_selection.select_iter(line_spec)
        # target._ui_selection.unselect_all()
        target._summary.text = 'Oops'
        target._button_select.set_sensitive(False)
        # Test
        target.on_changed_selection(None)
        # Test
        assert summary_expect == target._summary.text
        assert target._button_select.get_sensitive()

    def test_on_changed_selection_absent(self, patch_g_specs):
        """| Confirm summary shown matches chosen spec.
        | Case: no spec at line choosen.
        """
        # Setup
        WIN = Gtk.Window()
        specs = SPECS.g_specs
        line = specs.ui_model.append(None, [None])
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._ui_outline_specs.expand_all()
        target._ui_selection.select_iter(line)
        target._summary.text = 'Oops'
        target._button_select.set_sensitive(True)
        # Test
        target.on_changed_selection(None)
        assert target.NO_SUMMARY == target._summary.text
        assert not target._button_select.get_sensitive()

    def test_on_changed_selection_none(self, patch_g_specs):
        """| Confirm summary shown matches chosen spec.
        | Case: no spec is choosen.
        """
        # Setup
        WIN = Gtk.Window()
        specs = SPECS.g_specs
        N_SPECS = 5
        for i in range(N_SPECS):
            summary = 'Summary {}'.format(i)
            spec = SBASE.Base(p_name='', p_summary=summary, p_title='')
            _line = specs.insert_before(p_item=spec, p_line=None)
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._ui_outline_specs.expand_all()
        target._ui_selection.unselect_all()
        target._summary.text = 'Oops'
        target._button_select.set_sensitive(True)
        # Test
        target.on_changed_selection(None)
        assert target.NO_SUMMARY == target._summary.text
        assert not target._button_select.get_sensitive()

    # @pytest.mark.skip(reason='Next')
    # def test_on_changed_selection_none(self, patch_g_specs):
    #     """| Confirm summary shown matches chosen spec.
    #     | Case: no spec is choosen.
    #     """
    #     # Setup
    #     WIN = Gtk.Window()
    #     specs = SPECS.g_specs
    #     N_SPECS = 5
    #     for i in range(N_SPECS):
    #         summary = 'Summary {}'.format(i)
    #         spec = SBASE.Base(p_name='', p_summary=summary, p_title='')
    #         _ = specs.insert_before(p_item=spec, p_line=None)
    #     target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
    #     # Test
    #     target._ui_selection.unselect_all()
    #     assert False
    #     assert target.NO_SUMMARY == target._summary.text
    #     # control_sheet = CSHEET.ControlSheet(p_path=None)
    #     # target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
    #     # N_WIDTH = 4
    #     # N_DEPTH = 5
    #     # _ = fill_topics(control_sheet, N_WIDTH, N_DEPTH)
    #     # ui_model_topics = target._ui_outline_topics.get_model()
    #     # line_topic = ui_model_topics.get_iter_from_string('3:0')
    #     # control_topic = target._control_sheet.get_control_topic(line_topic)
    #     # view_topic = VTOPIC.ViewTopic(p_control=control_topic)
    #     # name_topic = VTOPICS.EditorTopics.name_tag(control_topic.tag)
    #     # target._views_topics.add_view(view_topic.ui_view, name_topic)
    #     # _ = target._views_topics.show_view(name_topic)
    #     # target._ui_outline_topics.expand_all()
    #     # target._ui_selection.select_iter(line_topic)
    #     # # Test
    #     # target._ui_selection.unselect_all()
    #     # name_visible = target._views_topics.ui_view.get_visible_child_name()
    #     # assert target._name_view_default == name_visible

    # @pytest.mark.skip
    # def test_on_changed_cursor(self, patch_outline):
    #     """| Confirm updates when current template changes.
    #     | Case: change to specification template
    #     """
    #     # Setup
    #     WIN = Gtk.Window()
    #     VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     target = QTEMPLATES.QueryTemplate(
    #         p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
    #     OUTLINE = patch_outline
    #     OUTLINE.attach_view(target._outline)
    #     target._outline.gtk_view.expand_all()
    #
    #     PATH_ITEM = '0:0:0'
    #     i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
    #     target._cursor.select_iter(i_item)
    #     item = OUTLINE.get_item(i_item)
    #
    #     target._button_specify.set_sensitive(False)
    #     target._summary_current.set_markup(target.NO_SUMMARY)
    #     # Test
    #     target.on_changed_cursor(target._cursor)
    #     assert item.summary == target._summary_current.get_label()
    #     assert target._button_specify.get_sensitive()
    #     # Teardown
    #     del WIN

    # @pytest.mark.skip
    # def test_on_changed_cursor_to_heading(self, patch_outline):
    #     """| Confirm updates when current template changes.
    #     | Case: change to heading template.
    #     """
    #     # Setup
    #     WIN = Gtk.Window()
    #     VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     target = QTEMPLATES.QueryTemplate(
    #         p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
    #     OUTLINE = patch_outline
    #     OUTLINE.attach_view(target._outline)
    #     target._outline.gtk_view.expand_all()
    #
    #     BLANK = ''
    #     SUMMARY = 'Something completely different.'
    #     heading = XHEADING.Heading(
    #         p_name=BLANK, p_summary=SUMMARY, p_title=BLANK)
    #     PATH_ITEM = '0:0:0'
    #     i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
    #     OUTLINE._ui_model.set_value(
    #         i_item, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM, heading)
    #     target._cursor.select_iter(i_item)
    #
    #     TEXT = 'The Spanish Inquisition'
    #     target._summary_current.set_markup(TEXT)
    #     target._button_specify.set_sensitive(True)
    #     # Test
    #     target.on_changed_cursor(target._cursor)
    #     assert SUMMARY == target._summary_current.get_label()
    #     assert not target._button_specify.get_sensitive()
    #     # Teardown
    #     del WIN

    # @pytest.mark.skip
    # def test_on_changed_cursor_to_empty(self, patch_outline):
    #     """| Confirm updates when current template changes.
    #     | Case: change to template None.
    #     """
    #     # Setup
    #     WIN = Gtk.Window()
    #     VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     target = QTEMPLATES.QueryTemplate(
    #         p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
    #     OUTLINE = patch_outline
    #     OUTLINE.attach_view(target._outline)
    #     target._outline.gtk_view.expand_all()
    #
    #     PATH_ITEM = '0:0:0'
    #     i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
    #     OUTLINE._ui_model.set_value(
    #         i_item, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM, None)
    #     target._cursor.select_iter(i_item)
    #
    #     TEXT = 'The Spanish Inquisition'
    #     target._summary_current.set_markup(TEXT)
    #     target._button_specify.set_sensitive(True)
    #     # Test
    #     target.on_changed_cursor(target._cursor)
    #     assert target.NO_SUMMARY == target._summary_current.get_label()
    #     assert not target._button_specify.get_sensitive()
    #     # Teardown
    #     del WIN

    # @pytest.mark.skip
    # def test_on_changed_cursor_to_none(self, patch_outline):
    #     """| Confirm updates when current template changes.
    #     | Case: change to no current template
    #     """
    #     # Setup
    #     WIN = Gtk.Window()
    #     VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     target = QTEMPLATES.QueryTemplate(
    #         p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
    #     OUTLINE = patch_outline
    #     OUTLINE.attach_view(target._outline)
    #     target._outline.gtk_view.expand_all()
    #
    #     TEXT = 'The Spanish Inquisition'
    #     target._cursor.unselect_all()
    #
    #     target._button_specify.set_sensitive(True)
    #     target._summary_current.set_markup(TEXT)
    #     # Test
    #     target.on_changed_cursor(target._cursor)
    #     assert target.NO_SUMMARY == target._summary_current.get_label()
    #     assert not target._button_specify.get_sensitive()
    #     # Teardown
    #     del WIN

    @pytest.mark.skip
    def test_on_toggle_search_field_inactive(self, patch_outline):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        WIN = Gtk.Window()
        VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        target = QTEMPLATES.QueryTemplate(
            p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
        SEARCH_ALL = ~ASHEET.FieldsTemplate.VOID
        target._outline.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTemplate.NAME)
        assert not target._outline.scope_search & ASHEET.FieldsTemplate.NAME
        assert target._outline.scope_search & ASHEET.FieldsTemplate.TITLE
        # Teardown
        del WIN

    @pytest.mark.skip
    def test_on_toggle_search_field_active(self, patch_outline):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        WIN = Gtk.Window()
        VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        target = QTEMPLATES.QueryTemplate(
            p_parent=WIN, p_attach_view_topics=VIEW_TOPICS)
        SEARCH_NONE = ASHEET.FieldsTemplate.VOID
        target._outline.scope_search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test
        target.on_toggle_search_field(button, ASHEET.FieldsTemplate.TITLE)
        assert target._outline.scope_search & ASHEET.FieldsTemplate.TITLE
        assert not target._outline.scope_search & ASHEET.FieldsTemplate.NAME
        # Teardown
        del WIN

    def test_set_no_spec(self):
        """Confirm summary content and Specify button state."""
        # Setup
        WIN = Gtk.Window()
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._summary.text = 'Oops'
        target._button_select.set_sensitive(True)
        # Test
        target._set_no_spec()
        assert target.NO_SUMMARY == target._summary.text
        assert not target._button_select.get_sensitive()


class TestModule:
    """Unit tests for module-level components of :mod:`.editor_topics`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        # (VTOPICS.UiEditorTopics, Gtk.Frame),
        (VSELECT_SPEC.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (VSELECT_SPEC.ModelSummary, BUI.ModelTextStyled),
        (VSELECT_SPEC.ViewOutlineSpec, BUI.ViewOutline),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT

    @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
        # (VSELECT_SPEC.g_specs, BUI.ModelOutlineMulti),
        ])
    def test_attributes(self, ATTR, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert isinstance(ATTR, TYPE_EXPECT)
