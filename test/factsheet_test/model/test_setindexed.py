"""
Unit tests for classes representing indexed sets.  See :mod:`.setindexed`.
"""
# import dataclasses as DC
import pytest   # type: ignore[import]

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET


@pytest.fixture
def patch_members():
    """Pytest fixture returns fixed list for members."""
    return list('abcd')


class TestSetIndexed:
    """Unit tests for :class:`.SetIndexed`."""

    @pytest.mark.parametrize('MEMBER, INDEX, RESULT', [
        ('b', 1, True),
        ('a', -1, False),
        ('z', 0, False),
        ])
    def test_contains(self, patch_members, MEMBER, INDEX, RESULT):
        """| Confirm contains.
        | Case: indexed elements in and not in set.
        """
        # Setup
        Element = MELEMENT.ElementOpaque[str]
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        element = Element(p_member=MEMBER, p_index=INDEX)
        # Test
        assert target.__contains__(element) is RESULT

    def test_contains_domain(self, patch_members):
        """| Confirm contains.
        | Case: argument is not an indexed element.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        NON_ELEMENT = 'Something completely different.'
        # Test
        assert not target.__contains__(NON_ELEMENT)

    @pytest.mark.parametrize('MEMBERS_L, MEMBERS_R, RESULT', [
        ((), (), True),
        ((1,), (), False),
        ((), (1,), False),
        ((1, 2), (1,), False),
        ((1, 2), (2, 1), False),
        ((1, 2, 3), (1, 4, 3), False),
        ((1, 2, 3), (1, 2, 3), True),
        ])
    def test_eq(self, MEMBERS_L, MEMBERS_R, RESULT):
        """ """
        # Setup
        Set = MSET.SetIndexed[str]
        target_left = Set(MEMBERS_L)
        target_right = Set(MEMBERS_R)
        # Test
        assert target_left.__eq__(target_right) is RESULT

    def test_eq_domain(self, patch_members):
        """ """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        SAMPLE = dict(enumerate(patch_members))
        print('Target: {}'.format(target))
        print('Sample: {}'.format(SAMPLE))
        # Test
        assert not target.__eq__(SAMPLE)

    def test_init(self, patch_members):
        """| Confirm initialization.
        | Case: distinct members, none of which are None.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        EXPECT = {
            MELEMENT.IndexElement(i): m for i, m in enumerate(patch_members)}
        # Test
        target = Set(patch_members)
        assert isinstance(target, MSET.SetIndexed)
        assert EXPECT == target._elements

    def test_init_empty(self):
        """| Confirm initialization.
        | Case: no members.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        EXPECT = dict()
        # Test
        target = Set()
        assert EXPECT == target._elements

    def test_init_member_dup(self, patch_members):
        """| Confirm initialization.
        | Case: members include duplicate.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        EXPECT = {
            MELEMENT.IndexElement(i): m for i, m in enumerate(patch_members)}
        MEMBERS_DUP = list(patch_members)
        MEMBERS_DUP.insert(3, 'b')
        # Test
        target = Set(MEMBERS_DUP)
        assert EXPECT == target._elements

    def test_init_member_none(self, patch_members):
        """| Confirm initialization.
        | Case: members include None.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        EXPECT = {
            MELEMENT.IndexElement(i): m for i, m in enumerate(patch_members)}
        MEMBERS_NONE = list(patch_members)
        MEMBERS_NONE.insert(1, None)
        # Test
        target = Set(MEMBERS_NONE)
        assert EXPECT == target._elements

    def test_iter(self, patch_members):
        """| Confirm iterator.
        | Case: non-empty set.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        EXPECT = dict(enumerate(patch_members))
        target = Set(patch_members)
        # Test
        assert EXPECT == {e.index: e.member for e in target}

    def test_iter_empty(self):
        """| Confirm iterator.
        | Case: empty set.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set()
        EXPECT = dict()
        # Test
        assert EXPECT == dict(target)

    def test_len_(self, patch_members):
        """| Confirm set size.
        | Case: non-empty set
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        SIZE = len(patch_members)
        # Test
        assert SIZE == len(target)

    def test_len_empty(self):
        """| Confirm set size.
        | Case: empty set.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set()
        SIZE = 0
        # Test
        assert SIZE == len(target)

    def test_str(self, patch_members):
        """| Confirm string representation.
        | Case: non-empty set.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        EXPECT = '<SetIndexed: ' + str(sorted(enumerate(patch_members))) + '>'
        # Test
        assert EXPECT == str(target)

    def test_str_empty(self):
        """| Confirm string representation.
        | Case: empty set.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set()
        EXPECT = '<SetIndexed: []>'
        # Test
        assert EXPECT == str(target)

    @pytest.mark.parametrize(
        'P_INDEX, P_MEMBER, FOUND, EXPECT_I, EXPECT_M', [
            (None, None, False, None, None),
            (None, 'x', False, None, None),
            (-1, None, False, None, None),
            (1, 'a', False, None, None),
            (2, None, True, 2, 'c'),
            (None, 'b', True, 1, 'b'),
            (3, 'd', True, 3, 'd'),
            ])
    def test_find_element(self, patch_members, P_INDEX, P_MEMBER, FOUND,
                          EXPECT_I, EXPECT_M):
        """Confirm element search."""
        # Setup
        Set = MSET.SetIndexed[str]
        target = Set(patch_members)
        # Test
        element = target.find_element(p_index=P_INDEX, p_member=P_MEMBER)
        if not FOUND:
            assert element is None
        else:
            assert EXPECT_I == element.index
            assert EXPECT_M == element.member

    def test_new_from_elements(self, patch_members):
        """| Confirm construction from elements.
        | Case: distinct elements, none with member None.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        source = Set(patch_members)
        # Test
        target = MSET.SetIndexed.new_from_elements(source)
        assert source == target

    def test_new_from_elements_dup_index(self, patch_members):
        """| Confirm construction from elements.
        | Case: elements with duplicate index.
        """
        # Setup
        Element = MELEMENT.ElementOpaque[str]
        Set = MSET.SetIndexed[str]
        reference = Set(patch_members)
        source = list(reference)
        source.append(Element(p_member='z', p_index=MELEMENT.IndexElement(2)))
        # Test
        target = MSET.SetIndexed.new_from_elements(source)
        assert reference == target

    def test_new_from_elements_dup_member(self, patch_members):
        """| Confirm construction from elements.
        | Case: elements with duplicate member.
        """
        # Setup
        Element = MELEMENT.ElementOpaque[str]
        Set = MSET.SetIndexed[str]
        reference = Set(patch_members)
        source = list(reference)
        source.append(Element(p_member='a', p_index=MELEMENT.IndexElement(-1)))
        # Test
        target = MSET.SetIndexed.new_from_elements(source)
        assert reference == target

    def test_new_from_elements_empty(self):
        """| Confirm construction from elements.
        | Case: no elements.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        source = Set()
        # Test: empty set
        target = MSET.SetIndexed.new_from_elements(source)
        assert source == target

    def test_new_from_elements_none(self, patch_members):
        """| Confirm construction from elements.
        | Case: elements include element with member None.
        """
        # Setup
        Set = MSET.SetIndexed[str]
        reference = Set(patch_members)
        source = MSET.SetIndexed(patch_members)
        source._elements[-1] = None
        # Test
        target = MSET.SetIndexed.new_from_elements(source)
        print('Reference: {}'.format(reference._elements.values()))
        print('Source:    {}'.format(source._elements.values()))
        print('Target:    {}'.format(target._elements.values()))
        assert reference == target

#     def test_new_product_set_none(self):
#         """Confirm product set constuction.
#         Case: no components
#         """
#         # Setup
#         components = []
#         expect = MSET.SetIndexed()
#         # Test:  no components
#         target = MSET.SetIndexed.new_product_set(components)
#         assert expect == target

