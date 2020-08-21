"""
Unit tests for fact-level model. See :mod:`~.fact`.
"""
import dataclasses as DC
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

from factsheet.model import infoid as MINFOID
from factsheet.model import fact as MFACT


class TestFact:
    """Unit tests for :class:`~.Fact`."""

    @pytest.mark.parametrize('STATE, EXPECT_NONE', [
        (MFACT.StatusOfFact.UNCHECKED, True),
        (MFACT.StatusOfFact.UNDEFINED, True),
        (MFACT.StatusOfFact.DEFINED, False),
        ])
    def test_call(self, patch_args_infoid, STATE, EXPECT_NONE):
        """Confirm call result for each fact check state."""
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact[int](**DC.asdict(ARGS))
        target._value = 'Shropshire Blue'
        target._status = STATE
        expect = None if EXPECT_NONE else target._value
        # Test
        assert target() is expect

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: Equivalence
        """
        # Setup
        # TITLE_SOURCE = 'The Parrot Sketch'
        # source = MFACT.Fact(p_title=TITLE_SOURCE)
        # # Test: type difference
        # assert not source.__eq__(TITLE_SOURCE)
        # # Test: InfoId difference
        # TITLE_TARGET = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_TARGET)
        # assert not source.__eq__(target)
        # # Test: Equivalence
        # target = MFACT.Fact(p_title=TITLE_SOURCE)
        # assert source.__eq__(target)
        # assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_class_block_fact):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        TITLE_MODEL = 'Something completely different.'
        source = MFACT.Fact(p_title=TITLE_MODEL)
        source._stale = True

        PatchBlockFact = patch_class_block_fact
        N_BLOCKS = 3
        blocks = [PatchBlockFact() for _ in range(N_BLOCKS)]
        for block in blocks:
            source.attach_block(block)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert not target._stale
        assert source._infoid == target._infoid

    def test_init(self, patch_args_infoid):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_infoid
        # Test
        target = MFACT.Fact[int](**DC.asdict(ARGS))
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert ARGS.p_name == target._infoid.name
        assert ARGS.p_summary == target._infoid.summary
        assert ARGS.p_title == target._infoid.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = MFACT.Fact()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_status', 'status'),
        # ('_note', 'note'),
        ])
    def test_property(self, patch_args_infoid, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact(**DC.asdict(ARGS))
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.parametrize('NAME_PROP', [
        'name',
        'summary',
        'title',
        ])
    def test_property_infoid(self, NAME_PROP):
        """Confirm pass-through InfoId properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = MFACT.Fact(p_name='Parrot', p_summary='Norwegian Blue',
                            p_title='Parrot Sketch')
        value_attr = getattr(target._infoid, NAME_PROP)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr == value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_check(self, patch_args_infoid):
        """Confirm default check."""
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact(**DC.asdict(ARGS))
        value_pre = target._value
        target.set_fresh()
        # Test
        result = target.check()
        assert target._value is value_pre
        assert target._status is MFACT.StatusOfFact.UNDEFINED
        assert target.is_stale()
        assert result is MFACT.StatusOfFact.UNDEFINED

    def test_clear(self, patch_args_infoid):
        """Confirm default check."""
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact(**DC.asdict(ARGS))
        target._value = 'Something completely different.'
        target._status = MFACT.StatusOfFact.DEFINED
        target.set_fresh()
        # Test
        target.clear()
        assert target._value is MFACT.StatusOfFact.UNCHECKED
        assert target._status is MFACT.StatusOfFact.UNCHECKED
        assert target.is_stale()

    def test_attach_block(self, patch_class_block_fact):
        """Confirm fact block addition.
        Case: block not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MFACT.Fact(p_title=TITLE_MODEL)

        PatchBlockFact = patch_class_block_fact
        N_VIEWS = 3
        blocks = [PatchBlockFact() for _ in range(N_VIEWS)]
        assert blocks[0].get_infoid().title != target._infoid.title
        # # Test
        for block in blocks:
            target.attach_block(block)
            assert target._infoid.title == block.get_infoid().title
            assert target._blocks[id(block)] is block
        assert len(blocks) == len(target._blocks)

    def test_attach_block_warn(
            self, patch_class_block_fact, PatchLogger, monkeypatch):
        """Confirm fact blcok addition.
        Case: block attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MFACT.Fact(p_title=TITLE_MODEL)

        PatchBlockFact = patch_class_block_fact
        N_BLOCKS = 3
        blocks = [PatchBlockFact() for _ in range(N_BLOCKS)]
        assert blocks[0].get_infoid().title != target._infoid.title
        for block in blocks:
            target.attach_block(block)
        assert N_BLOCKS == len(target._blocks)
        I_DUP = 1
        block_dup = blocks[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate fact block: {} (Fact.attach_block)'
            ''.format(hex(id(block_dup))))
        assert not patch_logger.called
        # Test
        target.attach_block(block_dup)
        assert len(blocks) == len(target._blocks)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_all(self, monkeypatch, patch_class_block_fact):
        """Confirm removals."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MFACT.Fact(p_title=TITLE_MODEL)

        PatchBlockFact = patch_class_block_fact
        N_BLOCKS = 3
        blocks = [PatchBlockFact() for _ in range(N_BLOCKS)]
        for block in blocks:
            target.attach_block(block)
        assert N_BLOCKS == len(target._blocks)
        # Test
        target.detach_all()
        assert not target._blocks
        assert N_BLOCKS == patch_detach.n_calls

    # def test_detach_attribute_views(
    #         self, monkeypatch, patch_class_block_fact):
    #     """Confirm removal of attribute views."""
    #     # Setup
    #     class PatchInfoIdModel:
    #         def __init__(self): self.called = False
    #
    #         def detach_view(self, _v): self.called = True
    #
    #     patch_infoid = PatchInfoIdModel()
    #     monkeypatch.setattr(
    #         MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)
    #
    #     TITLE_MODEL = 'Something completely different.'
    #     target = MFACT.Fact(p_title=TITLE_MODEL)
    #
    #     block = patch_class_block_fact()
    #     target.attach_block(block)
    #     # Test
    #     target._detach_attribute_views(block)
    #     assert patch_infoid.called

    def test_detach_block(self, monkeypatch, patch_class_block_fact):
        """Confirm fact block removal.
        Case: block attached initially
        """
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MFACT.Fact(p_title=TITLE_MODEL)

        PatchBlockFact = patch_class_block_fact
        N_BLOCKS = 3
        blocks = [PatchBlockFact() for _ in range(N_BLOCKS)]
        for block in blocks:
            target.attach_block(block)
        N_REMOVE = 1
        I_REMOVE = 1
        block_rem = blocks.pop(I_REMOVE)
        # Test
        target.detach_block(block_rem)
        assert N_REMOVE == patch_infoid.n_calls
        assert len(blocks) == len(target._blocks)
        for block in blocks:
            assert target._blocks[id(block)] is block

    def test_detach_block_warn(
            self, patch_class_block_fact, PatchLogger, monkeypatch):
        """Confirm fact block removal.
        Case: block not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MFACT.Fact(p_title=TITLE_MODEL)

        PatchBlockFact = patch_class_block_fact
        N_BLOCKS = 3
        blocks = [PatchBlockFact() for _ in range(N_BLOCKS)]
        assert blocks[0].get_infoid().title != target._infoid.title
        for block in blocks:
            target.attach_block(block)
        I_DUP = 1
        block_dup = blocks.pop(I_DUP)
        target.detach_block(block_dup)
        assert len(blocks) == len(target._blocks)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing fact block: {} (Fact.detach_block)'
            ''.format(hex(id(block_dup))))
        # Test
        target.detach_block(block_dup)
        assert len(blocks) == len(target._blocks)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_id_fact(self):
        """Confirm return is accurate"""
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MFACT.Fact(p_title=TEXT_TITLE)
        # Test: read
        target_prop = getattr(MFACT.Fact, 'id_fact')
        assert target_prop.fget is not None
        assert target._infoid.id_model == target.id_fact
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_is_fresh(self):
        """Confirm return is accurate.

        #. Case: Fact stale, identification information fresh
        #. Case: Fact fresh, identification information stale
        #. Case: Fact fresh, identification information fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MFACT.Fact(p_title=TEXT_TITLE)
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

        #. Case: Fact stale, identification information fresh
        #. Case: Fact fresh, identification information stale
        #. Case: Fact fresh, identification information fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MFACT.Fact(p_title=TEXT_TITLE)
        # Test: Fact stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_set_fresh(self):
        """Confirm all attributes set.

        #. Case: Fact fresh, identification information fresh
        #. Case: Fact stale, identification information fresh
        #. Case: Fact fresh, identification information stale
        #. Case: Fact stale, identification information stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MFACT.Fact(p_title=TEXT_TITLE)
        # Test: Fact fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Fact stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Fact fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Fact stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()

    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Fact fresh, identification information fresh
        #. Case: Fact stale, identification information fresh
        #. Case: Fact fresh, identification information stale
        #. Case: Fact stale, identification information stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MFACT.Fact(p_title=TEXT_TITLE)
        # Test: Fact fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Fact stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Fact fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Fact stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
