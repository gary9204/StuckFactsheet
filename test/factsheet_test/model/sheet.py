"""
factsheet_test.model.sheet - unit tests for Model class Sheet.
"""


# from factsheet.types_abstract import abc_sheet as ASHEET
from factsheet.model import sheet as MSHEET


class TestSheet:
    """Unit tests for Model class Sheet."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = MSHEET.Sheet()
        assert dict() == target._observers
        assert not target._unsaved_changes

    def test_add_observer(self, patch_observer_sheet):
        """Confirm addition of observer.
        Case: add novel observer
        """
        # Setup
        N_OBS = 3
        observers = [patch_observer_sheet() for _ in range(N_OBS)]
        target = MSHEET.Sheet()
        # Test
        for obs in observers:
            target.add_observer(obs)
            assert target._observers[id(obs)] is obs
        assert N_OBS == len(target._observers)

    def test_add_observer_dup(self):
        """Confirm addition of observer.
        Case: log duplicate observer
        """
        # Setup
        # Test
#         assert False

    def test_delete_sheet(self, patch_observer_sheet):
        """Confirm notifications and removals."""
        # Setup
        N_OBS = 3
        observers = [patch_observer_sheet() for _ in range(N_OBS)]
        N_CALLS = 1
        target = MSHEET.Sheet()
        for obs in observers:
            target.add_observer(obs)
        # Test
        target.delete_sheet()
        assert 0 == len(target._observers)
        for obs in observers:
            assert N_CALLS == obs.n_delete_model

    def test_remove_observer(self, patch_observer_sheet):
        """Confirm removal of observer.
        Case: remove observer
        """
        # Setup
        N_OBS = 3
        observers = [patch_observer_sheet() for _ in range(N_OBS)]
        target = MSHEET.Sheet()
        for obs in observers:
            target.add_observer(obs)
        I_OBS_T = 1
        obs_t = observers.pop(I_OBS_T)
        # Test
        target.remove_observer(obs_t)
        assert (N_OBS - 1) == len(target._observers)
        for obs in observers:
            assert target._observers[id(obs)] is obs

    def test_remove_observer_missing(self):
        """Confirm removal of observer.
        Case log missing observer
        """
        # Setup
        # Test
#         assert False

    def test_unsaved_changes(self):
        """Confirm change report.
        Case: no unsaved changes
        Case: some uncaved change
        # Test: no unsaved changes
        # Test: some uncaved change
        """
        # Setup
        target = MSHEET.Sheet()
        # Test: no unsaved changes
        assert not target.unsaved_changes()
        # Test: some uncaved change
        target._unsaved_changes = True
        assert target.unsaved_changes()