#     def test_new_product_set_singleton(self, patch_members):
#         """Confirm product set constuction.
#         Case: one component that is non-empty
#         """
#         # Setup
#         source = MSET.SetIndexed(patch_members)
#         components = [source]
#         expect = MSET.SetIndexed([(x, ) for x in source])
#         # Test: one component that is non-empty
#         target = MSET.SetIndexed.new_product_set(components)
#         assert expect == target

#     def test_new_product_set_multiple(self):
#         """Confirm product set constuction.
#         Case: multiple components that are each non-empty
#         """
#         # Setup
#         c_0 = MSET.SetIndexed('xyz')
#         c_1 = MSET.SetIndexed('01')
#         c_2 = MSET.SetIndexed('abcd')
#         components = [c_0, c_1, c_2]
#         elements = [(i, j, k) for i in c_0 for j in c_1 for k in c_2]
#         expect = MSET.SetIndexed(elements)
#         # Test: multiple components that are each non-empty
#         target = MSET.SetIndexed.new_product_set(components)
#         assert expect == target

#     def test_new_product_set_empty(self):
#         """Confirm product set constuction.
#         Case: multiple components one of which is empty
#         """
#         c_0 = MSET.SetIndexed('xyz')
#         c_1 = MSET.SetIndexed()
#         c_2 = MSET.SetIndexed('abcd')
#         components = [c_0, c_1, c_2]
#         expect = MSET.SetIndexed()
#         # Test: multiple components that are each non-empty
#         target = MSET.SetIndexed.new_product_set(components)
#         assert expect == target


