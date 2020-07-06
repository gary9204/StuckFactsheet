"""
Unit test for template class to specify a topic for user notes.  See
:mod:`~.note_spec`.
"""
import collections as COL
import dataclasses as DC
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]
import typing

from factsheet.content.note import note_spec as XNOTE_SPEC
from factsheet.content.note import note_topic as XNOTE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class ArgsSpec:
    """Convenience class for assembling arguments to
    :class:`.SpecNote` method ``__init__``.
    """
    name: str
    summary: str
    title: str
    path_assist: str
    model: typing.Type[XNOTE.Note]


# #: Container for clear and convenient reference to stock argument values.
# ArgsNote = COL.namedtuple(
#     'ArgsNote', 'name summary title path_assist model')


@pytest.fixture
def patch_args_spec():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SpecNote` object.
    """
    return ArgsSpec(
        name='Inquisition',
        summary='No one expects the Spanish Inquisition!',
        title='The Spanish Inquisition',
        path_assist=str(Path(XNOTE_SPEC.__file__).parent / 'note_spec.ui'),
        model=XNOTE.Note
        )


class TestSpecNote:
    """Unit tests for :class:`.SpecNote`."""

    def test_init(self, patch_args_spec):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_spec
        # Test
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        assert ARGS.name == target._name_template
        assert ARGS.summary == target._summary_template
        assert ARGS.title == target._title_template

        assert target._response is None
        assert target._model_topic is XNOTE.Note

        assert isinstance(target._assistant, Gtk.Assistant)
        assert target._assistant.get_modal()
        assert isinstance(target._summary_topic, Gtk.TextBuffer)
        assert isinstance(target._name_topic, Gtk.EntryBuffer)
        assert isinstance(target._title_topic, Gtk.EntryBuffer)
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
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)

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

    def test_on_apply(self, patch_args_spec):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_spec
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
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
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        target._assistant.show()
        # Test
        target.on_cancel(None)
        assert not target._assistant.get_visible()
        assert target._response is Gtk.ResponseType.CANCEL
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_prepare(self, patch_args_spec):
        """Confirm no-op handler exists."""
        # Setup
        ARGS = patch_args_spec
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        target._assistant.show()
        # Test
        target.on_prepare(None, None)
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
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        value_attr = getattr(target, name_attr)
        target_prop = getattr(XNOTE_SPEC.SpecNote, name_prop)
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

    def test_call_apply(self, patch_args_spec, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user completes assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        ALL = -1
        BLANK = ''

        class PatchMainIteration:
            def __init__(self, px_target):
                self.target = px_target

            def main_iteration(self):
                self.target._name_topic.set_text(NAME, ALL)
                self.target._summary_topic.set_text(SUMMARY, ALL)
                self.target._title_topic.set_text(TITLE, ALL)
                self.target._response = Gtk.ResponseType.APPLY

        patch_iter = PatchMainIteration(px_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert isinstance(result, XNOTE.Note)
        assert NAME == result._infoid.name
        assert SUMMARY == result._infoid.summary
        assert TITLE == result._infoid.title

        assert target._response is None
        assert BLANK == target._name_topic.get_text()
        start, end = target._summary_topic.get_bounds()
        INCLUDE_HIDDEN = True
        summary = target._summary_topic.get_text(start, end, INCLUDE_HIDDEN)
        assert BLANK == summary
        assert BLANK == target._title_topic.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_call_cancel(self, patch_args_spec, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_spec
        target = XNOTE_SPEC.SpecNote(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        ALL = -1
        BLANK = ''

        class PatchMainIteration:
            def __init__(self, px_target):
                self.target = px_target

            def main_iteration(self):
                self.target._name_topic.set_text(NAME, ALL)
                self.target._summary_topic.set_text(SUMMARY, ALL)
                self.target._title_topic.set_text(TITLE, ALL)
                self.target._response = Gtk.ResponseType.CANCEL

        patch_iter = PatchMainIteration(px_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert result is None

        assert BLANK == target._name_topic.get_text()
        start, end = target._summary_topic.get_bounds()
        INCLUDE_HIDDEN = True
        summary = target._summary_topic.get_text(start, end, INCLUDE_HIDDEN)
        assert BLANK == summary
        assert BLANK == target._title_topic.get_text()
        # Teardown
        target._assistant.destroy()
        del target._assistant
