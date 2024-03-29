"""
Unit tests for topic-level model. See :mod:`~.topic`.

.. include:: /test/refs_include_pytest.txt
"""
# from pathlib import Path
# import itertools as IT
# import pickle
import pytest

import factsheet.bridge_ui as BUI
# import factsheet.model.fact as MFACT
import factsheet.model.topic as MTOPIC


class TestTopic:
    """Unit tests for :class:`.Topic`."""

    @pytest.mark.skip
    def test_contains_in(self):
        """| Confirm check for fact in facts outline.
        | Case: fact in facts outline
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts:
        #     _ = target._facts.insert_before(fact)
        # I_FACT_TEST = 2
        # fact_test = facts[I_FACT_TEST]
        # # Test
        # assert fact_test in target

    @pytest.mark.skip
    def test_contains_not_in(self):
        """| Confirm check for fact in facts outline.
        | Case: fact not in facts outline
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts:
        #     _ = target._facts.insert_before(fact)
        # fact_test = MFACT.Fact(p_topic=target)
        # # Test
        # assert fact_test not in target

    @pytest.mark.skip
    def test_contains_none(self):
        """| Confirm check for fact in facts outline.
        | Case: item is None
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts:
        #     _ = target._facts.insert_before(fact)
        # item_test = None
        # # Test
        # assert item_test not in target

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: identity difference.
        #. Case: facts outline diffrence.
        #. Case: Equivalence
        """
        # Setup
        source = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        TEXT = 'Something completely different'
        # N_FACTS = 5
        # facts_source = [MFACT.Fact(p_topic=source) for _ in range(N_FACTS)]
        # for fact in facts_source:
        #     _ = source._facts.insert_before(fact)
        # Test: type difference
        assert not source.__eq__(TITLE)
        # Test: identity difference
        target = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        target.title.text = TEXT
        assert not source.__eq__(target)
        # Test: Facts outline diffrence
        # target = MTOPIC.Topic()
        # target.title.text = TITLE
        # facts_target = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts_target:
        #     _ = target._facts.insert_before(fact)
        # assert not source.__eq__(target)
        # Test: Equivalence
        target = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        target._stale = True
        target.title.text = TITLE
        # for fact in facts_source:
        #     _ = target._facts.insert_before(fact)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    # def test_get_set_state(self, new_id_args, tmp_path):
    #     """Confirm conversion to and from pickle format."""
    #     # Setup
    #     path = Path(str(tmp_path / 'get_set.fsg'))
    #     ID_ARGS = new_id_args()
    #     source = MTOPIC.Topic(**ID_ARGS)
    #     # N_FACTS = 5
    #     # for i in range(N_FACTS):
    #     #     fact = MFACT.Fact(p_topic=source)
    #     #     fact.name.text = 'Fact {:02}'.format(i)
    #     #     _ = source._facts.insert_before(fact)
    #     source._stale = True
    #     # Test
    #     with path.open(mode='wb') as io_out:
    #         pickle.dump(source, io_out)
    #     with path.open(mode='rb') as io_in:
    #         target = pickle.load(io_in)
    #     assert not target._stale
    #     # assert source._tag != target._tag
    #     assert source.name.text == target.name.text
    #     assert source.summary.text == target.summary.text
    #     assert source.title.text == target.title.text
    #     # for fact_s, fact_t in IT.zip_longest(
    #     #         source._facts.items(), target._facts.items()):
    #     #     assert fact_s.name.text == fact_t.name.text

    def test_init(self, new_id_args):
        """Confirm initialization.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        # Test
        target = MTOPIC.Topic(**ID_ARGS)
        assert isinstance(target._name, MTOPIC.Name)
        assert ID_ARGS['p_name'] == target.name.text
        assert isinstance(target._summary, MTOPIC.Summary)
        assert ID_ARGS['p_summary'] == target.summary.text
        assert isinstance(target._title, MTOPIC.Title)
        assert ID_ARGS['p_title'] == target.title.text
        assert not target._stale
        # assert target._facts.__orig_class__ is MTOPIC.OutlineFacts
        # with pytest.raises(StopIteration):
        #     next(iter(target._facts))

    @pytest.mark.skip
    def test_iter(self):
        """| Confirm iterator over facts outline.
        | Case: no lines with None.
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts:
        #     _ = target._facts.insert_before(fact)
        # # Test
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.skip
    def test_iter_blank(self):
        """| Confirm iterator over facts outline.
        | Case: lines with None.
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # I_BLANKS = [1, 3]
        # facts_blank = list(facts)
        # for i in I_BLANKS:
        #     facts_blank.insert(i, None)
        # for item in facts_blank:
        #     target._facts.insert_before(item)
        # # Test
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        # ('_facts', 'facts'),
        ('_name', 'name'),
        ('_summary', 'summary'),
        # ('_tag', 'tag'),
        ('_title', 'title'),
        ])
    def test_property(self, new_model_topic, NAME_ATTR, NAME_PROP):
        """Confirm values and access limits of properties.

        :param new_model_topic: fixture :func:`.new_model_topic`.
        :param NAME_ATTR: name of attribute under test.
        :param NAME_PROP: name of property under test.
        """
        # Setup
        N_FACTS = 5
        target = new_model_topic(N_FACTS)
        target_prop = getattr(MTOPIC.Topic, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_property_tag(self, new_model_topic):
        """Confirm values and access limits of tag property.

        :param new_model_topic: fixture :func:`.new_model_topic`.
        """
        # Setup
        N_FACTS = 5
        target = new_model_topic(N_FACTS)
        target_prop = getattr(MTOPIC.Topic, 'tag')
        # Test
        assert target_prop.fget is not None
        assert id(target) == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.skip
    def test_append_fact(self):
        """| Confirm fact appended to facts outline.
        | Case: no duplicate facts.
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # # Test
        # for fact in facts:
        #     target.append_fact(fact)
        # assert target.is_stale()
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.skip
    def test_append_fact_dup(self):
        """| Confirm fact appended to facts outline.
        | Case: duplicate facts.
        """
        # # Setup
        # target = MTOPIC.Topic()
        # N_FACTS = 5
        # facts = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts:
        #     _ = target.append_fact(fact)
        # target.set_fresh()
        # # Test
        # for fact in facts:
        #     target.append_fact(fact)
        # assert target.has_not_changed()
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.skip
    def test_append_outline_fact(self):
        """| Confirm facts outline appended to facts outline.
        | Case: no duplicate facts.
        """
        # # Setup
        # N_FACTS = 5
        # target = MTOPIC.Topic()
        # facts_target = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts_target:
        #     target.append_fact(fact)
        # target.set_fresh()
        # source = MTOPIC.Topic()
        # facts_source = [MFACT.Fact(p_topic=source) for _ in range(N_FACTS)]
        # for fact in facts_source:
        #     source.append_fact(fact)
        # facts = facts_target + facts_source
        # # Test
        # target.append_outline_facts(source)
        # target.is_stale()
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.skip
    def test_append_outline_fact_dup(self):
        """| Confirm facts outline appended to facts outline.
        | Case: duplicate facts.
        """
        # # Setup
        # N_FACTS = 5
        # target = MTOPIC.Topic()
        # facts_target = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts_target:
        #     target.append_fact(fact)
        # target.set_fresh()
        # source = MTOPIC.Topic()
        # for fact in reversed(facts_target):
        #     source.append_fact(fact)
        # facts = facts_target
        # # Test
        # target.append_outline_facts(source)
        # target.has_not_changed()
        # for fact, fact_target in IT.zip_longest(facts, target):
        #     assert fact is fact_target

    @pytest.mark.skip
    def test_check_fact(self, new_model_topic, patch_class_fact):
        """Confirm fact checked."""
        # # Setup
        # PatchFact = patch_class_fact
        # N_FACTS = 5
        # target = new_model_topic(N_FACTS)
        # I_FACT = 2
        # line_fact = list(target._facts.lines())[I_FACT]
        # fact = target._facts.get_item(line_fact)
        # # Test
        # target.check_fact(line_fact)
        # assert PatchFact.VALUE_CHECKED == fact.value
        # assert fact.status is PatchFact.STATUS_CHECKED
        # assert target.is_stale()

    @pytest.mark.skip
    def test_clear(self, new_model_topic, patch_class_fact):
        """Confirm all facts cleared."""
        # # Setup
        # PatchFact = patch_class_fact
        # N_FACTS = 5
        # target = new_model_topic(N_FACTS)
        # # Test
        # target.clear()
        # for fact in target:
        #     assert PatchFact.VALUE_CLEARED == fact.value
        #     assert fact.status is PatchFact.STATUS_CLEARED
        # assert target.is_stale()

    @pytest.mark.skip
    def test_clear_fact(self, new_model_topic, patch_class_fact):
        """Confirm fact cleared."""
        # # Setup
        # PatchFact = patch_class_fact
        # N_FACTS = 5
        # target = new_model_topic(N_FACTS)
        # I_FACT = 2
        # line_fact = list(target._facts.lines())[I_FACT]
        # fact = target._facts.get_item(line_fact)
        # target.check_fact(line_fact)
        # # Test
        # target.clear_fact(line_fact)
        # assert PatchFact.VALUE_CLEARED == fact.value
        # assert fact.status is PatchFact.STATUS_CLEARED
        # assert target.is_stale()

    def test_is_stale(self, new_model_topic):
        """Confirm fresh/stale check with facts.

        #. Case: Topic stale, identity fresh, facts fresh.
        #. Case: Topic fresh, identity stale, facts fresh.
        #. Case: Sheet fresh, identity fresh, facts fresh.
        #. Case: Topic fresh, identity fresh, a fact stale.

        :param new_model_topic: fixture :func:`.new_model_topic`.
        """
        # Setup
        N_FACTS = 5
        target = new_model_topic(N_FACTS)
        # Test: Topic stale, identity fresh, facts fresh.
        target._stale = True
        target.summary.set_fresh()
        assert target.is_stale()
        assert target._stale
        assert not target.has_not_changed()
        # Test: Topic fresh, identity stale, facts fresh.
        target._stale = False
        target.summary.set_stale()
        assert target.is_stale()
        assert target._stale
        assert not target.has_not_changed()
        # Test: Topic fresh, identity fresh, facts fresh.
        target._stale = False
        target.summary.set_fresh()
        assert not target.is_stale()
        assert not target._stale
        assert target.has_not_changed()
        # Test: Topic fresh, identity fresh, a fact stale.
        # LINE_STALE = 2
        # target._stale = False
        # target.summary.set_fresh()
        # for i, line in enumerate(target._facts.lines()):
        #     fact = target._facts.get_item(line)
        #     if i == LINE_STALE:
        #         fact.set_stale()
        #     else:
        #         fact.set_fresh()
        # assert target.is_stale()
        # assert target._stale
        # assert not target.has_not_changed()

    def test_is_stale_no_facts(self, new_model_topic):
        """Confirm fresh/stale check without facts.

        #. Case: Topic stale, identity fresh, no facts.
        #. Case: Topic fresh, identity stale, no facts.
        #. Case: Topic fresh, identity fresh, no facts.

        :param new_model_topic: fixture :func:`.new_model_topic`.
        """
        # Setup
        N_FACTS = 5
        target = new_model_topic(N_FACTS)
        # Test: Topic stale, identity fresh, no facts.
        target._stale = True
        target.summary.set_fresh()
        assert target.is_stale()
        assert target._stale
        assert not target.has_not_changed()
        # Test: Topic fresh, identity stale, no facts.
        target._stale = False
        target.summary.set_stale()
        assert target.is_stale()
        assert target._stale
        assert not target.has_not_changed()
        # Test: Topic fresh, identity fresh, no facts.
        target._stale = False
        target.summary.set_fresh()
        assert not target.is_stale()
        assert not target._stale
        assert target.has_not_changed()

    def test_set_fresh(self, new_model_topic):
        """Confirm frest set at all levels.

        #. Case: Topic fresh, identity fresh, facts fresh.
        #. Case: Topic stale, identity fresh, facts fresh.
        #. Case: Topic fresh, identity stale, facts fresh.
        #. Case: Topic fresh, identity fresh, facts stale.
        #. Case: Sheet stale, identity stale, facts stale

        :param new_model_topic: fixture :func:`.new_model_topic`.
        """
        # Setup
        N_FACTS = 5
        target = new_model_topic(N_FACTS)
        # N_FACTS = 5
        # facts_target = [MFACT.Fact(p_topic=target) for _ in range(N_FACTS)]
        # for fact in facts_target:
        #     target.append_fact(fact)
        # Test: Topic fresh, identity fresh, facts fresh.
        target._stale = False
        target.summary.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target.has_not_changed()
        assert target.summary.has_not_changed()
        # for fact in facts_target:
        #     assert fact.has_not_changed()
        # Test: Topic stale, identity fresh, facts fresh.
        target._stale = True
        target.summary.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target.has_not_changed()
        assert target.summary.has_not_changed()
        # for fact in facts_target:
        #     assert fact.has_not_changed()
        # Test: Topic fresh, identity stale, facts fresh.
        target._stale = False
        target.summary.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target.has_not_changed()
        assert target.summary.has_not_changed()
        # for fact in facts_target:
        #     assert fact.has_not_changed()
        # Test: Topic fresh, identity fresh, facts stale.
        # LINE_STALE = 1
        # target._stale = False
        # target.summary.set_fresh()
        # for i, line in enumerate(target._facts.lines()):
        #     fact = target._facts.get_item(line)
        #     if i == LINE_STALE:
        #         fact.set_stale()
        #     else:
        #         fact.set_fresh()
        # target.set_fresh()
        # assert not target._stale
        # assert target.has_not_changed()
        # assert target.summary.has_not_changed()
        # for fact in facts_target:
        #     assert fact.has_not_changed()
        # # Test: Sheet stale, identity stale, facts stale
        # LINE_STALE = 4
        # target._stale = True
        # target.summary.set_stale()
        # for i, line in enumerate(target._facts.lines()):
        #     fact = target._facts.get_item(line)
        #     if i == LINE_STALE:
        #         fact.set_stale()
        #     else:
        #         fact.set_fresh()
        # target.set_fresh()
        # assert not target._stale
        # assert target.has_not_changed()
        # assert target.summary.has_not_changed()
        # for fact in facts_target:
        #     assert fact.has_not_changed()


