"""
Unit tests for GTK-specific ancestor furo template classes.  See
:mod:`.spec`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

# import factsheet.content.spec as XSPEC
import factsheet.model.fact as MFACT
import factsheet.model.topic as MTOPIC
import factsheet.view.block.block_fact as VFACT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@DC.dataclass
class ArgsSpec:
    """Convenience class for pytest fixture.

    Class assembles arguments to :class:`.Spec` method ``__init__``.
    """
    p_name: str
    p_summary: str
    p_title: str
    p_path_assist: XSPEC.StrAssist
    p_attach_view_topics: typing.Callable


@pytest.fixture
def patch_args_spec():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.Spec` object.
    """
    return ArgsSpec(
        p_name='Inquisition',
        p_summary='No one expects the Spanish Inquisition!',
        p_title='The Spanish Inquisition',
        p_path_assist=XSPEC.StrAssist('/path/to/parrot'),
        p_attach_view_topics=lambda _self: None,
        )


class TestTypes:
    """Unit test for module type."""
    # Setup
    # Test
    assert XSPEC.StrAssist is not None
    target = XSPEC.StrAssist('Parrot')
    assert isinstance(target, str)


class TestProtoFact:
    """Unit tests for :class:`.ProtoFact`."""

    def test_init(self):
        """Confirm initialization.

        #. Case: default prerequisites.
        #. Case: explicit prerequisites.
        """
        # Setup
        FACT = MFACT.Fact[typing.Any, typing.Any]
        BLOCK = VFACT.BlockFact[typing.Any]
        PREREQS = ['Brie', 'Cheddar', 'Provolone', 'Stilton']
        # Test: default prerequisites.
        target = XSPEC.ProtoFact(class_fact=FACT, class_block=BLOCK)
        assert target.class_fact is FACT
        assert target.class_block is BLOCK
        assert list() == target.prereqs
        # Test: explicit prerequisites.
        target = XSPEC.ProtoFact(
            class_fact=FACT, class_block=BLOCK, prereqs=PREREQS)
        assert PREREQS == target.prereqs


class TestProtoTopic:
    """Unit tests for :class:`.ProtoTopic`."""

    def test_init(self):
        """Confirm initialization.

        #. Case: default providers.
        #. Case: explicit providers.
        """
        # Setup
        TOPIC = MTOPIC.Topic()
        N_PROVIDERS = 4
        PROVIDERS = [MTOPIC.Topic for _ in range(N_PROVIDERS)]
        # Test: default prerequisites.
        target = XSPEC.ProtoTopic(class_topic=TOPIC)
        assert target.class_topic is TOPIC
        assert list() == target.classes_provider
        # Test: explicit prerequisites.
        target = XSPEC.ProtoTopic(
            class_topic=TOPIC, classes_provider=PROVIDERS)
        assert PROVIDERS == target.classes_provider


class TestSpec:
    """Unit tests for :class:`.Spec`."""

    def test_call(self, patch_args_spec):
        """Confirm call method specifies a topic."""
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        # Test
        assert target() is None

    def test_init(self, patch_args_spec):
        """| Confirm initialization.
        | Case: nominal arguments
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        # Test
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        assert ARGS.p_name == target._name_template
        assert ARGS.p_summary == target._summary_template
        assert ARGS.p_title == target._title_template

        assert target._path_assist == ARGS.p_path_assist
        assert target._attach_view_topics is ARGS.p_attach_view_topics
        assert target._prototopic is PROTOTOPIC.class_topic

        assert isinstance(target._protofacts, list)
        assert not target._protofacts
        assert isinstance(target._fact_to_block, VFACT.MapFactToBlock)
        assert target._response is None

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_name_template', 'name'],
        ['_summary_template', 'summary'],
        ['_title_template', 'title'],
        ])
    def test_property(self, patch_args_spec, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(XSPEC.Spec, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

        # def test_set_view_topics(self, patch_args_spec):
        #     """Confirm no-op method exists."""
        #     # Setup
        #     ARGS = patch_args_spec
        #     target = XSPEC.Spec(**DC.asdict(ARGS))
        #     # Test
        #     target.set_view_topics(None)

    def test_on_apply(self, patch_args_spec):
        """Confirm assistant hiddenand response set."""
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        assistant = Gtk.Assistant()
        assistant.show()
        # Test
        target.on_apply(assistant)
        assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.APPLY

    def test_on_cancel(self, patch_args_spec):
        """Confirm assistant hidden and response set."""
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        assistant = Gtk.Assistant()
        assistant.show()
        # Test
        target.on_cancel(assistant)
        assert not assistant.get_visible()
        assert target._response is Gtk.ResponseType.CANCEL

    def test_add_protofact(self, patch_args_spec):
        """Confirm addition of fact prototype."""
        # Setup
        ARGS = patch_args_spec
        PROTOTOPIC = XSPEC.ProtoTopic(class_topic=MTOPIC.Topic)
        target = XSPEC.Spec(**DC.asdict(ARGS), p_prototopic=PROTOTOPIC)
        SIZE = 5
        classes_fact = [MFACT.Fact for _ in range(SIZE)]
        blocks_fact = [VFACT.BlockFact for _ in range(SIZE)]
        protofacts = [XSPEC.ProtoFact(classes_fact[i], blocks_fact[i])
                      for i in range(SIZE)]
        # Test
        for pf in protofacts:
            target.add_protofact(pf)
        assert protofacts == target._protofacts

        # def test_on_prepare(self, patch_args_spec):
        #     """Confirm no-op handler exists."""
        #     # Setup
        #     ARGS = patch_args_spec
        #     target = XSPEC.Spec(**DC.asdict(ARGS))
        #     # Test
        #     target.on_prepare(None, None)


class TestGtkSpec:
    """Unit test for :func:`.textbuffer_get_text`."""

    def test_textbuffer_get_text(self):
        """ """
        # Setup
        ALL = -1
        BLANK = ''
        TEXT = "Something completely different."
        target = Gtk.TextBuffer()
        # Test
        assert BLANK == XSPEC.textbuffer_get_text(target)
        target.set_text(TEXT, ALL)
        assert TEXT == XSPEC.textbuffer_get_text(target)
