"""
Unit tests for class representing indexed element. See :mod:`.element`.
"""
import collections.abc as ABC_COL
import dataclasses as DC
import pytest   # type: ignore[import]

from factsheet.model import element as MELEMENT


@DC.dataclass
class ArgsElement:
    """Convenience class assembles arguments to
    :meth:`.ElementGeneric.__init__` for pytest fixture.
    """
    p_member: int
    p_index: MELEMENT.IndexElement


@pytest.fixture
def patch_args_element():
    return ArgsElement(
        p_member=42,
        p_index=MELEMENT.IndexElement(6),
        )


class TestStyle:
    """Unit tests for :class:`.Style`."""

    def test_eq(self, patch_args_element):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: name difference
        #. Case: Equivalence
        """
        # Setup
        NAME = MELEMENT.IdStyle('Norwegian Blue')
        NAME_DIFF = MELEMENT.Style(p_name='Something completely different')
        reference = MELEMENT.Style(p_name=NAME)
        # Test: type difference
        target = MELEMENT.Style(p_name=NAME_DIFF)
        assert not target.__eq__('Something completely different')
        # Test: name difference
        target = MELEMENT.Style(p_name=NAME_DIFF)
        assert not target.__eq__(reference)
        # Test: Equivalence
        target = MELEMENT.Style(p_name=NAME)
        assert target.__eq__(reference)
        assert not target.__ne__(reference)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = MELEMENT.IdStyle('Norwegian Blue')
        # Test
        target = MELEMENT.Style(p_name=NAME)
        assert NAME == target.name


class TestTypes:
    """Unit tests for :mod:`.element` module-level type definitions."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert MELEMENT.IdStyle is not None
        assert MELEMENT.IndexElement is not None
        assert MELEMENT.MemberGeneric is not None


class TestElementGeneric:
    """Unit tests for :class:`.ElementGeneric`."""

    def test_eq(self, patch_args_element):
        """Confirm equivalence operator

        #. Case: type difference - no index
        #. Case: type difference - no member
        #. Case: index difference
        #. Case: member difference
        #. Case: Equivalence
        """
        # Setup
        class Other:
            pass

        ARGS = patch_args_element
        target = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        # Test: type difference - no index
        other = Other()
        assert not target.__eq__(other)
        # Test: type difference - no member
        other = Other()
        other.index = "Something completely different"
        assert not target.__eq__(other)
        # Test: index difference - no mbmber
        other = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        other._index = MELEMENT.IndexElement(3)
        assert not target.__eq__(other)
        # Test: member difference
        other = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        other._member = 21
        assert not target.__eq__(other)
        # Test: equivalence
        other = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        assert not target.__ne__(other)
        assert target.__eq__(other)

    def test_init(self, patch_args_element):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_element
        # Test
        target = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        assert ARGS.p_member == target._member
        assert ARGS.p_index == target._index

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_member', 'member'],
        ['_index', 'index'],
        ])
    def test_property(self, patch_args_element, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_element
        target = MELEMENT.ElementGeneric(**DC.asdict(ARGS))
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(MELEMENT.ElementGeneric, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.parametrize('ID_STYLE, SYMBOL, EXPECT', [
        ('Label', 'g', '<i>g</i><sub>6</sub>'),
        ('Element', 'g', '<i>g</i><sub>6</sub> = 42'),
        ('Index', 'g', '6'),
        ('Member', 'g', '42'),
        ('Plain', 'g', '6: 42'),
        ('Oops!', 'g', '6: 42'),
        ])
    def test_format(self, patch_args_element, ID_STYLE, SYMBOL, EXPECT):
        """| Confirm invocation of each style.
        | Case: with symbol.
        """
        # Setup
        ARGS = patch_args_element
        target = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        # Test
        actual = target.format(p_id_style=ID_STYLE, p_symbol=SYMBOL)
        assert EXPECT == actual

    @pytest.mark.parametrize('ID_STYLE, EXPECT', [
        ('Label', '<i>a</i><sub>6</sub>'),
        ('Element', '<i>a</i><sub>6</sub> = 42'),
        ('Index', '6'),
        ('Member', '42'),
        ('Plain', '6: 42'),
        ('Oops!', '6: 42'),
        ])
    def test_format_default(self, patch_args_element, ID_STYLE, EXPECT):
        """| Confirm invocation of each style.
        | Case: without symbol.
        """
        # Setup
        ARGS = patch_args_element
        target = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        # Test
        actual = target.format(p_id_style=ID_STYLE)
        assert EXPECT == actual

    def test_style_ids(self, patch_args_element):
        """Confirm style iterations"""
        # Setup
        IDS = ['Label', 'Element', 'Index', 'Member', 'Plain']
        ARGS = patch_args_element
        target = MELEMENT.ElementGeneric[int](**DC.asdict(ARGS))
        # Test
        result = target.ids_style()
        assert isinstance(result, ABC_COL.Iterator)
        assert IDS == list(result)
