"""
Unit test for class to specify modular addition of integers.  See
:mod:`~.plusmodn_spec`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]
import typing

from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content import spec as XSPEC
from factsheet.content.note import note_topic as XNOTE
from factsheet.content.ops.int import plusmodn_spec as XSPEC_PLUS_N
from factsheet.content.ops.int import plusmodn_topic as XPLUS_N
from factsheet.content.sets.int import segint_topic as XSEG_INT
from factsheet.content.sets.int import setint_topic as XSET_INT
from factsheet.model import setindexed as MSET
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
# from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class ITopics:
    """Convenience class for assembling indexes to topics in patch
    topics outline.
    """
    none: Gtk.TreeIter
    heading: Gtk.TreeIter
    note: Gtk.TreeIter
    segment: Gtk.TreeIter
    plus_n: Gtk.TreeIter


@pytest.fixture
def patch_model_topics():
    """Pytest fixture returns sample topics outline for testing."""
    model_topics = UI.FACTORY_SHEET.new_model_outline_topics()

    i_none = model_topics.insert_after(None, None)
    heading = XHEADING.Heading(
        p_name='Heading', p_summary='Heading summary', p_title='Heading Title')
    i_heading = model_topics.insert_after(heading, i_none)
    note = XNOTE.Note(p_name='Note')
    i_note = model_topics.insert_after(note, i_heading)
    segment = XSEG_INT.SegInt(p_name='Segment', p_title='Initial Segment')
    i_segment = model_topics.insert_after(segment, i_note)
    MODULUS = 6
    SET = MSET.SetIndexed(list(range(MODULUS)))
    plus_n = XPLUS_N.PlusModN(p_name='PlusModN', p_set=SET, p_modulus=MODULUS)
    i_plus_n = model_topics.insert_after(plus_n, i_segment)
    indexes = ITopics(i_none, i_heading, i_note, i_segment, i_plus_n)
    return model_topics, indexes


@DC.dataclass(frozen=True)
class ArgsSpec:
    """Convenience class for assembling arguments to
    :class:`.SpecPlusModN` method ``__init__``.
    """
    p_name: str
    p_summary: str
    p_title: str
    p_class_topic: typing.Type[XPLUS_N.PlusModN]
    p_path_assist: XSPEC.StrAssist
    p_new_view_topics: typing.Optional[UI.NewViewOutlineTopics]


@pytest.fixture
def patch_args_spec(patch_model_topics):
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SpecPlusModN` object."""
    model_topics, _indexes = patch_model_topics
    view_topics = UI.FACTORY_SHEET.new_view_outline_topics()
    model_topics.attach_view(view_topics)

    def NEW_VIEW_TOPICS(): return view_topics

    return ArgsSpec(
        p_name='Inquisition',
        p_summary='No one expects the Spanish Inquisition!',
        p_title='The Spanish Inquisition',
        p_class_topic=XPLUS_N.PlusModN,
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_PLUS_N.__file__).parent / 'plusmodn_spec.ui')),
        p_new_view_topics=NEW_VIEW_TOPICS
        )


@pytest.fixture
def patch_ui_confirm(patch_model_topics):
    """Pytest fixture returns user interface objects for page Confirm."""
    model_topics, indexes = patch_model_topics
    view_topics = UI.FACTORY_SHEET.new_view_outline_topics()
    model_topics.attach_view(view_topics)
    cursor = view_topics.gtk_view.get_selection()
    cursor.select_iter(indexes.segment)

    MODULUS = 6
    RANGE = (2, 100)
    spin = Gtk.SpinButton()
    spin.set_range(*RANGE)
    spin.set_value(MODULUS)

    return XSPEC_PLUS_N.UiConfirm(
        ui_cursor=cursor,
        ui_name_set=Gtk.Label(label='Inquisition'),
        ui_title_set=Gtk.Label(label='The Spanish Inquisition!'),
        ui_modulus=spin,
        ui_view_modulus=Gtk.Label(label='Oops! no modulus view.'),
        )


@pytest.fixture
def patch_ui_identify():
    """Pytest fixture returns user interface objects for page Identify."""
    MODULUS = 6
    RANGE = (2, 100)
    spin = Gtk.SpinButton()
    spin.set_range(*RANGE)
    spin.set_value(MODULUS)

    return XSPEC_PLUS_N.UiIdentify(
        ui_modulus=spin,
        ui_name=Gtk.EntryBuffer(text='Parrot'),
        ui_summary=Gtk.TextBuffer(text='The parrot is a Norwegian Blue.'),
        ui_title=Gtk.EntryBuffer(text='The Parrot Sketch'),
        )


@pytest.fixture
def patch_ui_pages(patch_ui_confirm, patch_ui_identify):
    """Pytest fixture returns interface objects for assistant pages."""
    return XSPEC_PLUS_N.UiPages(
        page_confirm=patch_ui_confirm,
        page_identify=patch_ui_identify
        )


