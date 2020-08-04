"""
Defines unit tests for classes to display fact value that is sequence
of integers.  See :mod:`.scene_int`.
"""
import pytest   # type: ignore[import]

# from factsheet.model import setindexed as MSET
from factsheet.model import table as MTABLE
from factsheet.view import scene_table as VTABLE


class TestSceneSynopsisTable:
    """Unit tests for :class:`.SceneSynopsisTable`."""

    def test_init(self, patch_args_table):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_table
        VALUE = MTABLE.TableElements(rows=ARGS.rows, columns=ARGS.columns)
        TEXT = 'Table with 5 rows and 3 columns'
        # Test
        target = VTABLE.SceneSynopsisTable(p_value=VALUE)
        target_gtk = target._label_gtk
        assert TEXT == target_gtk.get_label()


class TestSceneTableauTable:
    """Unit tests for :class:`.SceneTableauTable`.

    Not implemented at present. :class:`.SceneTableau` serves as sample
    at present.
    """

    @pytest.mark.skip(reason='SceneTableau provides adequate sample.')
    def test_init(self, patch_args_table):
        """Confirm initialization."""
        # Setup
        # ARGS = patch_args_table
        # VALUE = MTABLE.TableElements(rows=ARGS.rows, columns=ARGS.columns)
        # TEXT = repr(VALUE)
        # # Test
        # target = VTABLE.SceneTableauTable(p_value=VALUE)
        # target_gtk = target.scene_gtk.get_child()
        # value_text = target._label_gtk.get_label()
        # assert REPR == value_text
        # assert VALUE == int(value_text)


class TestSceneTextTable:
    """Unit tests for :class:`.SceneTextTable`."""

    def test_init(self, patch_args_table):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_table
        VALUE = MTABLE.TableElements(rows=ARGS.rows, columns=ARGS.columns)
        TEXT = repr(VALUE)
        # Test
        target = VTABLE.SceneTextTable(p_value=VALUE)
        target_gtk = target._label_gtk
        assert TEXT == target_gtk.get_label()
