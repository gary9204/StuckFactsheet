"""
Unit tests for classes representing sets.  See :mod:`.settag`.
"""
from _collections_abc import dict_keys  # type: ignore[import]
from _collections_abc import dict_values  # type: ignore[import]
import dataclasses as DC
import pytest   # type: ignore[import]
import typing

from factsheet.model import settag as SETTAG


class TestSubsets:
    """Unit tests for subset functions"""

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_0(self):
        """Confirm generation of fixed-sized subsets.
        Case: size 0 subset
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        expect = SETTAG.TaggedSet()
        # Test
        target = list(SETTAG.subsets_size_n(source, 0))
        assert 1 == len(target)
        assert expect in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_1(self):
        """Confirm generation of fixed-sized subsets.
        Case: size 1 subsets
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        elements = list(source)
        expect = []
        for x in elements:
            expect.append({x})
        # Test
        target = [set(s) for s in SETTAG.subsets_size_n(source, 1)]
        assert len(expect) == len(target)
        for s in expect:
            assert s in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_mid(self):
        """Confirm generation of fixed-sized subsets.
        Case: subsets between 1 and set size
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        elements = list(source)
        expect = []
        for x in elements:
            subset = list(elements)
            subset.remove(x)
            expect.append(set(subset))
        # Test
        target = [set(s) for s in SETTAG.subsets_size_n(source, 2)]
        assert len(expect) == len(target)
        for s in expect:
            assert s in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_max(self):
        """Confirm generation of fixed-sized subsets.
        Case: subset size of set
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        expect = source
        # Test
        target = list(SETTAG.subsets_size_n(source, 3))
        assert 1 == len(target)
        assert expect in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_super_max(self):
        """Confirm generation of fixed-sized subsets.
        Case: subset size greater than size of set
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        # Test
        target = list(SETTAG.subsets_size_n(source, 10))
        assert 0 == len(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_size_minus(self):
        """Confirm generation of fixed-sized subsets.
        Case: negative value for set size
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        # Test
        with pytest.raises(ValueError):
            _target = list(SETTAG.subsets_size_n(source, -1))

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_all_empty(self):
        """Confirm generation of subsets.
        Case: all subsets of empty set
        """
        # Setup
        source = SETTAG.TaggedSet()
        expect = SETTAG.TaggedSet()
        # Test
        target = list(SETTAG.subsets_all(source))
        assert 1 == len(target)
        assert expect in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_all_1(self):
        """Confirm generation of subsets.
        Case: all subsets of 1-element set
        """
        values = ['a']
        source = SETTAG.TaggedSet(values)
        elements = list(source)
        expect = [set(), set(elements)]
        # Test
        target = [set(s) for s in SETTAG.subsets_all(source)]
        assert len(expect) == len(target)
        for s in expect:
            assert s in target

    @pytest.mark.skip(reason='Update in progress')
    def test_subset_all(self):
        """Confirm generation of subsets.
        Case: all subsets of set with multiple elements
        """
        # Setup
        values = list('abc')
        source = SETTAG.TaggedSet(values)
        elements = list(source)
        expect = []
        #    - 0-element subset
        expect.append(set())
        #    - 1-element subset
        for x in elements:
            expect.append({x})
        #    - 2-element subset
        for x in elements:
            subset = list(elements)
            subset.remove(x)
            expect.append(set(subset))
        #    - 3-element subset
        expect.append(set(elements))
        # Test
        target = [set(s) for s in SETTAG.subsets_all(source)]
        assert len(expect) == len(target)
        for s in expect:
            assert s in target


@pytest.fixture
def values_abcd():
    return list('abcd')


