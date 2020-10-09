"""
Unit tests for identification information type hints and interfaces.

See :mod:`.abc_infoid`.
"""
import factsheet.abc_types.abc_infoid as ABC_INFOID


class TestInterfaceIdentity:
    """Unit tests for :class:`.InterfaceIdentity`.

    See :mod:`.abc_common` for additional tests to confirm property
    definitions of :class:`.InterfaceIdentity`.
    """


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_infoid`."""

    def test_types(self):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert ABC_INFOID.IdNameOpaque is not None
        assert ABC_INFOID.IdSummaryOpaque is not None
        assert ABC_INFOID.TagOpaque is not None
        assert ABC_INFOID.IdTitleOpaque is not None
