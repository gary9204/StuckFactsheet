"""
Unit tests for topic-level model. See :mod:`~.topic`.
"""
import dataclasses as DC
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import re as RE

import factsheet.model.infoid as MINFOID
import factsheet.model.topic as MTOPIC
import factsheet.model.types_model as MTYPES


class TestTopic:
    """Unit tests for :class:`~.model.topic.Topic`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: Fact collection diffrence
        #. Case: Equivalence
        """
        # Setup
        TITLE_MODEL = 'The Parrot Sketch'
        source = MTOPIC.Topic()
        source.init_identity(p_title=TITLE_MODEL)
        # Test: type difference
        assert not source.__eq__(TITLE_MODEL)
        # Test: InfoId difference
        TITLE_TARGET = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_TARGET)
        assert not source.__eq__(target)
        # # Test: Fact collection diffrence
        # target_facts = FACTS[:]
        # _ = target_facts.pop()
        # target = MTOPIC.Topic(p_classes_fact=target_facts)
        # target.init_identity(p_title=TITLE_MODEL)
        # assert not source.__eq__(target)
        # Test: Equivalence
        target = MTOPIC.Topic()
        target._facts = source._facts
        target.init_identity(p_title=TITLE_MODEL)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(
            self, tmp_path, patch_args_infoid, interface_form_topic):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        source = MTOPIC.Topic()
        ARGS = patch_args_infoid
        source.init_identity(**DC.asdict(ARGS))
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
        # assert len(FACTS) == len(target_facts)
        # for fact, class_fact in zip(target_facts, FACTS):
        #     assert isinstance(fact, class_fact)

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
        """| Confirm Identification initialization.
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
        """| Confirm Identification initialization.
        | Case: explicit arguments.
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
        """Confirm pass-through InfoId properties are get-only.

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

    def test_attach_form(self, interface_form_topic):
        """Confirm topic form addition.
        Case: form not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        assert forms[0].get_infoid().title != target._infoid.title
        # Test
        for form in forms:
            target.attach_form(form)
            assert target._infoid.title == form.get_infoid().title
            assert target._forms[id(form)] is form
        assert len(forms) == len(target._forms)

    def test_attach_form_warn(
            self, interface_form_topic, PatchLogger, monkeypatch):
        """Confirm topic form addition.
        Case: form attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

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

    def test_detach_all(self, monkeypatch, interface_form_topic):
        """Confirm removals."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

        N_FORMS = 3
        forms = [interface_form_topic() for _ in range(N_FORMS)]
        for form in forms:
            target.attach_form(form)
        assert N_FORMS == len(target._forms)
        # Test
        target.detach_all()
        assert not target._forms
        assert N_FORMS == patch_detach.n_calls

    def test_detach_attribute_views(self, monkeypatch, interface_form_topic):
        """Confirm removal of attribute views."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

        form = interface_form_topic()
        target.attach_form(form)
        # Test
        target._detach_attribute_views(form)
        assert patch_infoid.called

    def test_detach_form(self, monkeypatch, interface_form_topic):
        """Confirm topic form removal.
        Case: form attached initially
        """
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

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

    def test_detach_form_warn(
            self, interface_form_topic, PatchLogger, monkeypatch):
        """Confirm topic form removal.
        Case: form not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)

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

    def test_tag(self):
        """Confirm reported ID"""
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

    def test_is_fresh(self):
        """Confirm return is accurate.

        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic fresh, identification information fresh
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        # Test: InfoId stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, identification information fresh
        assert not target.is_fresh()
        target._stale = False
        target._infoid.set_fresh()
        assert target.is_fresh()
        assert not target._stale

    def test_is_stale(self):
        """Confirm return is accurate.

        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic fresh, identification information fresh
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_set_fresh(self):
        """Confirm all attributes set.

        #. Case: Topic fresh, identification information fresh
        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic stale, identification information stale
         """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()

    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Topic fresh, identification information fresh
        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic stale, identification information stale
         """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MTOPIC.Topic()
        target.init_identity(p_title=TITLE_MODEL)
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Topic stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()


class TestTypes:
    """Unit tests for type definitions in :mod:`.topic`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert MTOPIC.TagTopic is MTYPES.TagTopic
