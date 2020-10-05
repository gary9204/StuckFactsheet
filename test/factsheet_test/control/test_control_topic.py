"""
Unit tests for class that mediates topic-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_topic`.
"""
from factsheet.control import control_topic as CTOPIC
from factsheet.model import topic as MTOPIC


class TestTopic:
    """Unit tests for :class:`~.control_topic.ControlTopic`."""

    def test_init(self, factory_topic):
        """Confirm initialization."""
        # Setup
        TOPIC = factory_topic()
        facts = list(TOPIC.facts())
        # Test
        target = CTOPIC.ControlTopic(TOPIC)
        assert target._topic is TOPIC
        assert isinstance(target._controls_fact, dict)
        assert len(facts) == len(target._controls_fact)
        for fact in facts:
            assert target._controls_fact[fact.tag]._fact is fact

    def test_attach_form(self, monkeypatch, factory_topic):
        """Confirm topic form addition."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_attach_form = False

            def attach_form(self, _form):
                self.called_attach_form = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MTOPIC.Topic, 'attach_form', patch_model.attach_form)

        TOPIC = factory_topic()
        target = CTOPIC.ControlTopic(TOPIC)
        # Test
        target.attach_form(None)
        assert patch_model.called_attach_form

    def test_detach_form(self, monkeypatch, factory_topic):
        """Confirm topic form removal."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_detach_form = False

            def detach_form(self, _form):
                self.called_detach_form = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MTOPIC.Topic, 'detach_form', patch_model.detach_form)

        TOPIC = factory_topic()
        target = CTOPIC.ControlTopic(TOPIC)
        # Test
        target.detach_form(None)
        assert patch_model.called_detach_form
