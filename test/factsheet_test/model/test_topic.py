"""
Unit tests for topic-level model. See :mod:`~.topic`.
"""
# import dataclasses as DC
# import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
# import re as RE

import factsheet.bridge_ui as BUI
# import factsheet.model.fact as MFACT
import factsheet.model.topic as MTOPIC


class TestTopic:
    pass
    """Unit tests for :class:`.Topic`."""

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: identity difference.
        #. Case: Fact collection diffrence.
        #. Case: Equivalence
        """
        # Setup
        source = MTOPIC.Topic()
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        TEXT = 'Something completely different'
        # Test: type difference
        assert not source.__eq__(TITLE)
        # Test: identity difference
        target = MTOPIC.Topic()
        target.title.text = TEXT
        assert not source.__eq__(target)
        # # Test: Fact collection diffrence
        # target = factory_topic()
        # fact = PatchFact(p_topic=target)
        # target.insert_fact_before(fact, None)
        # assert not source.__eq__(target)
        # Test: Equivalence
        target = MTOPIC.Topic()
        target._stale = True
        target.title.text = TITLE
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        source = MTOPIC.Topic()
        NAME = 'Parrot'
        source.name.text = NAME
        SUMMARY = 'The parrot is a Norwegian Blue.'
        source.summary.text = SUMMARY
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        source._stale = True
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert not target._stale
        assert source._tag != target._tag
        assert source == target

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        # Test
        target = MTOPIC.Topic()
        assert not target._stale
        assert isinstance(target._name, MTOPIC.NameTopic)
        assert isinstance(target._summary, MTOPIC.SummaryTopic)
        assert isinstance(target._tag, int)
        assert id(target) == target._tag
        assert isinstance(target._title, MTOPIC.TitleTopic)
    #     assert isinstance(target._facts, MTYPES.OutlineFacts)
    #     target_facts = [target._facts.get_item(i)
    #                     for i in target._facts.indices()]
    #     assert not target_facts

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_name', 'name'),
        ('_summary', 'summary'),
        ('_tag', 'tag'),
        ('_title', 'title'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm values and access limits of properties."""
        # Setup
        target = MTOPIC.Topic()
        target_prop = getattr(MTOPIC.Topic, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.skip
    def test_check_fact(self, patch_class_fact, factory_topic):
        """Confirm fact check."""
        # Setup
        pass
    #     PatchFact = patch_class_fact
    #     target = factory_topic()
    #     I_LEAF = 2
    #     index = list(target._facts.indices())[I_LEAF]
    #     fact = target._facts.get_item(index)
    #     target.set_fresh()
    #     # Test
    #     target.check_fact(index)
    #     assert target.is_stale()
    #     assert PatchFact.VALUE == fact()
    #     assert fact.status is MFACT.StatusOfFact.DEFINED

    @pytest.mark.skip
    def test_clear_all(self, factory_topic):
        """Confirm fact check."""
        # Setup
        pass
    #     target = factory_topic()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         _ = fact.check()
    #     target.set_fresh()
    #     # Test
    #     target.clear_all()
    #     assert target.is_stale()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         assert fact() is None
    #         assert fact.status is MFACT.StatusOfFact.UNCHECKED

    @pytest.mark.skip
    def test_clear_fact(self, factory_topic):
        """Confirm fact clear."""
        # Setup
        pass
    #     target = factory_topic()
    #     I_LEAF = 2
    #     index = list(target._facts.indices())[I_LEAF]
    #     fact = target._facts.get_item(index)
    #     _ = fact.check()
    #     target.set_fresh()
    #     # Test
    #     target.clear_fact(index)
    #     assert target.is_stale()
    #     assert fact() is None
    #     assert fact.status is MFACT.StatusOfFact.UNCHECKED

    @pytest.mark.skip
    def test_facts(self, factory_topic):
        """Confirm iterator over fact."""
        # Setup
        pass
    #     target = factory_topic()
    #     # Test
    #     for fact, index in zip(target.facts(), target._facts.indices()):
    #         assert fact is target._facts.get_item(index)

    @pytest.mark.skip
    def test_insert_fact_after(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        pass
    #     class PatchInsertAfter:
    #         def __init__(self): self.called = False

    #         def insert_after(self, _item, _index): self.called = True

    #     patch_outline = PatchInsertAfter()
    #     monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
    #                         'insert_after', patch_outline.insert_after)
    #     TITLE_MODEL = 'Something completely different.'
    #     target = MTOPIC.Topic()
    #     target.init_identity(p_title=TITLE_MODEL)
    #     target.set_fresh()
    #     # Test
    #     _ = target.insert_fact_after(None, None)
    #     assert patch_outline.called
    #     assert target.is_stale()

    @pytest.mark.skip
    def test_insert_fact_before(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        pass
    #     class PatchInsertBefore:
    #         def __init__(self): self.called = False

    #         def insert_before(self, _item, _index): self.called = True

    #     patch_outline = PatchInsertBefore()
    #     monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
    #                         'insert_before', patch_outline.insert_before)
    #     TITLE_MODEL = 'Something completely different.'
    #     target = MTOPIC.Topic()
    #     target.init_identity(p_title=TITLE_MODEL)
    #     target.set_fresh()
    #     # Test
    #     _ = target.insert_fact_before(None, None)
    #     assert patch_outline.called
    #     assert target.is_stale()

    @pytest.mark.skip
    def test_insert_fact_child(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        pass
    #     class PatchInsertChild:
    #         def __init__(self): self.called = False

    #         def insert_child(self, _item, _index): self.called = True

    #     patch_outline = PatchInsertChild()
    #     monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
    #                         'insert_child', patch_outline.insert_child)
    #     TITLE_MODEL = 'Something completely different.'
    #     target = MTOPIC.Topic()
    #     target.init_identity(p_title=TITLE_MODEL)
    #     target.set_fresh()
    #     # Test
    #     _ = target.insert_fact_child(None, None)
    #     assert patch_outline.called
    #     assert target.is_stale()

    @pytest.mark.skip
    def test_insert_facts_section(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        pass
    #     class PatchInsertSection:
    #         def __init__(self): self.called = False

    #         def insert_section(self, _source, _i_from, _i_to):
    #             self.called = True

    #     patch_outline = PatchInsertSection()
    #     monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
    #                         'insert_section', patch_outline.insert_section)
    #     TITLE_MODEL = 'Something completely different.'
    #     target = MTOPIC.Topic()
    #     target.init_identity(p_title=TITLE_MODEL)
    #     target.set_fresh()
    #     # Test
    #     _ = target.insert_facts_section(None, None)
    #     assert patch_outline.called
    #     assert target.is_stale()

    @pytest.mark.skip
    def test_is_fresh(self, factory_topic):
        """Confirm return is accurate.

        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info stale, no facts.
        #. Case: Topic fresh, ID info fresh, no facts.
        """
        # Setup
        pass
    #     target = factory_topic()
    #     I_LEAF = 2
    #     I_LAST = 4
    #     # Test: InfoId stale, ID info fresh, no facts.
    #     target._stale = True
    #     target._infoid.set_fresh()
    #     assert not target.is_fresh()
    #     assert target._stale
    #     # Test: InfoId fresh, ID info fresh, no stale.
    #     target._stale = False
    #     target._infoid.set_stale()
    #     assert not target.is_fresh()
    #     assert target._stale
    #     # Test: InfoId fresh, ID info fresh, no facts.
    #     assert not target.is_fresh()
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     assert target.is_fresh()
    #     assert not target._stale
    #     # Test: Topic fresh, ID info fresh, leaf fact stale
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if i == I_LEAF:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     assert not target.is_fresh()
    #     assert target._stale
    #     # Test: Topic fresh, ID info fresh, last fact stale
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if i == I_LAST:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     assert not target.is_fresh()
    #     assert target._stale
    #     # Test: Sheet fresh, ID info fresh, facts fresh
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         fact.set_fresh()
    #     assert target.is_fresh()
    #     assert not target._stale

    @pytest.mark.skip
    def test_is_stale(self, factory_topic):
        """Confirm return is accurate.

        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info stale, no facts.
        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic fresh, ID info fresh, leaf fact stale.
        #. Case: Topic fresh, ID info fresh, last fact stale.
        #. Case: Sheet fresh, ID info fresh, facts fresh.
        """
        # Setup
        pass
    #     target = factory_topic()
    #     I_LEAF = 2
    #     I_LAST = 4
    #     # Test: Topic stale, ID info fresh, no facts.
    #     target._stale = True
    #     target._infoid.set_fresh()
    #     assert target.is_stale()
    #     assert target._stale
    #     # Test: Topic fresh, ID info stale, no facts.
    #     target._stale = False
    #     target._infoid.set_stale()
    #     assert target.is_stale()
    #     assert target._stale
    #     # Test: Topic fresh, ID info fresh, no facts.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     assert not target.is_stale()
    #     assert not target._stale
    #     # Test: Topic fresh, ID info fresh, leaf fact stale.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if i == I_LEAF:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     assert target.is_stale()
    #     assert target._stale
    #     # Test: Topic fresh, ID info fresh, last fact stale.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if i == I_LAST:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     assert target.is_stale()
    #     assert target._stale
    #     # Test: Sheet fresh, ID info fresh, facts fresh.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         fact.set_fresh()
    #     assert not target.is_stale()
    #     assert not target._stale

    @pytest.mark.skip
    def test_set_fresh(self, factory_topic):
        """Confirm all attributes set.

        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info stale, no facts.
        #. Case: Topic stale, ID info stale, no facts.
        #. Case: Sheet fresh, ID info fresh, topics stale
        #. Case: Sheet stale, ID info stale, topics stale
        """
        # Setup
        pass
    #     target = factory_topic()
    #     # Test: Topic fresh, ID info fresh, no facts.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Topic stale, ID info fresh, no facts.
    #     target._stale = True
    #     target._infoid.set_fresh()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Topic fresh, ID info stale, no facts.
    #     target._stale = False
    #     target._infoid.set_stale()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Topic stale, ID info stale, no facts.
    #     target._stale = True
    #     target._infoid.set_stale()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Sheet fresh, ID info stale, facts stale.
    #     target._stale = False
    #     target._infoid.set_stale()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if i % 2:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         assert fact.is_fresh()
    #     # Test: Sheet stale, ID info stale, facts stale.
    #     target._stale = True
    #     target._infoid.set_stale()
    #     for i, index in enumerate(target._facts.indices()):
    #         fact = target._facts.get_item(index)
    #         if not i % 2:
    #             fact.set_stale()
    #         else:
    #             fact.set_fresh()
    #     target.set_fresh()
    #     assert not target._stale
    #     assert target._infoid.is_fresh()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         assert fact.is_fresh()

    @pytest.mark.skip
    def test_set_stale(self, factory_topic):
        """Confirm all attributes set.

        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info fresh, facts fresh.
         """
        # Setup
        pass
    #     target = factory_topic()
    #     # Test: Topic fresh, ID info fresh, no facts.
    #     target._stale = False
    #     target._infoid.set_fresh()
    #     target.set_stale()
    #     assert target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Topic stale, ID info fresh, no facts.
    #     target._stale = True
    #     target._infoid.set_fresh()
    #     target.set_stale()
    #     assert target._stale
    #     assert target._infoid.is_fresh()
    #     # Test: Topic fresh, ID info stale, no facts.
    #     target._stale = False
    #     target._infoid.set_stale()
    #     target.set_stale()
    #     assert target._stale
    #     assert target._infoid.is_stale()
    #     # Test: Topic stale, ID info stale, no facts.
    #     target._stale = True
    #     target._infoid.set_stale()
    #     target.set_stale()
    #     assert target._stale
    #     assert target._infoid.is_stale()
    #     # Test: Topic fresh, ID info fresh, facts fresh.
    #     target._stale = True
    #     target._infoid.set_fresh()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         fact.set_fresh()
    #     target.set_stale()
    #     assert target._stale
    #     assert target._infoid.is_fresh()
    #     for index in target._facts.indices():
    #         fact = target._facts.get_item(index)
    #         assert fact.is_fresh()


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.topic`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (MTOPIC.NameTopic, BUI.BridgeTextMarkup),
        (MTOPIC.SummaryTopic, BUI.BridgeTextFormat),
        (MTOPIC.TitleTopic, BUI.BridgeTextMarkup),
        (MTOPIC.TagTopic.__supertype__, int),  # type: ignore[attr-defined]
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
