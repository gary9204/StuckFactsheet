"""
Unit test for template class to specify a topic for user notes.  See
:mod:`~.spec_note`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]
import typing

from factsheet.content import spec as XSPEC
from factsheet.content.note import spec_note as XSPEC_NOTE
from factsheet.content.note import topic_note as XNOTE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class ArgsSpec:
    """Convenience class for assembling arguments to
    :class:`.SpecNote` method ``__init__``.
    """
    p_name: str
    p_summary: str
    p_title: str
    p_path_assist: XSPEC.StrAssist
    p_attach_view_topics: typing.Optional[typing.Callable]


@pytest.fixture
def patch_args_spec():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SpecNote` object.
    """
    return ArgsSpec(
        p_name='Inquisition',
        p_summary='No one expects the Spanish Inquisition!',
        p_title='The Spanish Inquisition',
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_NOTE.__file__).parent / 'spec_note.ui')),
        p_attach_view_topics=None
        )


class TestSpecNote:
    """Unit tests for :class:`.SpecNote`."""

#     def test_init(self, patch_args_spec):
#         """Confirm initialization."""
#         # Setup
#         ARGS = patch_args_spec
#         # Test
#         target = XSPEC_NOTE.SpecNote(**DC.asdict(ARGS))
#         assert ARGS.p_name == target._name_template
#         assert ARGS.p_summary == target._summary_template
#         assert ARGS.p_title == target._title_template
#         assert target._response is None
#
#         assert ARGS.p_path_assist == target._path_assist
#         assert target._class_topic is XNOTE.Note

#     @pytest.mark.parametrize(
#         'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
#             # ('apply', '_assistant', Gtk.Assistant, 0),
#             # ('cancel', '_assistant', Gtk.Assistant, 0),
#             # ('destroy', '_assistant', Gtk.Assistant, 0),
#             # ('prepare', '_assistant', Gtk.Assistant, 0),
#             ])
#     def test_init_signals(self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN,
#                           N_DEFAULT, patch_args_spec):
#         """Confirm initialization of signal connections."""
#         # Setup
#         origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
#         signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
#         ARGS = patch_args_spec
#         # Test
#         target = XSPEC_NOTE.SpecNote(**DC.asdict(ARGS))

#         attribute = getattr(target, NAME_ATTRIBUTE)
#         n_handlers = 0
#         while True:
#             id_signal = GO.signal_handler_find(
#                 attribute, GO.SignalMatchType.ID, signal,
#                 0, None, None, None)
#             if 0 == id_signal:
#                 break

#             n_handlers += 1
#             GO.signal_handler_disconnect(attribute, id_signal)

#         assert N_DEFAULT + 1 == n_handlers

    def test_on_apply(self, patch_args_spec):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=XNOTE.Note)
        target = XSPEC_NOTE.SpecNote(
            **DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        assistant = Gtk.Assistant()
        assistant.show()
        # Test
        target.on_apply(assistant)
        assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.APPLY
        # Teardown
        del assistant

    def test_on_cancel(self, patch_args_spec):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=XNOTE.Note)
        target = XSPEC_NOTE.SpecNote(
            **DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        assistant = Gtk.Assistant()
        assistant.show()
        # Test
        target.on_cancel(assistant)
        assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.CANCEL
        # Teardown
        del assistant

        # def test_on_prepare(self, patch_args_spec):
        #     """Confirm no-op handler exists."""
        #     # Setup
        #     ARGS = patch_args_spec
        #     target = XSPEC_NOTE.SpecNote(**DC.asdict(ARGS))
        #     assistant = Gtk.Assistant()
        #     assistant.show()
        #     # Test
        #     target.on_prepare(assistant, None)
        #     # Teardown
        #     del assistant

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
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=XNOTE.Note)
        target = XSPEC_NOTE.SpecNote(
            **DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        value_attr = getattr(target, name_attr)
        target_prop = getattr(XSPEC_NOTE.SpecNote, name_prop)
        value_prop = getattr(target, name_prop)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_call_apply(self, patch_args_spec, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user completes assistant.
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=XNOTE.Note)
        target = XSPEC_NOTE.SpecNote(
            **DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        # Sync identification information with spec_note.ui.
        NAME = ''
        SUMMARY = ''
        TITLE = ''

        class PatchMainIteration:
            def __init__(self, px_target):
                self.target = px_target

            def main_iteration(self):
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

    def test_call_cancel(self, patch_args_spec, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=XNOTE.Note)
        target = XSPEC_NOTE.SpecNote(
            **DC.asdict(ARGS), p_prototopic=PROTOTOPIC)

        class PatchMainIteration:
            def __init__(self, px_target):
                self.target = px_target

            def main_iteration(self):
                self.target._response = Gtk.ResponseType.CANCEL

        patch_iter = PatchMainIteration(px_target=target)
        monkeypatch.setattr(
            Gtk, 'main_iteration', patch_iter.main_iteration)
        # Test
        result = target()
        assert result is None
