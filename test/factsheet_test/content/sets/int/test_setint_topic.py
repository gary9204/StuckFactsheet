"""
Unit tests for class for set of integers topic. See
:mod:`~.setint_topic`.
"""
import factsheet.content.sets.int.setint_topic as XSETINT
import factsheet.content.sets.set_topic as XSET
import factsheet.model.element as MELEMENT


class TestSetInt:
    """Unit tests for :class:`~.SetInt`."""

    def test_specialize(self):
        """Confirm specialization of :class:`.Set`."""
        # Setup
        # Test
        assert issubclass(XSETINT.SetInt, XSET.Set)
        assert not issubclass(XSET.Set, XSETINT.SetInt)

    def test_types(self):
        """Confirm support types defined."""
        # Setup
        # Test
        assert XSETINT.ElementInt is MELEMENT.ElementOpaque[int]

    # def test_init(self):
    #     """| Confirm initialization.
    #     | Case: explicit arguments.
    #     """
    #     # Setup
    #     NAME = 'SetInt'
    #     SUMMARY = 'This topic represents a set of integers.'
    #     TITLE = 'Integer Set'
    #     SIZE = 0
    #     # Test
    #     target = XSETINT.SetInt()
    #     assert not target._stale
    #     assert isinstance(target._forms, dict)
    #     assert not target._forms
    #     assert NAME == target.name
    #     assert SUMMARY == target.summary
    #     assert TITLE == target.title
    #     assert SIZE == len(target._elements)
