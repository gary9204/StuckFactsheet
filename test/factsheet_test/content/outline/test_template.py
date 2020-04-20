"""
Unit test for template class to create a section in a factsheet topic
outline.  See :mod:`.template`.
"""
import collections as COL
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.content.outline import template as TEMPLATE
from factsheet.content.outline import topic as TOPIC

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


#: Container for clear and convenient reference to stock argument values.
ArgsSection = COL.namedtuple(
    'ArgsSection', 'name summary title path_assist model')


@pytest.fixture
def patch_args_section():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.Section` object."""
    return ArgsSection(
        name='Inquisition',
        summary='No one expects the Spanish Inquisition!',
        title='The Spanish Inquisition',
        path_assist=str(Path(TEMPLATE.__file__).parent / 'assistant.ui'),
        model=TOPIC.Topic
        )


class TestSection:
    """Unit tests for :class:`.Section`."""

    def test_init(self, patch_args_section):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_section
        # Test
        target = TEMPLATE.Section(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        assert ARGS.name == target._name_template
        assert ARGS.summary == target._summary_template
        assert ARGS.title == target._title_template

        assert target._response is None
        assert target._model_topic is TOPIC.Topic

        assert isinstance(target._assistant, Gtk.Assistant)
        assert isinstance(target._summary_topic, Gtk.TextBuffer)
        assert isinstance(target._name_topic, Gtk.EntryBuffer)
        assert isinstance(target._title_topic, Gtk.EntryBuffer)
        # Teardown
        target._assistant.destroy()
        del target._assistant

    @pytest.mark.parametrize(
        'name_signal, name_attribute, origin, n_default', [
            ('apply', '_assistant', Gtk.Assistant, 0),
            ('cancel', '_assistant', Gtk.Assistant, 0),
            ('destroy', '_assistant', Gtk.Assistant, 0),
            ('prepare', '_assistant', Gtk.Assistant, 0),
            ])
    def test_init_signals(self, name_signal, name_attribute, origin,
                          n_default, patch_args_section):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(origin))
        signal = GO.signal_lookup(name_signal, origin_gtype)
        ARGS = patch_args_section
        # Test
        target = TEMPLATE.Section(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)

        attribute = getattr(target, name_attribute)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert n_default + 1 == n_handlers
        # Teardown
        target._assistant.destroy()
        del target._assistant

    def test_on_apply(self, patch_args_section):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
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

    def test_on_cancel(self, patch_args_section):
        """Confirm assistant hidden, response set, and call method
        unblocked.
        """
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
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

    def test_on_prepare(self, patch_args_section):
        """Confirm no-op handler exists."""
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
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
    def test_property(self, patch_args_section, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title,
            p_path_assist=ARGS.path_assist, p_model=ARGS.model)
        value_attr = getattr(target, name_attr)
        target_prop = getattr(TEMPLATE.Section, name_prop)
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

    def test_call_apply(self, patch_args_section, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user completes assistant.
        """
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
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
        assert isinstance(result, TOPIC.Topic)
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

    def test_call_cancel(self, patch_args_section, monkeypatch):
        """Confirm call method specifies a topic.

        Case: user cancels assistant.
        """
        # Setup
        ARGS = patch_args_section
        target = TEMPLATE.Section(
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
