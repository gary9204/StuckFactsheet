"""
Unit tests for class that mediates topic-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.

See :mod:`~.control.topic`.
"""
from factsheet.control import topic as CTOPIC
from factsheet.content.section import section_topic as MTOPIC


class TestTopic:
    """Unit tests for :class:`~.control.topic.Topic`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = CTOPIC.Topic()
        assert target._model is None

    def test_attach_view(self, monkeypatch):
        """Confirm view addition."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_attach_view = False

            def attach_view(self, _view):
                self.called_attach_view = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MTOPIC.Topic, 'attach_view', patch_model.attach_view)

        target = CTOPIC.Topic.new()
        # Test
        target.attach_view(None)
        assert patch_model.called_attach_view

    def test_detach_view(self, monkeypatch):
        """Confirm page removal."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_detach_view = False

            def detach_view(self, _view):
                self.called_detach_view = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MTOPIC.Topic, 'detach_view', patch_model.detach_view)

        target = CTOPIC.Topic.new()
        # Test
        target.detach_view(None)
        assert patch_model.called_detach_view

    def test_new(self):
        """Confirm control creation with default model."""
        # Setup
        # Test
        target = CTOPIC.Topic.new()
        assert isinstance(target, CTOPIC.Topic)
        assert isinstance(target._model, MTOPIC.Topic)

    def test_open(self):
        """Confirm control creation with model."""
        # Setup
        TITLE = 'Parrot Sketch'
        model = MTOPIC.Topic(p_title=TITLE)
        # Test
        target = CTOPIC.Topic.open(pm_model=model)
        assert isinstance(target, CTOPIC.Topic)
        assert target._model is model
