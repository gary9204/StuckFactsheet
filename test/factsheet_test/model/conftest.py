"""
factsheet_test.model.conftest - test fixtures for Model classes.
"""


import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ASHEET


@pytest.fixture
def patch_observer_sheet():
    class ObserverSheet(ASHEET.ObserverSheet):
        def __init__(self):
            self.n_changed_name = 0
            self.n_delete_model = 0

        def update_name(self)->None:
            self.n_changed_name += 1

        def detach(self)->None:
            self.n_delete_model += 1

    return ObserverSheet
