"""
Unit test for class to create a heading in Factsheet template outline.
See :mod:`.heading`.
"""
import collections as COL
import pytest   # type: ignore[import]

from factsheet.content import heading as XHEADING


ArgsHeading = COL.namedtuple('ArgsHeading', 'name summary title')
"""Container for clear and convenient reference to stock argument
values.
"""


@pytest.fixture
def patch_args_heading():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.Heading` object."""
    return ArgsHeading(
        name='Inquisition',
        summary='No one expects the Spanish Inquisition!',
        title='The Spanish Inquisition',
        )


class TestHeading:
    """Unit tests for :class:`.Heading`."""

    def test_init(self, patch_args_heading):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_heading
        # Test
        target = XHEADING.Heading(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title)
        assert ARGS.name == target._name
        assert ARGS.summary == target._summary
        assert ARGS.title == target._title

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_name', 'name'],
        ['_summary', 'summary'],
        ['_title', 'title'],
        ])
    def test_property(self, patch_args_heading, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_heading
        target = XHEADING.Heading(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(XHEADING.Heading, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_call(self, patch_args_heading):
        """Confirm call method return."""
        # Setup
        ARGS = patch_args_heading
        target = XHEADING.Heading(
            p_name=ARGS.name, p_summary=ARGS.summary, p_title=ARGS.title)
        # Test
        assert target() is None
