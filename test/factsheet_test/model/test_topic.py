"""
Unit tests for topic-level model. See :mod:`~.topic`.
"""
import dataclasses as DC
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import re as RE

import factsheet.adapt_gtk.adapt_topic as ATOPIC
import factsheet.model.fact as MFACT
import factsheet.model.infoid as MINFOID
import factsheet.model.topic as MTOPIC
import factsheet.model.types_model as MTYPES


class TestTopic:
    """Unit tests for :class:`.Topic`."""

    def test_eq(self, patch_class_fact, factory_topic):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: Fact collection diffrence
        #. Case: Equivalence
        """
        # Setup
        PatchFact = patch_class_fact
        reference = factory_topic()
        TEXT = 'Something completely different'
        # Test: type difference
        assert not reference.__eq__(TEXT)
        # Test: InfoId difference
        target = factory_topic()
        target.init_identity(p_title=TEXT)
        assert not reference.__eq__(target)
        # Test: Fact collection diffrence
        target = factory_topic()
        fact = PatchFact(p_topic=target)
        target.insert_fact_before(fact, None)
        assert not reference.__eq__(target)
        # Test: Equivalence
        target = factory_topic()
        assert reference.__eq__(target)
        assert not reference.__ne__(target)

    def test_get_set_state(
            self, tmp_path, factory_topic, interface_form_topic):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        source = factory_topic()
        source._stale = True

        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        for form in forms:
            source.attach_form(form)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert isinstance(target._forms, dict)
        assert not target._forms
        assert not target._stale
        assert source._infoid == target._infoid
        assert source._facts == target._facts

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        BLANK = ''
        # Test
        target = MTOPIC.Topic()
        assert not target._stale
        assert isinstance(target._forms, dict)
        assert not target._forms
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert BLANK == target._infoid.name
        assert BLANK == target._infoid.summary
        assert BLANK == target._infoid.title
        assert id(target) == target._tag
        assert isinstance(target._facts, MTYPES.OutlineFacts)
        target_facts = [target._facts.get_item(i)
                        for i in target._facts.indices()]
        assert not target_facts

    def test_init_extra(self):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        ERROR = RE.escape("Topic.__init__() called with extra argument(s): "
                          "{'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = MTOPIC.Topic(extra='Oops!')

    def test_init_identity(self, patch_args_infoid):
        """| Confirm identification initialization.
        | Case: explicit arguments.
        """
        # Setup
        target = MTOPIC.Topic()
        ARGS = patch_args_infoid
        # Test
        target.init_identity(**DC.asdict(ARGS))
        assert ARGS.p_name == target._infoid.name
        assert ARGS.p_summary == target._infoid.summary
        assert ARGS.p_title == target._infoid.title

    def test_init_identity_default(self):
        """| Confirm identification initialization.
        | Case: default arguments.
        """
        # Setup
        target = MTOPIC.Topic()
        TEXT = 'Something completely different.'
        target._infoid.init_identity(
            p_name=TEXT, p_summary=TEXT, p_title=TEXT)
        BLANK = ''
        # Test
        target.init_identity()
        assert BLANK == target._infoid.name
        assert BLANK == target._infoid.summary
        assert BLANK == target._infoid.title

    @pytest.mark.parametrize('NAME_PROP', [
        'name',
        'summary',
        'title',
        ])
    def test_property_infoid(self, patch_args_infoid, NAME_PROP):
        """Confirm identification properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = MTOPIC.Topic()
        ARGS = patch_args_infoid
        target.init_identity(**DC.asdict(ARGS))
        value_attr = getattr(target._infoid, NAME_PROP)
        target_prop = getattr(MTOPIC.Topic, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr == value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_attach_form(self, factory_topic, interface_form_topic):
        """| Confirm fact form addition.
        | Case: form not attached initially.
        """
        # Setup
        target = factory_topic()

        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        assert forms[0].get_infoid().title != target._infoid.title
        # Test
        for form in forms:
            target.attach_form(form)
            assert target._infoid.title == form.get_infoid().title
            assert target._facts._gtk_model is (
                form._facts.gtk_view.get_model())
            assert target._forms[id(form)] is form
        assert len(forms) == len(target._forms)

    def test_attach_form_warn(self, factory_topic, interface_form_topic,
                              PatchLogger, monkeypatch):
        """| Confirm fact form addition.
        | Case: form attached initially.
        """
        # Setup
        target = factory_topic()

        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        assert forms[0].get_infoid().title != target._infoid.title
        for form in forms:
            target.attach_form(form)
        assert N_FORMS == len(target._forms)
        I_DUP = 1
        form_dup = forms[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate form: {} (Topic.attach_form)'
            ''.format(hex(id(form_dup))))
        assert not patch_logger.called
        # Test
        target.attach_form(form_dup)
        assert len(forms) == len(target._forms)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_check_fact(self, patch_class_fact, factory_topic):
        """Confirm fact check."""
        # Setup
        PatchFact = patch_class_fact
        target = factory_topic()
        I_LEAF = 2
        index = list(target._facts.indices())[I_LEAF]
        fact = target._facts.get_item(index)
        target.set_fresh()
        # Test
        target.check_fact(index)
        assert target.is_stale()
        assert PatchFact.VALUE == fact()
        assert fact.status is MFACT.StatusOfFact.DEFINED

    def test_clear_all(self, factory_topic):
        """Confirm fact check."""
        # Setup
        target = factory_topic()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            _ = fact.check()
        target.set_fresh()
        # Test
        target.clear_all()
        assert target.is_stale()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            assert fact() is None
            assert fact.status is MFACT.StatusOfFact.UNCHECKED

    def test_clear_fact(self, factory_topic):
        """Confirm fact clear."""
        # Setup
        target = factory_topic()
        I_LEAF = 2
        index = list(target._facts.indices())[I_LEAF]
        fact = target._facts.get_item(index)
        _ = fact.check()
        target.set_fresh()
        # Test
        target.clear_fact(index)
        assert target.is_stale()
        assert fact() is None
        assert fact.status is MFACT.StatusOfFact.UNCHECKED

    def test_detach_all(
            self, monkeypatch, factory_topic, interface_form_topic):
        """Confirm removal of all forms."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        target = factory_topic()
        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        for form in forms:
            target.attach_form(form)
        assert N_FORMS == len(target._forms)
        # Test
        target.detach_all()
        assert not target._forms
        assert N_FORMS == patch_detach.n_calls

    def test_detach_attribute_views(
            self, monkeypatch, factory_topic, interface_form_topic):
        """Confirm removal of attribute views."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        class PatchFactsDetach:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_facts = PatchFactsDetach()
        monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact, 'detach_view',
                            patch_facts.detach_view)

        target = factory_topic()
        form = interface_form_topic()
        target.attach_form(form)
        # Test
        target._detach_attribute_views(form)
        assert patch_infoid.called
        assert patch_facts.called

    def test_detach_form(
            self, monkeypatch, factory_topic, interface_form_topic):
        """| Confirm removal of topic form.
        | Case: form attached initially.
        """
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        target = factory_topic()
        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        for form in forms:
            target.attach_form(form)
        N_REMOVE = 1
        I_REMOVE = 1
        form_rem = forms.pop(I_REMOVE)
        # Test
        target.detach_form(form_rem)
        assert N_REMOVE == patch_infoid.n_calls
        assert len(forms) == len(target._forms)
        for form in forms:
            assert target._forms[id(form)] is form

    def test_detach_form_warn(self, factory_topic, interface_form_topic,
                              PatchLogger, monkeypatch):
        """| Confirm topic form removal.
        | Case: form not attached initially.
        """
        # Setup
        target = factory_topic()
        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        assert forms[0].get_infoid().title != target._infoid.title
        for form in forms:
            target.attach_form(form)
        form_missing = interface_form_topic()
        assert N_FORMS == len(target._forms)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing form: {} (Topic.detach_form)'
            ''.format(hex(id(form_missing))))
        # Test
        target.detach_form(form_missing)
        assert N_FORMS == len(target._forms)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_facts(self, factory_topic):
        """Confirm iterator over fact."""
        # Setup
        target = factory_topic()
        # Test
        for fact, index in zip(target.facts(), target._facts.indices()):
            assert fact is target._facts.get_item(index)

    def test_insert_fact_after(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        class PatchInsertAfter:
            def __init__(self): self.called = False

            def insert_after(self, _item, _index): self.called = True

        patch_outline = PatchInsertAfter()
        monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
                            'insert_after', patch_outline.insert_after)
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_fact_after(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_insert_fact_before(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        class PatchInsertBefore:
            def __init__(self): self.called = False

            def insert_before(self, _item, _index): self.called = True

        patch_outline = PatchInsertBefore()
        monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
                            'insert_before', patch_outline.insert_before)
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_fact_before(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_insert_fact_child(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        class PatchInsertChild:
            def __init__(self): self.called = False

            def insert_child(self, _item, _index): self.called = True

        patch_outline = PatchInsertChild()
        monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
                            'insert_child', patch_outline.insert_child)
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_fact_child(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_insert_facts_section(self, monkeypatch):
        """Confirm method passes request to facts outline."""
        # Setup
        class PatchInsertSection:
            def __init__(self): self.called = False

            def insert_section(self, _source, _i_from, _i_to):
                self.called = True

        patch_outline = PatchInsertSection()
        monkeypatch.setattr(ATOPIC.AdaptTreeStoreFact,
                            'insert_section', patch_outline.insert_section)
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_facts_section(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_is_fresh(self, factory_topic):
        """Confirm return is accurate.

        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info stale, no facts.
        #. Case: Topic fresh, ID info fresh, no facts.
        """
        # Setup
        target = factory_topic()
        I_LEAF = 2
        I_LAST = 4
        # Test: InfoId stale, ID info fresh, no facts.
        target._stale = True
        target._infoid.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, ID info fresh, no stale.
        target._stale = False
        target._infoid.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, ID info fresh, no facts.
        assert not target.is_fresh()
        target._stale = False
        target._infoid.set_fresh()
        assert target.is_fresh()
        assert not target._stale
        # Test: Topic fresh, ID info fresh, leaf fact stale
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if i == I_LEAF:
                fact.set_stale()
            else:
                fact.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: Topic fresh, ID info fresh, last fact stale
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if i == I_LAST:
                fact.set_stale()
            else:
                fact.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, facts fresh
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            fact.set_fresh()
        assert target.is_fresh()
        assert not target._stale

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
        target = factory_topic()
        I_LEAF = 2
        I_LAST = 4
        # Test: Topic stale, ID info fresh, no facts.
        target._stale = True
        target._infoid.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, ID info stale, no facts.
        target._stale = False
        target._infoid.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, ID info fresh, no facts.
        target._stale = False
        target._infoid.set_fresh()
        assert not target.is_stale()
        assert not target._stale
        # Test: Topic fresh, ID info fresh, leaf fact stale.
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if i == I_LEAF:
                fact.set_stale()
            else:
                fact.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, ID info fresh, last fact stale.
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if i == I_LAST:
                fact.set_stale()
            else:
                fact.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, facts fresh.
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            fact.set_fresh()
        assert not target.is_stale()
        assert not target._stale

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
        target = factory_topic()
        # Test: Topic fresh, ID info fresh, no facts.
        target._stale = False
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, ID info fresh, no facts.
        target._stale = True
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, ID info stale, no facts.
        target._stale = False
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, ID info stale, no facts.
        target._stale = True
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet fresh, ID info stale, facts stale.
        target._stale = False
        target._infoid.set_stale()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if i % 2:
                fact.set_stale()
            else:
                fact.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            assert fact.is_fresh()
        # Test: Sheet stale, ID info stale, facts stale.
        target._stale = True
        target._infoid.set_stale()
        for i, index in enumerate(target._facts.indices()):
            fact = target._facts.get_item(index)
            if not i % 2:
                fact.set_stale()
            else:
                fact.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            assert fact.is_fresh()

    def test_set_stale(self, factory_topic):
        """Confirm all attributes set.

        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info fresh, no facts.
        #. Case: Topic stale, ID info fresh, no facts.
        #. Case: Topic fresh, ID info fresh, facts fresh.
         """
        # Setup
        target = factory_topic()
        # Test: Topic fresh, ID info fresh, no facts.
        target._stale = False
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, ID info fresh, no facts.
        target._stale = True
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, ID info stale, no facts.
        target._stale = False
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Topic stale, ID info stale, no facts.
        target._stale = True
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Topic fresh, ID info fresh, facts fresh.
        target._stale = True
        target._infoid.set_fresh()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            fact.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        for index in target._facts.indices():
            fact = target._facts.get_item(index)
            assert fact.is_fresh()

    def test_tag(self):
        """Confirm reported topic tag."""
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        # Test: read
        target_prop = getattr(MTOPIC.Topic, 'tag')
        assert target_prop.fget is not None
        assert target._tag == target.tag
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None


class TestTypes:
    """Unit tests for type definitions in :mod:`.Topic`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert MTOPIC.TagTopic is MTYPES.TagTopic
