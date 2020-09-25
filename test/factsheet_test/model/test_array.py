"""
Unit tests for stub array classes.  See :mod:`.array`.
"""
import pytest   # type: ignore[import]

from factsheet.model import array as MARRAY


class TestArray:
    """Unit tests for :class:`.Array`."""

    def test_init(self, patch_args_array):
        """| Confirm initialization.
        | Case: explicit arguments
        """
        # Setup
        ARGS = patch_args_array
        # Test
        target = MARRAY.Array(
            p_rows=ARGS.p_rows, p_cols=ARGS.p_cols, p_styles=ARGS.p_styles,
            p_title=ARGS.p_title, p_symbol_row=ARGS.p_symbol_row,
            p_symbol_col=ARGS.p_symbol_col, p_symbol_entry=ARGS.p_symbol_entry)
        assert target._rows is ARGS.p_rows
        assert target._cols is ARGS.p_cols
        assert ARGS.p_styles == target._styles
        assert ARGS.p_title == target._title
        assert ARGS.p_symbol_row == target._symbol_row
        assert ARGS.p_symbol_col == target._symbol_col
        assert ARGS.p_symbol_entry == target._symbol_entry

    def test_init_default(self, patch_args_array):
        """| Confirm initialization.
        | Case: default arguments
        """
        # Setup
        ARGS = patch_args_array
        TITLE_DEFAULT = 'G'
        SYMBOL_DEFAULT = 'g'
        # Test
        target = MARRAY.Array(
            p_rows=ARGS.p_rows, p_cols=ARGS.p_cols, p_styles=ARGS.p_styles)
        assert TITLE_DEFAULT == target._title
        assert SYMBOL_DEFAULT == target._symbol_row
        assert SYMBOL_DEFAULT == target._symbol_col
        assert SYMBOL_DEFAULT == target._symbol_entry

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_rows', 'rows'),
        ('_cols', 'cols'),
        ('_styles', 'styles'),
        ('_title', 'title'),
        ('_symbol_row', 'symbol_row'),
        ('_symbol_col', 'symbol_col'),
        ('_symbol_entry', 'symbol_entry'),
        ])
    def test_property(self, patch_args_array, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_array
        # Test
        target = MARRAY.Array(
            p_rows=ARGS.p_rows, p_cols=ARGS.p_cols, p_styles=ARGS.p_styles,
            p_title=ARGS.p_title, p_symbol_row=ARGS.p_symbol_row,
            p_symbol_col=ARGS.p_symbol_col, p_symbol_entry=ARGS.p_symbol_entry)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(MARRAY.Array, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