class TestTaggedSet:
    """Unit tests for class TaggedSet."""

    @pytest.mark.skip(reason='Update in progress')
    def test_contains_domain(self, values_abcd):
        """Confirm contains.
        Case: argument is not a TaggedElement
        """
        # Setup
        non_element = 'This is not an TaggedElement.'
        target = SETTAG.TaggedSet(values_abcd)
        # Test
        assert not target.__contains__(non_element)

    @pytest.mark.skip(reason='Update in progress')
    def test_contains_true(self, values_abcd):
        """Confirm contains.
        Case: element in set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        element_in = SETTAG.TaggedElement(tag=1, value='b')
        # Test
        assert target.__contains__(element_in)

    @pytest.mark.skip(reason='Update in progress')
    def test_contains_false(self, values_abcd):
        """Confirm contains.
        Case: invalid key
        Case: valid key with value mismatch
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        element_out_key = SETTAG.TaggedElement(tag=10, value='b')
        element_out_value = SETTAG.TaggedElement(tag=2, value='a')
        # Test: invalid key
        assert not target.__contains__(element_out_key)
        # Test: valid key with value mismatch
        assert not target.__contains__(element_out_value)

    @pytest.mark.skip(reason='Update in progress')
    def test_init_empty(self):
        """Confirm initialization.
        Case: no values
        """
        # Setup
        target = SETTAG.TaggedSet()
        # Test
        assert target is not None
        assert dict() == target._elements

    @pytest.mark.skip(reason='Update in progress')
    def test_init_values(self, values_abcd):
        """Confirm initialization.
        Case: distinct values
        """
        # Setup
        expect_elements = dict(zip(range(4), values_abcd))
        # Test
        target = SETTAG.TaggedSet(values_abcd)
        assert target is not None
        assert expect_elements.items() == target._elements.items()

    @pytest.mark.skip(reason='Update in progress')
    def test_init_values_dup(self, values_abcd):
        """Confirm initialization.
        Case: values with duplicates
        """
        # Setup
        expect_elements = dict(zip(range(4), values_abcd))
        dup_values = list(values_abcd)
        dup_values.insert(3, 'b')
        # Test
        target = SETTAG.TaggedSet(dup_values)
        assert target is not None
        assert expect_elements.items() == target._elements.items()

    @pytest.mark.skip(reason='Update in progress')
    def test_init_value_none(self, values_abcd):
        """Confirm initialization.
        Case: values with None
        """
        # Setup
        expect_elements = dict(zip(range(4), values_abcd))
        dup_values = list(values_abcd)
        dup_values.insert(1, None)
        # Test
        target = SETTAG.TaggedSet(dup_values)
        assert target is not None
        assert expect_elements.items() == target._elements.items()

    @pytest.mark.skip(reason='Update in progress')
    def test_iter_empty(self):
        """Confirm iterator.
        Case: empty inspect set
        """
        # Setup
        expect_empty = dict()
        target = SETTAG.TaggedSet()
        # Test
        assert expect_empty == dict(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_iter(self, values_abcd):
        """Confirm (element) iterator.
        Case: non-empty inspect set
        """
        # Setup
        expect_elements = dict(enumerate(values_abcd))
        target = SETTAG.TaggedSet(values_abcd)
        # Test
        target_elements = list(target)
        assert isinstance(target_elements[0], SETTAG.TaggedElement)
        assert expect_elements == dict(target_elements)

    @pytest.mark.skip(reason='Update in progress')
    def test_len_empty(self):
        """Confirm length.
        Case: empty set
        """
        # Setup
        target = SETTAG.TaggedSet()
        # Test
        assert 0 == len(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_len_(self, values_abcd):
        """Confirm length.
        Case: non-empty set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        # Test
        assert len(values_abcd) == len(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_str_empty(self):
        """Confirm string representation.
        Case: empty set
        """
        # Setup
        target = SETTAG.TaggedSet()
        expect_string = 'TaggedSet: []'
        # Test
        assert expect_string == str(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_str(self, values_abcd):
        """Confirm string representation.
        Case: non-empty set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        expect_string = 'TaggedSet: ' + str(sorted(enumerate(values_abcd)))
        # Test
        assert expect_string == str(target)

    @pytest.mark.skip(reason='Update in progress')
    def test_new_from_elements_empty(self, values_abcd):
        """Confirm constructed class method.
        Case: empty set
        """
        # Setup
        source = SETTAG.TaggedSet()
        # Test: empty set
        target = SETTAG.TaggedSet.new_from_elements(source)
        assert source == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_from_elements_dup(self, values_abcd):
        """Confirm constructed class method.
        Case: non-empty set with duplicate values
        """
        # Setup
        source = SETTAG.TaggedSet(values_abcd)
        duplicate = SETTAG.TaggedSet(values_abcd)
        duplicate._elements[10] = 'c'
        # Test: non-empty set
        target = SETTAG.TaggedSet.new_from_elements(duplicate)
        assert source == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_from_elements_none(self, values_abcd):
        """Confirm constructed class method.
        Case: non-empty set with None value
        """
        # Setup
        source = SETTAG.TaggedSet(values_abcd)
        with_none = SETTAG.TaggedSet(values_abcd)
        with_none._elements[10] = None
        # Test: non-empty set
        target = SETTAG.TaggedSet.new_from_elements(with_none)
        assert source == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_from_elements(self, values_abcd):
        """Confirm constructed class method.
        Case: non-empty set
        """
        # Setup
        source = SETTAG.TaggedSet(values_abcd)
        # Test: non-empty set
        target = SETTAG.TaggedSet.new_from_elements(source)
        assert source == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_product_set_none(self):
        """Confirm product set constuction.
        Case: no components
        """
        # Setup
        components = []
        expect = SETTAG.TaggedSet()
        # Test:  no components
        target = SETTAG.TaggedSet.new_product_set(components)
        assert expect == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_product_set_singleton(self, values_abcd):
        """Confirm product set constuction.
        Case: one component that is non-empty
        """
        # Setup
        source = SETTAG.TaggedSet(values_abcd)
        components = [source]
        expect = SETTAG.TaggedSet([(x, ) for x in source])
        # Test: one component that is non-empty
        target = SETTAG.TaggedSet.new_product_set(components)
        assert expect == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_product_set_multiple(self):
        """Confirm product set constuction.
        Case: multiple components that are each non-empty
        """
        # Setup
        c_0 = SETTAG.TaggedSet('xyz')
        c_1 = SETTAG.TaggedSet('01')
        c_2 = SETTAG.TaggedSet('abcd')
        components = [c_0, c_1, c_2]
        elements = [(i, j, k) for i in c_0 for j in c_1 for k in c_2]
        expect = SETTAG.TaggedSet(elements)
        # Test: multiple components that are each non-empty
        target = SETTAG.TaggedSet.new_product_set(components)
        assert expect == target

    @pytest.mark.skip(reason='Update in progress')
    def test_new_product_set_empty(self):
        """Confirm product set constuction.
        Case: multiple components one of which is empty
        """
        c_0 = SETTAG.TaggedSet('xyz')
        c_1 = SETTAG.TaggedSet()
        c_2 = SETTAG.TaggedSet('abcd')
        components = [c_0, c_1, c_2]
        expect = SETTAG.TaggedSet()
        # Test: multiple components that are each non-empty
        target = SETTAG.TaggedSet.new_product_set(components)
        assert expect == target

    @pytest.mark.skip(reason='Update in progress')
    def test_tags_empty(self):
        """Confirm dictionary view of tags.
        Case: empty set
        """
        # Setup
        target = SETTAG.TaggedSet()
        # Test
        assert isinstance(target.tags(), dict_keys)
        assert 0 == len(target.tags())

    @pytest.mark.skip(reason='Update in progress')
    def test_tags(self, values_abcd):
        """Confirm dictionary view of tags."""
        # Setup
        target_set = SETTAG.TaggedSet(values_abcd)
        expect_tags = list(range(len(values_abcd)))
        # Test
        assert isinstance(target_set.tags(), dict_keys)
        assert expect_tags == list(target_set.tags())

    @pytest.mark.skip(reason='Update in progress')
    def test_tag_of_domain(self, values_abcd):
        """Confirm value-to-tag correspondence.
        Case: value not in set
        """
        # Setup
        target_set = SETTAG.TaggedSet(values_abcd)
        value = 'Not in target set'
        expect_tag = None
        # Test
        assert expect_tag == target_set.tag_of(value)

    @pytest.mark.skip(reason='Update in progress')
    def test_tag_of(self, values_abcd):
        """Confirm value-to-tag correspondence.
        Case: value in inspect set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        value = 'b'
        expect_tag = 1
        # Test
        assert expect_tag == target.tag_of(value)

    @pytest.mark.skip(reason='Update in progress')
    def test_values_empty(self):
        """Confirm dictionary view of values.
        Case: empty set"""
        # Setup
        target = SETTAG.TaggedSet()
        # Test
        assert isinstance(target.values(), dict_values)
        assert 0 == len(target.values())

    @pytest.mark.skip(reason='Update in progress')
    def test_values(self, values_abcd):
        """Confirm dictionary view of values.
        Case: Non-empty set"""
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        expect_values = list(values_abcd)
        # Test
        assert isinstance(target.values(), dict_values)
        assert expect_values == list(target.values())

    @pytest.mark.skip(reason='Update in progress')
    def test_value_of_domain(self, values_abcd):
        """Confirm tag-to-value correspondence.
        Case: tag not in inspect set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        tag = 10
        expect_value = None
        # Test
        assert expect_value == target.value_of(tag)

    @pytest.mark.skip(reason='Update in progress')
    def test_value_of(self, values_abcd):
        """Confirm tag-to-value correspondence.
        Case: tag in inspect set
        """
        # Setup
        target = SETTAG.TaggedSet(values_abcd)
        tag = 2
        expect_value = 'c'
        # Test
        assert expect_value == target.value_of(tag)


class TestTypes:
    """Unit tests for :mod:`.settag` module-level type definitions."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert SETTAG.Tag is not None
        assert SETTAG.GenericRep is not None


class TestElementGeneric:
    """Unit test fors :class:`.ElementGeneric`."""

    def test_defined(self):
        """Confirm class definition."""
        # Setup
        Element = SETTAG.ElementGeneric[str]
        TAG = SETTAG.Tag(42)
        REP = 'Parrot'
        target = Element(REP, TAG)
        # Test
        assert REP == target.rep
        with pytest.raises(DC.FrozenInstanceError):
            target.rep = REP
        assert TAG == target.tag
        with pytest.raises(DC.FrozenInstanceError):
            target.tag = TAG
