"""
Unit tests for class that mediates topic-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_topic`.
"""
from factsheet.control import control_topic as CTOPIC
from factsheet.model import topic as MTOPIC


class TestTopic:
    """Unit tests for :class:`~.control_topic.ControlTopic`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = 'Parrot'
        MODEL = MTOPIC.Topic(p_name=NAME)
        # Test
        target = CTOPIC.ControlTopic(MODEL)
        assert target._model is MODEL

    def test_attach_form(self, monkeypatch):
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

        NAME = 'Parrot'
        MODEL = MTOPIC.Topic(p_name=NAME)
        target = CTOPIC.ControlTopic(MODEL)
        # Test
        target.attach_form(None)
        assert patch_model.called_attach_form

    def test_detach_form(self, monkeypatch):
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

        NAME = 'Parrot'
        MODEL = MTOPIC.Topic(p_name=NAME)
        target = CTOPIC.ControlTopic(MODEL)
        # Test
        target.detach_form(None)
        assert patch_model.called_detach_form

#     def test_new(self):
#         """Confirm control creation with default model."""
#         # Setup
#         # Test
#         target = CTOPIC.ControlTopic.new()
#         assert isinstance(target, CTOPIC.ControlTopic)
#         assert isinstance(target._model, MTOPIC.Topic)

#     def test_open(self):
#         """Confirm control creation with model."""
#         # Setup
#         TITLE = 'Parrot Sketch'
#         model = MTOPIC.Topic(p_title=TITLE)
#         # Test
#         target = CTOPIC.ControlTopic.open(p_model=model)
#         assert isinstance(target, CTOPIC.ControlTopic)
#         assert target._model is model
