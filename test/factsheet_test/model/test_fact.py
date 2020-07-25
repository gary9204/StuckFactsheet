"""
Unit tests for fact-level model. See :mod:`~.fact`.
"""
import dataclasses as DC
# import logging
# from pathlib import Path
# import pickle
import pytest   # type: ignore[import]

from factsheet.model import infoid as MINFOID
from factsheet.model import fact as MFACT


class TestFact:
    """Unit tests for :class:`~.Fact`."""

    @pytest.mark.parametrize('STATE, EXPECT_NONE', [
        (MFACT.StateOfCheck.UNCHECKED, True),
        (MFACT.StateOfCheck.UNDEFINED, True),
        (MFACT.StateOfCheck.CHECKED, False),
        ])
    def test_call(self, patch_args_infoid, STATE, EXPECT_NONE):
        """Confirm call result for each fact check state."""
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact[int](**DC.asdict(ARGS))
        target._value = 'Shropshire Blue'
        target._state_of_check = STATE
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

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_get_set_state(self, tmp_path, interface_pane_fact):
        """Confirm conversion to and from pickle format."""
        # Setup
        # path = Path(str(tmp_path / 'get_set.fsg'))

        # TITLE_MODEL = 'Something completely different.'
        # source = MFACT.Fact(p_title=TITLE_MODEL)
        # source._stale = True

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # for view in views:
        #     source.attach_view(view)
        # # Test
        # with path.open(mode='wb') as io_out:
        #     pickle.dump(source, io_out)

        # with path.open(mode='rb') as io_in:
        #     target = pickle.load(io_in)

        # assert isinstance(target._views, dict)
        # assert not target._views
        # assert not target._stale
        # assert source._infoid == target._infoid

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
        assert target._state_of_check is MFACT.StateOfCheck.UNCHECKED
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # # Test
        target = MFACT.Fact()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_state_of_check', 'state_of_check'),
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
        assert target._state_of_check is MFACT.StateOfCheck.UNDEFINED
        assert target.is_stale()
        assert result is MFACT.StateOfCheck.UNDEFINED

    def test_clear(self, patch_args_infoid):
        """Confirm default check."""
        # Setup
        ARGS = patch_args_infoid
        target = MFACT.Fact(**DC.asdict(ARGS))
        target._value = 'Something completely different.'
        target._state_of_check = MFACT.StateOfCheck.CHECKED
        target.set_fresh()
        # Test
        target.clear()
        assert target._value is None
        assert target._state_of_check is MFACT.StateOfCheck.UNCHECKED
        assert target.is_stale()

    @pytest.mark.parametrize('NAME_PROP', [
        # 'name',
        # 'summary',
        # 'title',
        ])
    def test_property_infoid(self, NAME_PROP):
        """Confirm pass-through InfoId properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        # target = MFACT.Fact(p_name='Parrot', p_summary='Norwegian Blue',
        #                       p_title='Parrot Sketch')
        # value_attr = getattr(target._infoid, NAME_PROP)
        # target_prop = getattr(MFACT.Fact, NAME_PROP)
        # value_prop = getattr(target, NAME_PROP)
        # # Test: read
        # assert target_prop.fget is not None
        # assert value_attr == value_prop
        # # Test: no replace
        # assert target_prop.fset is None
        # # Test: no delete
        # assert target_prop.fdel is None

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_attach_view(self, interface_pane_fact):
        """Confirm view addition.
        Case: view not attached initially
        """
        # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # assert views[0].get_infoid().title != target._infoid.title
        # # Test
        # for view in views:
        #     target.attach_view(view)
        #     assert target._infoid.title == view.get_infoid().title
        #     assert target._views[id(view)] is view
        # assert len(views) == len(target._views)

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_attach_view_warn(
            self, interface_pane_fact, PatchLogger, monkeypatch):
        """Confirm view addition.
        Case: view attached initially
        """
        # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # assert views[0].get_infoid().title != target._infoid.title
        # for view in views:
        #     target.attach_view(view)
        # assert N_VIEWS == len(target._views)
        # I_DUP = 1
        # view_dup = views[I_DUP]

        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = (
        #     'Duplicate view: {} (Fact.attach_view)'
        #     ''.format(hex(id(view_dup))))
        # assert not patch_logger.called
        # # Test
        # target.attach_view(view_dup)
        # assert len(views) == len(target._views)
        # assert patch_logger.called
        # assert PatchLogger.T_WARNING == patch_logger.level
        # assert log_message == patch_logger.message

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_detach_all(self, monkeypatch, interface_pane_fact):
        """Confirm removals."""
        # Setup
        # class PatchInfoIdModel:
        #     def __init__(self): self.n_calls = 0

        #     def detach_view(self, _v): self.n_calls += 1

        # patch_detach = PatchInfoIdModel()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # for view in views:
        #     target.attach_view(view)
        # assert N_VIEWS == len(target._views)
        # # Test
        # target.detach_all()
        # assert not target._views
        # assert N_VIEWS == patch_detach.n_calls

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_detach_view(self, monkeypatch, interface_pane_fact):
        """Confirm view removal.
        Case: view attached initially
        """
        # Setup
        # class PatchInfoIdModel:
        #     def __init__(self): self.n_calls = 0

        #     def detach_view(self, _v): self.n_calls += 1

        # patch_infoid = PatchInfoIdModel()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # for view in views:
        #     target.attach_view(view)
        # N_REMOVE = 1
        # I_REMOVE = 1
        # view_rem = views.pop(I_REMOVE)
        # # Test
        # target.detach_view(view_rem)
        # assert N_REMOVE == patch_infoid.n_calls
        # assert len(views) == len(target._views)
        # for view in views:
        #     assert target._views[id(view)] is view

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_detach_attribute_views(
            self, monkeypatch, interface_pane_fact):
        """Confirm removal of attribute views."""
        # Setup
        # class PatchInfoIdModel:
        #     def __init__(self): self.called = False

        #     def detach_view(self, _v): self.called = True

        # patch_infoid = PatchInfoIdModel()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # view = interface_pane_fact()
        # target.attach_view(view)
        # Test
        # target._detach_attribute_views(view)
        # assert patch_infoid.called

    @pytest.mark.skip(reason='Implementation in progress.')
    def test_detach_view_warn(
            self, interface_pane_fact, PatchLogger, monkeypatch):
        """Confirm view removal.
        Case: view not attached initially
        """
        # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MFACT.Fact(p_title=TITLE_MODEL)

        # N_VIEWS = 3
        # views = [interface_pane_fact() for _ in range(N_VIEWS)]
        # assert views[0].get_infoid().title != target._infoid.title
        # for view in views:
        #     target.attach_view(view)
        # I_DUP = 1
        # view_dup = views.pop(I_DUP)
        # target.detach_view(view_dup)
        # assert len(views) == len(target._views)

        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = (
        #     'Missing view: {} (Fact.detach_view)'
        #     ''.format(hex(id(view_dup))))
        # Test
        # target.detach_view(view_dup)
        # assert len(views) == len(target._views)
        # assert patch_logger.called
        # assert PatchLogger.T_WARNING == patch_logger.level
        # assert log_message == patch_logger.message

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
