"""
Unit test for class to specify an initial segment of natural numbers.
See :mod:`~.segint_spec`.
"""
import collections as COL
import dataclasses as DC
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]
import typing

from factsheet.content import gtk_helper as XHELPER
from factsheet.content.sets.int import segint_spec as XSPEC_SEGINT
from factsheet.content.sets.int import segint_topic as XSEGINT

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass(frozen=True)
class ArgsSpec:
    """Convenience class for assembling arguments to
    :method:`.SpecSegInt.__init__`.
    """
    p_name: str
    p_summary: str
    p_title: str
    p_path_assist: str
    p_model: typing.Type[XSEGINT.SegInt]


@pytest.fixture
def patch_args_spec():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SpecSegInt` object."""
    return ArgsSpec(
        p_name='Inquisition',
        p_summary='No one expects the Spanish Inquisition!',
        p_title='The Spanish Inquisition',
        p_path_assist=str(Path(XSPEC_SEGINT.__file__).parent /
                          'segint_spec.ui'),
        p_model=XSEGINT.SegInt
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

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        BOUND = 5
        ALL = -1
        BLANK = ''

        class PatchMainIteration:
            def __init__(self, p_target):
                self.target = p_target

            def main_iteration(self):
                self.target._name_topic.set_text(NAME, ALL)
                self.target._summary_topic.set_text(SUMMARY, ALL)
                self.target._title_topic.set_text(TITLE, ALL)
                self.target._bound.set_value(BOUND)
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
        assert BOUND == len(result._scope)

        assert target._response is None
        assert BLANK == target._name_topic.get_text()
        assert BLANK == XHELPER.textbuffer_get_text(target._summary_topic)
        assert BLANK == target._title_topic.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_call_cancel(self, patch_args_spec, monkeypatch):
        """| Confirm call method specifies segment topic.
        | Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        ALL = -1
        BLANK = ''

        class PatchMainIteration:
            def __init__(self, p_target):
                self.target = p_target

            def main_iteration(self):
                self.target._name_topic.set_text(NAME, ALL)
                self.target._summary_topic.set_text(SUMMARY, ALL)
                self.target._title_topic.set_text(TITLE, ALL)
                self.target._response = Gtk.ResponseType.CANCEL

        patch_iter = PatchMainIteration(p_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert result is None

        assert target._response is None
        assert BLANK == target._name_topic.get_text()
        assert BLANK == XHELPER.textbuffer_get_text(target._summary_topic)
        assert BLANK == target._title_topic.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_init(self, patch_args_spec):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_spec
        BOUND = 1
        # Test
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assert ARGS.p_name == target._name_template
        assert ARGS.p_summary == target._summary_template
        assert ARGS.p_title == target._title_template

        assert target._model_topic is ARGS.p_model
        assert isinstance(target._name_topic, Gtk.EntryBuffer)
        assert isinstance(target._summary_topic, Gtk.TextBuffer)
        assert isinstance(target._title_topic, Gtk.EntryBuffer)
        assert isinstance(target._bound, Gtk.SpinButton)
        assert BOUND == target._bound.get_value_as_int()
        assert isinstance(target._segment, Gtk.Label)

        assert isinstance(target._assistant, Gtk.Assistant)
        assert target._assistant.get_modal()

        assert target._response is None
        # Teardown
        target._assistant.destroy()
        del target._assistant

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('apply', '_assistant', Gtk.Assistant, 0),
            ('cancel', '_assistant', Gtk.Assistant, 0),
            ('destroy', '_assistant', Gtk.Assistant, 0),
            ('prepare', '_assistant', Gtk.Assistant, 0),
            ])
    def test_init_signals(self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN,
                          N_DEFAULT, patch_args_spec):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        ARGS = patch_args_spec
        # Test
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))

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
        target._assistant.destroy()
        del target._assistant

    @pytest.mark.parametrize('name_attr, name_prop', [
        ['_name_template', 'name'],
        ['_summary_template', 'summary'],
        ['_title_template', 'title'],
        ])
    def test_property(self, patch_args_spec, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        value_attr = getattr(target, name_attr)
        target_prop = getattr(XSPEC_SEGINT.SpecSegInt, name_prop)
        value_prop = getattr(target, name_prop)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_clear_assist(self, patch_args_spec):
        """Confirm clearing of assistant contents."""
        # Setup
        ARGS = patch_args_spec
        BOUND = 42
        BOUND_DEFAULT = 1
        BLANK = ''
        TEXT = 'Oops'
        ALL = -1
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        target._name_topic.set_text(TEXT, ALL)
        target._summary_topic.set_text(TEXT, ALL)
        target._title_topic.set_text(TEXT, ALL)
        target._bound.set_value(BOUND)
        target._response = TEXT
        # Test
        target._clear_assist()
        assert BLANK == target._name_topic.get_text()
        assert BLANK == XHELPER.textbuffer_get_text(target._summary_topic)
        assert BLANK == target._title_topic.get_text()
        assert BOUND_DEFAULT == target._bound.get_value_as_int()
        assert target._response is None
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_apply(self, patch_args_spec):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        target._assistant.show()
        # Test
        target.on_apply(None)
        assert not target._assistant.get_visible()
        assert target._response is Gtk.ResponseType.APPLY
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_cancel(self, patch_args_spec):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        target._assistant.show()
        # Test
        target.on_cancel(None)
        assert not target._assistant.get_visible()
        assert target._response is Gtk.ResponseType.CANCEL
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_prepare_intro(self, patch_args_spec):
        """| Confirm prepare signal processing.
        | Case: Intro page.
        """
        # Setup
        N_INTRO = 0
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assistant = target._assistant
        page_intro = assistant.get_nth_page(N_INTRO)
        # Test
        target.on_prepare(assistant, page_intro)
        # Intro page does not change application state. No other checks.
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_prepare_bound(self, patch_args_spec):
        """| Confirm prepare signal processing.
        | Case: Bound page.
        """
        # Setup
        # Setup
        N_BOUND = 1
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        assistant = target._assistant
        page_bound = assistant.get_nth_page(N_BOUND)
        # Test
        target.on_prepare(assistant, page_bound)
        # Bound page does not change application state. No other checks.
        # Teardown
        target._assistant.destroy()
        del target._assistant

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
    def test_on_prepare_identify(
            self, patch_args_spec, BOUND, NAME, SUMMARY, TITLE):
        """| Confirm prepare signal processing.
        | Case: Identify page.
        """
        # Setup
        N_IDENTIFY = 2
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        target._bound.set_value(BOUND)

        assistant = target._assistant
        page_identify = assistant.get_nth_page(N_IDENTIFY)
        assistant.set_page_complete(page_identify, False)
        # Test
        target.on_prepare(assistant, page_identify)
        assert assistant.get_page_complete(page_identify)

        assert NAME == target._name_topic.get_text()
        assert SUMMARY == XHELPER.textbuffer_get_text(target._summary_topic)
        assert TITLE == target._title_topic.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_prepare_confirm(self, patch_args_spec):
        """| Confirm prepare signal processing.
        | Case: Confirm page.
        """
        # Setup
        N_CONFIRM = 3
        ARGS = patch_args_spec
        target = XSPEC_SEGINT.SpecSegInt(**DC.asdict(ARGS))
        BOUND = 42
        text_label = 'Segment: [0, {})'.format(BOUND)
        target._bound.set_value(BOUND)
        assistant = target._assistant
        page_confirm = assistant.get_nth_page(N_CONFIRM)
        # Test
        target.on_prepare(assistant, page_confirm)
        assert text_label == target._segment.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant
