"""
Unit tests for class that mediates topic-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_topic`.
"""
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_topic as CTOPIC
import factsheet.model.topic as MTOPIC


class TestTopic:
    """Unit tests for :class:`~.control_topic.ControlTopic`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TOPIC = MTOPIC.Topic()
        # facts = list(TOPIC.facts())
        # Test
        target = CTOPIC.ControlTopic(TOPIC)
        assert target._topic is TOPIC
        # assert isinstance(target._controls_fact, dict)
        # assert len(facts) == len(target._controls_fact)
        # for fact in facts:
        #     assert target._controls_fact[fact.tag]._fact is fact

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP, HAS_SETTER', [
        ('_topic', 'topic', False),
        ('_topic', 'idcore', False),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP, HAS_SETTER):
        """Confirm values and access limits of properties."""
        # Setup
        TOPIC = MTOPIC.Topic()
        target = CTOPIC.ControlTopic(p_topic=TOPIC)
        target_prop = getattr(CTOPIC.ControlTopic, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        REPLACE = MTOPIC.Topic()
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        if HAS_SETTER:
            target_prop.fset(target, REPLACE)
            value_attr = getattr(target, NAME_ATTR)
            assert value_attr is REPLACE
        else:
            assert target_prop.fset is None
        assert target_prop.fdel is None

    # def test_attach_form(self, monkeypatch):
    #     """Confirm topic form addition."""
    #     # Setup
    #     class PatchModel:
    #         def __init__(self):
    #             self.called_attach_form = False

    #         def attach_form(self, _form):
    #             self.called_attach_form = True

    #     patch_model = PatchModel()
    #     monkeypatch.setattr(
    #         MTOPIC.Topic, 'attach_form', patch_model.attach_form)

    #     TOPIC = factory_topic()
    #     target = CTOPIC.ControlTopic(TOPIC)
    #     # Test
    #     target.attach_form(None)
    #     assert patch_model.called_attach_form

    # def test_detach_form(self, monkeypatch):
    #     """Confirm topic form removal."""
    #     # Setup
    #     class PatchModel:
    #         def __init__(self):
    #             self.called_detach_form = False

    #         def detach_form(self, _form):
    #             self.called_detach_form = True

    #     patch_model = PatchModel()
    #     monkeypatch.setattr(
    #         MTOPIC.Topic, 'detach_form', patch_model.detach_form)

    #     TOPIC = factory_topic()
    #     target = CTOPIC.ControlTopic(TOPIC)
    #     # Test
    #     target.detach_form(None)
    #     assert patch_model.called_detach_form


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_topic`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (CTOPIC.ViewNameTopic, BUI.ViewTextMarkup),
        (CTOPIC.ViewSummaryTopic, BUI.ViewTextFormat),
        (CTOPIC.ViewTitleTopic, BUI.ViewTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
