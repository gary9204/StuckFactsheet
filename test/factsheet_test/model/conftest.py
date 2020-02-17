"""
factsheet_test.model.conftest - test fixtures for Model classes.
"""


import pytest   # type: ignore[import]

from factsheet.types_abstract import abc_sheet as ASHEET


@pytest.fixture
def patch_observer_sheet():
    class ObserverSheet(ASHEET.ObserverSheet):
        def __init__(self):
            self.n_changed_name = 0
            self.n_delete_model = 0

        def on_changed_name_sheet(self)->None:
            self.n_changed_name += 1

        def on_delete_model_sheet(self)->None:
            self.n_delete_model += 1

    return ObserverSheet
