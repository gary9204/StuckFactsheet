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


class TestFieldsIdCore:
    """Unit tests for :class:`.FieldsId`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(VSELECT_SPEC.FieldsId.VOID)
        assert VSELECT_SPEC.FieldsId.NAME
        assert VSELECT_SPEC.FieldsId.SUMMARY
        assert VSELECT_SPEC.FieldsId.TITLE


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
        assert VSELECT_SPEC.FieldsId.NAME == target._scope_search

    def test_init_dialog(self, monkeypatch):
        """Confirm initialization of top-level visual element.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
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

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_dialog(p_parent=WIN, p_get_ui_element=get_ui_element)
        assert isinstance(patch_call.dialog, Gtk.Dialog)
        assert patch_call.dialog.get_transient_for() is WIN
        assert patch_call.dialog.get_destroy_with_parent()

        header_bar = patch_call.dialog.get_header_bar()
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
        class PatchCall:
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

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_outline_specs(get_ui_element)
        assert target._ui_outline_specs.get_model() is target._specs.ui_model
        assert UI_ID == patch_call.id_ui
        assert target._ui_outline_specs is patch_call.site.get_child()
        assert target._ui_outline_specs.get_visible()
        columns = target._ui_outline_specs.get_columns()
        assert target._column_name is columns[C_NAME]
        assert TITLE_C_NAME == target._column_name.get_title()
        assert target._column_title is columns[C_TITLE]
        assert TITLE_C_TITLE == target._column_title.get_title()
        assert N_COLUMNS == len(columns)
        assert target._ui_selection is target._ui_outline_specs.get_selection()

    def test_init_search(self, monkeypatch):
        """Confirm initialization of search bar.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __call__(self, p_id_ui):
                stub = self.stubs.get(p_id_ui)
                return stub

            def __init__(self):
                self.binding = None
                self.connections = list()
                self.stubs = dict(
                    ui_search=Gtk.SearchBar(),
                    ui_header=Gtk.HeaderBar(),
                    ui_search_in_name=Gtk.CheckButton(),
                    ui_search_in_summary=Gtk.CheckButton(),
                    ui_search_in_title=Gtk.CheckButton(),
                    )

            def bind_property(self, *args):
                self.binding = args

        WIN = Gtk.Window()
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        monkeypatch.setattr(
            Gtk.ToggleButton, 'bind_property', patch_call.bind_property)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        PROP_SOURCE = 'active'
        PROP_TARGET = 'search-mode-enabled'
        I_FIND = 0
        LABEL_FIND = 'Find'
        # Test
        target._init_search(get_ui_element)
        assert VSELECT_SPEC.FieldsId.NAME == target._scope_search
        prop_source, target, prop_target, flags = patch_call.binding
        assert PROP_SOURCE == prop_source
        assert isinstance(target, Gtk.SearchBar)
        assert PROP_TARGET == prop_target
        assert GO.BindingFlags.BIDIRECTIONAL == flags
        header_bar = patch_call.stubs['ui_header']
        buttons = header_bar.get_children()
        button_find = buttons[I_FIND]
        assert LABEL_FIND == button_find.get_label()
        assert isinstance(button_find, Gtk.ToggleButton)
        assert button_find.get_visible()

    @pytest.mark.parametrize('NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT', [
        ('toggled', 'ui_search_in_name', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_in_summary', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_in_title', Gtk.CheckButton, 0),
        ])
    def test_init_search_signals(
            self, monkeypatch, NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param NAME_SIGNAL: name of signal.
        :param NAME_BUTTON: name of search button connected to signal.
        :param ORIGIN: GTK class of connected attribute.
        :param N_DEFAULT: number of default handlers.
        """
        # Setup
        class PatchCall:
            def __call__(self, p_id_ui):
                stub = self.stubs.get(p_id_ui)
                return stub

            def __init__(self):
                self.stubs = dict(
                    ui_search=Gtk.SearchBar(),
                    ui_header=Gtk.HeaderBar(),
                    ui_search_in_name=Gtk.CheckButton(),
                    ui_search_in_summary=Gtk.CheckButton(),
                    ui_search_in_title=Gtk.CheckButton(),
                    )

        WIN = Gtk.Window()
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')

        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target._init_search(get_ui_element)
        button = patch_call.stubs[NAME_BUTTON]
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                button, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(button, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_ui_selection', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param NAME_SIGNAL: name of signal.
        :param NAME_ATTRIBUTE: name of attribute connected to signal.
        :param ORIGIN: GTK class of connected attribute.
        :param N_DEFAULT: number of default handlers.
        """
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

    def test_init_summary(self, monkeypatch):
        """Confirm initialization of spec summary.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.site = Gtk.Viewport()

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.site

        WIN = Gtk.Window()
        UI_ID = 'ui_site_summary'
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_summary(get_ui_element)
        assert UI_ID == patch_call.id_ui
        view_summary = patch_call.site.get_child()
        assert view_summary.get_visible()
        assert target._summary.ui_model is view_summary.get_buffer()
        assert view_summary.get_wrap_mode() is Gtk.WrapMode.WORD_CHAR

    def test_call(self, patch_dialog_run, monkeypatch, patch_g_specs):
        """| Confirm spec selection.
        | Case: spec chosen.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        specs = SPECS.g_specs
        N_SPECS = 5
        I_CHOSEN = 3
        for i in range(N_SPECS):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            spec = SBASE.Base(p_name=name, p_summary='', p_title=title)
            line = specs.insert_before(p_item=spec, p_line=None)
            if I_CHOSEN == i:
                spec_chosen = spec
                line_chosen = line
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._ui_outline_specs.expand_all()
        target._ui_selection.select_iter(line_chosen)
        target._dialog.show()
        # Test
        assert target() is spec_chosen
        assert not target._dialog.get_visible()
        assert target.NO_SUMMARY == target._summary.text

    def test_call_cancel(self, patch_dialog_run, monkeypatch, patch_g_specs):
        """| Confirm spec selection.
        | Case: no spec chosen.
        """
        # Setup
        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)

        WIN = Gtk.Window()
        specs = SPECS.g_specs
        N_SPECS = 5
        for i in range(N_SPECS):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            spec = SBASE.Base(p_name=name, p_summary='', p_title=title)
            _line = specs.insert_before(p_item=spec, p_line=None)
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._ui_outline_specs.expand_all()
        line_chosen = target._specs.ui_model.get_iter_first()
        target._ui_selection.select_iter(line_chosen)
        target._dialog.show()
        # Test
        assert target() is None
        assert not target._dialog.get_visible()
        assert target.NO_SUMMARY == target._summary.text

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

    @pytest.mark.parametrize('SCOPE, BUTTON, FIELD, EXPECT', [
        (VSELECT_SPEC.FieldsId.VOID, True, VSELECT_SPEC.FieldsId.NAME,
         VSELECT_SPEC.FieldsId.NAME),
        (VSELECT_SPEC.FieldsId.VOID, True, VSELECT_SPEC.FieldsId.SUMMARY,
         VSELECT_SPEC.FieldsId.SUMMARY),
        (VSELECT_SPEC.FieldsId.VOID, True, VSELECT_SPEC.FieldsId.TITLE,
         VSELECT_SPEC.FieldsId.TITLE),
        (~VSELECT_SPEC.FieldsId.VOID, False, VSELECT_SPEC.FieldsId.NAME,
         VSELECT_SPEC.FieldsId.SUMMARY | VSELECT_SPEC.FieldsId.TITLE),
        ])
    def test_on_changed_search_scope(self, SCOPE, BUTTON, FIELD, EXPECT):
        """| Confirm change in search scope."""
        # Setup
        WIN = Gtk.Window()
        target = VSELECT_SPEC.SelectSpec(p_parent=WIN)
        target._scope_search = SCOPE
        button = Gtk.ToggleButton(active=BUTTON)
        # Test
        target.on_changed_search_scope(button, FIELD)
        assert EXPECT == target._scope_search
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

    # @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
    #     # (VSELECT_SPEC.g_specs, BUI.ModelOutlineMulti),
    #     ])
    # def test_attributes(self, ATTR, TYPE_EXPECT):
    #     """Confirm type alias definitions.
    #
    #     :param TYPE_TARGET: type alias under test.
    #     :param TYPE_EXPECT: type expected.
    #     """
    #     # Setup
    #     # Test
    #     assert isinstance(ATTR, TYPE_EXPECT)