class TestSpecPlusModN:
    """Unit tests for :class:`.SpecPlusModN`."""

    def test_call_apply(self, patch_args_spec, monkeypatch):
        """| Confirm call method specifies segment topic.
        | Case: user completes assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(ARGS))
        # Sync identification information with plusmodn_spec.ui.
        NAME = ''
        SUMMARY = ''
        TITLE = ''
        MODULUS = 2
        SET = XSEG_INT.SegInt(p_bound=MODULUS)
        REPS = {0: XSET_INT.ElementInt(0, 0),
                1: XSET_INT.ElementInt(1, 1),
                }

        class PatchMainIteration:
            def __init__(self, p_target):
                self.target = p_target

            def main_iteration(self):
                self.target._response = Gtk.ResponseType.APPLY

        patch_iter = PatchMainIteration(p_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)

        monkeypatch.setattr(
            AOUTLINE, 'get_item_gtk', lambda _m, _i: SET)
        # Test
        result = target()
        assert isinstance(result, XPLUS_N.PlusModN)
        assert NAME == result.name
        assert SUMMARY == result.summary
        assert TITLE == result.title
        assert MODULUS == result._modulus
        assert REPS == result._reps

    def test_call_cancel(self, patch_args_spec, monkeypatch):
        """| Confirm call method specifies segment topic.
        | Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(ARGS))

        class PatchMainIteration:
            def __init__(self, p_target):
                self.target = p_target

            def main_iteration(self):
                self.target._response = Gtk.ResponseType.CANCEL

        patch_iter = PatchMainIteration(p_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert result is None

    @pytest.mark.parametrize('NAME_ITER, RESULT', [
        ('heading', False),
        ('note', False),
        ('segment', True),
        ('plus_n', False),
        ])
    def test_on_changed_cursor(
            self, patch_args_spec, patch_model_topics, NAME_ITER, RESULT):
        """| Confirm updates when current topic changes.
        | Case: change to topic.
        """
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        model_topics, indexes = patch_model_topics
        view_topics = UI.FACTORY_SHEET.new_view_outline_topics()
        model_topics.attach_view(view_topics)
        INDEX = getattr(indexes, NAME_ITER)
        topic = model_topics.get_item(INDEX)
        cursor = view_topics.gtk_view.get_selection()
        cursor.select_iter(INDEX)

        assistant = Gtk.Assistant()
        N_PAGE_SET = 2
        for _ in range(N_PAGE_SET + 1):
            page = Gtk.Label()
            assistant.append_page(page)
            assistant.set_page_complete(page, not RESULT)

        summary_set = Gtk.TextBuffer()
        # Test
        target.on_changed_cursor(cursor, assistant, summary_set)
        assert topic.summary == XSPEC.textbuffer_get_text(summary_set)
        page_set = assistant.get_nth_page(N_PAGE_SET)
        assert assistant.get_page_complete(page_set) is RESULT

    def test_on_changed_cursor_to_empty(
            self, patch_args_spec, patch_model_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic None.
        """
        # Setup
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        model_topics, indexes = patch_model_topics
        view_topics = UI.FACTORY_SHEET.new_view_outline_topics()
        model_topics.attach_view(view_topics)
        cursor = view_topics.gtk_view.get_selection()
        cursor.select_iter(indexes.none)

        assistant = Gtk.Assistant()
        N_PAGE_SET = 2
        for _ in range(N_PAGE_SET + 1):
            page = Gtk.Label()
            assistant.append_page(page)
            assistant.set_page_complete(page, True)

        summary_set = Gtk.TextBuffer()
        # Test
        target.on_changed_cursor(cursor, assistant, summary_set)
        assert target.NO_SUMMARY == XSPEC.textbuffer_get_text(summary_set)
        page_set = assistant.get_nth_page(N_PAGE_SET)
        assert not assistant.get_page_complete(page_set)

    def test_on_changed_cursor_to_none(
            self, patch_args_spec, patch_model_topics):
        """| Confirm updates when current topic changes.
        | Case: change to no current topic.
        """
        # Setup
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        model_topics, _indexes = patch_model_topics
        view_topics = UI.FACTORY_SHEET.new_view_outline_topics()
        model_topics.attach_view(view_topics)
        cursor = view_topics.gtk_view.get_selection()
        cursor.unselect_all()

        assistant = Gtk.Assistant()
        N_PAGE_SET = 2
        for _ in range(N_PAGE_SET + 1):
            page = Gtk.Label()
            assistant.append_page(page)
            assistant.set_page_complete(page, True)

        summary_set = Gtk.TextBuffer()
        # Test
        target.on_changed_cursor(cursor, assistant, summary_set)
        assert target.NO_SUMMARY == XSPEC.textbuffer_get_text(summary_set)
        page_set = assistant.get_nth_page(N_PAGE_SET)
        assert not assistant.get_page_complete(page_set)

    @pytest.mark.parametrize('TITLE_PAGE', [
        'New Operation',
        'Modulus',
        'Set',
        'Identify',
        'Confirm',
        'Oops!'
        ])
    def test_on_prepare(
            self, monkeypatch, TITLE_PAGE, patch_args_spec, patch_ui_pages):
        """Confirm prepare signal dispatch by page title."""
        # Setup
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        # Test
        target.on_prepare(assistant, page, patch_ui_pages)
        # Call success is adequate. Changes checked in other tests.
        # Teardown

    def test_prepare_confirm(
            self, monkeypatch, patch_args_spec, patch_ui_pages):
        """| Confirm prepare signal processing.
        | Case: Confirm page.
        """
        # Setup
        TITLE_PAGE = 'Confirm'
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        UI_PAGES = patch_ui_pages
        page_confirm = UI_PAGES.page_confirm
        model, index = page_confirm.ui_cursor.get_selected()
        topic_set = AOUTLINE.get_item_gtk(model, index)
        modulus = page_confirm.ui_modulus.get_value_as_int()
        text_modulus = '<i>Modulus: </i>{}'.format(modulus)
        # Test
        target.on_prepare(assistant, page, UI_PAGES)
        assert topic_set.name == page_confirm.ui_name_set.get_label()
        assert topic_set.title == page_confirm.ui_title_set.get_label()
        assert text_modulus == page_confirm.ui_view_modulus.get_label()
        # Teardown
        del assistant

    def test_prepare_confirm_none(
            self, monkeypatch, patch_args_spec, patch_ui_pages):
        """| Confirm prepare signal processing.
        | Case: Confirm page.
        """
        # Setup
        TITLE_PAGE = 'Confirm'
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        UI_PAGES = patch_ui_pages
        page_confirm = UI_PAGES.page_confirm
        page_confirm.ui_cursor.unselect_all()
        WARNING = 'Oops! Please go back and select a set.'
        modulus = page_confirm.ui_modulus.get_value_as_int()
        text_modulus = '<i>Modulus: </i>{}'.format(modulus)
        # Test
        target.on_prepare(assistant, page, UI_PAGES)
        assert WARNING == page_confirm.ui_name_set.get_label()
        assert WARNING == page_confirm.ui_title_set.get_label()
        assert text_modulus == page_confirm.ui_view_modulus.get_label()
        # Teardown
        del assistant

    @pytest.mark.parametrize('MODULUS, NAME, SUMMARY, TITLE', [
        (2, '+ (mod 2)', 'The operation is addition modulo 2.',
         'Plus Modulo 2'),
        (42, '+ (mod 42)', 'The operation is addition modulo 42.',
         'Plus Modulo 42'),
        ])
    def test_on_prepare_identify(
            self, MODULUS, NAME, SUMMARY, TITLE, monkeypatch,
            patch_args_spec, patch_ui_pages):
        """| Confirm prepare signal processing.
        | Case: Identify page.
        """
        # Setup
        TITLE_PAGE = 'Identify'
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        UI_PAGES = patch_ui_pages
        page_identify = UI_PAGES.page_identify
        page_identify.ui_modulus.set_value(MODULUS)
        # Test
        target.on_prepare(assistant, page, UI_PAGES)
        assert assistant.get_page_complete(page)

        assert NAME == page_identify.ui_name.get_text()
        assert SUMMARY == XSPEC.textbuffer_get_text(page_identify.ui_summary)
        assert TITLE == page_identify.ui_title.get_text()
        # Teardown
        del assistant

    def test_on_toggle_search_field_active(
            self, patch_args_spec, patch_model_topics):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        SEARCH_ALL = ASHEET.FieldsTemplate.VOID
        view_topics, _indexes = patch_model_topics
        view_topics.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=True)
        # Test
        target.on_toggle_search_field(
            button, view_topics, ASHEET.FieldsTemplate.TITLE)
        assert view_topics.scope_search & ASHEET.FieldsTemplate.TITLE
        assert not view_topics.scope_search & ASHEET.FieldsTemplate.NAME

    def test_on_toggle_search_field_inactive(
            self, patch_args_spec, patch_model_topics):
        """| Confirm search field set.
        | Case: button inactive
        """
        # Setup
        target = XSPEC_PLUS_N.SpecPlusModN(**DC.asdict(patch_args_spec))
        SEARCH_ALL = ~ASHEET.FieldsTemplate.VOID
        view_topics, _indexes = patch_model_topics
        view_topics.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target.on_toggle_search_field(
            button, view_topics, ASHEET.FieldsTemplate.NAME)
        assert not view_topics.scope_search & ASHEET.FieldsTemplate.NAME
        assert view_topics.scope_search & ASHEET.FieldsTemplate.TITLE