class TestTypes:
    """Unit tests for :mod:`.MSET` module-level type definitions."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert MELEMENT.IndexElement is not None
        assert MELEMENT.MemberOpaque is not None


# class TestElementOpaque:
#     """Unit test fors :class:`.ElementOpaque`."""

#     def test_defined(self):
#         """Confirm class definition."""
#         # Setup
#         Element = MELEMENT.ElementOpaque[str]
#         INDEX = MELEMENT.IndexElement(42)
#         MEMBER = 'Parrot'
#         target = Element(p_member=MEMBER, p_index=INDEX)
#         # Test
#         assert MEMBER == target.member
#         with pytest.raises(DC.FrozenInstanceError):
#             target.member = MEMBER
#         assert INDEX == target.index
#         with pytest.raises(DC.FrozenInstanceError):
#             target.index = INDEX


class TestSubsets:
    """Unit tests for subset functions"""

#     def test_subset_size_0(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: size 0 subset
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         expect = MSET.SetIndexed()
#         # Test
#         target = list(MSET.subsets_size_n(source, 0))
#         assert 1 == len(target)
#         assert expect in target

#     def test_subset_size_1(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: size 1 subsets
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         elements = list(source)
#         expect = []
#         for x in elements:
#             expect.append({x})
#         # Test
#         target = [set(s) for s in MSET.subsets_size_n(source, 1)]
#         assert len(expect) == len(target)
#         for s in expect:
#             assert s in target

#     def test_subset_size_mid(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: subsets between 1 and set size
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         elements = list(source)
#         expect = []
#         for x in elements:
#             subset = list(elements)
#             subset.remove(x)
#             expect.append(set(subset))
#         # Test
#         target = [set(s) for s in MSET.subsets_size_n(source, 2)]
#         assert len(expect) == len(target)
#         for s in expect:
#             assert s in target

#     def test_subset_size_max(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: subset size of set
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         expect = source
#         # Test
#         target = list(MSET.subsets_size_n(source, 3))
#         assert 1 == len(target)
#         assert expect in target

#     def test_subset_size_super_max(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: subset size greater than size of set
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         # Test
#         target = list(MSET.subsets_size_n(source, 10))
#         assert 0 == len(target)

#     def test_subset_size_minus(self):
#         """Confirm generation of fixed-sized subsets.
#         Case: negative rep for set size
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         # Test
#         with pytest.raises(repError):
#             _target = list(MSET.subsets_size_n(source, -1))

#     def test_subset_all_empty(self):
#         """Confirm generation of subsets.
#         Case: all subsets of empty set
#         """
#         # Setup
#         source = MSET.SetIndexed()
#         expect = MSET.SetIndexed()
#         # Test
#         target = list(MSET.subsets_all(source))
#         assert 1 == len(target)
#         assert expect in target

#     def test_subset_all_1(self):
#         """Confirm generation of subsets.
#         Case: all subsets of 1-element set
#         """
#         reps = ['a']
#         source = MSET.SetIndexed(reps)
#         elements = list(source)
#         expect = [set(), set(elements)]
#         # Test
#         target = [set(s) for s in MSET.subsets_all(source)]
#         assert len(expect) == len(target)
#         for s in expect:
#             assert s in target

#     def test_subset_all(self):
#         """Confirm generation of subsets.
#         Case: all subsets of set with multiple elements
#         """
#         # Setup
#         reps = list('abc')
#         source = MSET.SetIndexed(reps)
#         elements = list(source)
#         expect = []
#         #    - 0-element subset
#         expect.append(set())
#         #    - 1-element subset
#         for x in elements:
#             expect.append({x})
#         #    - 2-element subset
#         for x in elements:
#             subset = list(elements)
#             subset.remove(x)
#             expect.append(set(subset))
#         #    - 3-element subset
#         expect.append(set(elements))
#         # Test
#         target = [set(s) for s in MSET.subsets_all(source)]
#         assert len(expect) == len(target)
#         for s in expect:
#             assert s in target
