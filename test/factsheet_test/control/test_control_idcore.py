"""
Unit tests for generic control to add views of :class:`~.IdCore`
identity attributes.  See :mod:`~.control_idcore`.
"""
import pytest   # type: ignore[import]

import factsheet.control.control_idcore as CIDCORE
import factsheet.model.idcore as MIDCORE


PatchControl = CIDCORE.ControlIdCore[
    MIDCORE.ViewNameActive, MIDCORE.ViewNamePassive,
    MIDCORE.ViewSummaryActive, MIDCORE.ViewSummaryPassive,
    MIDCORE.ViewTitleActive, MIDCORE.ViewTitlePassive]


class TestControlIdCore:
    """Unit tests for :class:`.ControlIdCore`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (CIDCORE.ControlIdCore, 'new_view_name_active'),
        (CIDCORE.ControlIdCore, 'new_view_name_passive'),
        (CIDCORE.ControlIdCore, 'new_view_summary_active'),
        (CIDCORE.ControlIdCore, 'new_view_summary_passive'),
        (CIDCORE.ControlIdCore, 'new_view_title_active'),
        (CIDCORE.ControlIdCore, 'new_view_title_passive'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__
