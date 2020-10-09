"""
Unit tests for fact abstract interfaces.  See :mod:`.abc_fact`.
"""
import enum

import factsheet.abc_types.abc_fact as ABC_FACT


class TestInterfaceBlockFact:
    """Unit tests for interface :class:`.InterfaceBlockFact`.

    See :mod:`.abc_common` for additional tests to confirm method
    definitions of :class:`.InterfaceBlockFact`.
    """

    pass


class TestInterfaceFact:
    """Unit tests for interface :class:`.InterfaceFact`.

    See :mod:`.abc_common` for additional tests to confirm method and
    property definitions of :class:`.InterfaceFact`.
    """


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_fact`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ABC_FACT.TagFact is not None
        Status = ABC_FACT.StatusOfFact
        assert issubclass(Status, enum.Enum)
        assert Status.BLOCKED
        assert Status.DEFINED
        assert Status.UNCHECKED
        assert Status.UNDEFINED
        assert ABC_FACT.TopicOpaque is not None
        assert ABC_FACT.ValueOpaque is not None
