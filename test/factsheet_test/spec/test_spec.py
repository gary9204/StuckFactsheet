"""
Unit tests for specifications to define topics for Factsheet content.
See :mod:`~.factsheet.spec`.

.. include:: /test/refs_include_pytest.txt
"""
import pytest  # type: ignore[import]


import factsheet.bridge_ui as BUI
import factsheet.spec as SPEC
import factsheet.spec.base_s as BSPEC
import factsheet.spec.sets as SSETS
import factsheet.spec.ops as SOPS


class TestModule:
    """Unit tests for module-level components of :mod:`~.factsheet.spec`."""

    def test_g_spec(self):
        """Confirm definition of specification outline global variable."""
        # Setup
        target = SPEC.g_specs
        model = target._ui_model
        CHILDREN = [next((SSETS.g_specs).items()),
                    next((SOPS.g_specs).items()),
                    ]
        n_children = len(CHILDREN)
        # Test
        assert isinstance(target, BUI.ModelOutlineMulti)
        line_first = next(target.lines())
        assert n_children == model.iter_n_children(line_first)
        assert target.get_item(p_line=line_first) == BSPEC.g_spec_basic
        for i in range(n_children):
            line_child = model.iter_nth_child(line_first, i)
            assert target.get_item(p_line=line_child) is CHILDREN[i]