class TestModule:
    """Unit tests for module-level components of :mod:`.topic`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (MTOPIC.LineOutline, BUI.LineOutline),
        (MTOPIC.Name, BUI.x_b_t_ModelTextMarkup),
        (MTOPIC.DisplayName, BUI.DisplayTextMarkup),
        (MTOPIC.FactoryDisplayName, BUI.FactoryDisplayTextMarkup),
        (MTOPIC.EditorName, BUI.EditorTextMarkup),
        (MTOPIC.FactoryEditorName, BUI.FactoryEditorTextMarkup),
        # (MTOPIC.OutlineFacts, BUI.BridgeOutlineColumnar[MFACT.Fact]),
        (MTOPIC.Summary, BUI.ModelTextStyled),
        (MTOPIC.DisplaySummary, BUI.DisplayTextStyled),
        (MTOPIC.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (MTOPIC.EditorSummary, BUI.EditorTextStyled),
        (MTOPIC.FactoryEditorSummary, BUI.FactoryEditorTextStyled),
        (MTOPIC.Title, BUI.x_b_t_ModelTextMarkup),
        (MTOPIC.DisplayTitle, BUI.DisplayTextMarkup),
        (MTOPIC.FactoryDisplayTitle, BUI.FactoryDisplayTextMarkup),
        (MTOPIC.EditorTitle, BUI.EditorTextMarkup),
        (MTOPIC.FactoryEditorTitle, BUI.FactoryEditorTextMarkup),
        (MTOPIC.TagTopic.__qualname__, 'NewType.<locals>.new_type'),
        (MTOPIC.TagTopic.__dict__['__supertype__'], int),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
