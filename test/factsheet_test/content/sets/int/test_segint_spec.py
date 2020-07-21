"""
Unit test for class to specify an initial segment of natural numbers.
See :mod:`~.segint_spec`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]
import typing

from factsheet.content import spec as XSPEC
from factsheet.content.sets.int import segint_spec as XSPEC_SEGINT
from factsheet.content.sets.int import segint_topic as XSEGINT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass(frozen=True)
class ArgsSpec:
    """Convenience class for assembling arguments to
    :class:`.SpecSegInt` method ``__init__``.
    """
    p_name: str
    p_summary: str
    p_title: str
    p_class_topic: typing.Type[XSEGINT.SegInt]
    p_path_assist: XSPEC.StrAssist
    p_new_view_topics: typing.Optional[typing.Callable]


@pytest.fixture
def patch_args_spec():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SpecSegInt` object."""
    return ArgsSpec(
        p_name='Inquisition',
        p_summary='No one expects the Spanish Inquisition!',
        p_title='The Spanish Inquisition',
        p_class_topic=XSEGINT.SegInt,
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_SEGINT.__file__).parent / 'segint_spec.ui')),
        p_new_view_topics=None
        )


@pytest.fixture
def patch_ui_args():
    """Pytest fixture returns seto if interface objects for prepare signal."""
    BOUND = 42
    RANGE = (1, 100)
    spin = Gtk.SpinButton()
    spin.set_range(*RANGE)
    spin.set_value(BOUND)
    return XSPEC_SEGINT.UiArgs(
        ui_name=Gtk.EntryBuffer(text='Parrot'),
        ui_summary=Gtk.TextBuffer(text='The parrot is a Norwegian Blue.'),
        ui_title=Gtk.EntryBuffer(text='The Parrot Sketch'),
        ui_bound=spin,
        ui_segment=Gtk.Label(label='Something completely different')
        )


class TestSpecSegInt:
    """Unit tests for :class:`.SpecSegInt`."""

    def test_call_apply(self, patch_args_spec, monkeypatch):
        """| Confirm call method specifies segment topic.
        | Case: user completes assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        # Sync identification information with segint_spec.ui.
        NAME = ''
        SUMMARY = 'This topic is an initial segment of natural numbers.'
        TITLE = ''
        BOUND = 1

        class PatchMainIteration:
            def __init__(self, p_target):
                self.target = p_target

            def main_iteration(self):
                self.target._response = Gtk.ResponseType.APPLY

        patch_iter = PatchMainIteration(p_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert isinstance(result, XSEGINT.SegInt)
        assert NAME == result.name
        assert SUMMARY == result.summary
        assert TITLE == result.title
        assert BOUND == len(result._elements)

    def test_call_cancel(self, patch_args_spec, monkeypatch):
        """| Confirm call method specifies segment topic.
        | Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))

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

    @pytest.mark.parametrize('TITLE_PAGE', [
        'New Segment',
        'Bound',
        'Identify',
        'Confirm',
        'Missing',
        ])
    def test_on_prepare(
            self, monkeypatch, TITLE_PAGE, patch_args_spec, patch_ui_args):
        """Confirm prepare signal dispatch by page title."""
        # Setup
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        BOUND = 1
        UIARGS = patch_ui_args
        UIARGS.ui_bound.set_value(BOUND)
        # Test
        target.on_prepare(assistant, page, UIARGS)
        # Call success is adequate. Changes checked in other tests.
        # Teardown
        del assistant

    def test_prepare_confirm(
            self, monkeypatch, patch_args_spec, patch_ui_args):
        """| Confirm prepare signal processing.
        | Case: Confirm page.
        """
        # Setup
        TITLE_PAGE = 'Confirm'
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        UIARGS = patch_ui_args
        bound = UIARGS.ui_bound.get_value_as_int()
        text_segment = '<b>Segment: </b>[0, {})'.format(bound)
        # Test
        target.on_prepare(assistant, page, UIARGS)
        assert text_segment == UIARGS.ui_segment.get_label()
        # Teardown
        del assistant

    @pytest.mark.parametrize('BOUND, NAME, SUMMARY, TITLE', [
        (1, 'N(1)', 'The set is initial segment of natural numbers '
         '[0, 1) (that is, {0}).', 'Set of integers [0, 1)'),
        (2, 'N(2)', 'The set is initial segment of natural numbers '
         '[0, 2) (that is, {0, 1}).', 'Set of integers [0, 2)'),
        (3, 'N(3)', 'The set is initial segment of natural numbers '
         '[0, 3) (that is, {0, 1, 2}).', 'Set of integers [0, 3)'),
        (42, 'N(42)', 'The set is initial segment of natural numbers '
         '[0, 42) (that is, {0, 1, ..., 41}).', 'Set of integers [0, 42)'),
        ])
    def test_on_prepare_identify(self, BOUND, NAME, SUMMARY, TITLE,
                                 monkeypatch, patch_args_spec, patch_ui_args):
        """| Confirm prepare signal processing.
        | Case: Identify page.
        """
        # Setup
        TITLE_PAGE = 'Identify'
        monkeypatch.setattr(
            Gtk.Assistant, 'get_page_title', lambda _self, _page: TITLE_PAGE)

        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assistant = Gtk.Assistant()
        page = Gtk.Label()
        assistant.append_page(page)
        UIARGS = patch_ui_args
        UIARGS.ui_bound.set_value(BOUND)
        # Test
        target.on_prepare(assistant, page, UIARGS)
        assert assistant.get_page_complete(page)

        assert NAME == UIARGS.ui_name.get_text()
        assert SUMMARY == XSPEC.textbuffer_get_text(UIARGS.ui_summary)
        assert TITLE == UIARGS.ui_title.get_text()
        # Teardown
        del assistant
