"""
Defines classes for Factsheet-specific implementation of set-like type.

The classes support a set whose elements are indexed (that is, labeled).
"""

import collections as COL
# import dataclasses as DC
import typing

from factsheet.model import element as MELEMENT

# IndexElement = typing.NewType('IndexElement', int)
MemberGeneric = typing.TypeVar('MemberGeneric')
Element = MELEMENT.ElementGeneric[MemberGeneric]


# @DC.dataclass(frozen=True)
# class ElementGeneric(typing.Generic[MemberGeneric]):
#     """Defines an indexed element.

#     An indexed element represents a member of a set with a label (index)
#     for each member.  For consistency, the terms "indexed element" and
#     "element" refer to a member-index pair.

#     :param member: value of element.
#     :param index: label of element.
#     """
#     member: MemberGeneric
#     index: MELEMENT.IndexElement


class SetIndexed(COL.abc.Set, typing.Generic[MemberGeneric]):
    """Set-like collection with indexed elements.

    Indexed set methods preclude the following:

        * An element with member None.
        * Distinct elements with the equal members.
        * Distinct elements with the equal indecies.

    .. warning:: ``SetIndexed`` provides no interfaces to altered a set
        after construction.  Please do not modify the elements, members,
        and indicies of ``SetIndexed`` instances.

    .. admonition:: About Equality

        Two indexed sets are equivalent when they have the same
        indexed elements (that is, same set of member-index pairs).

    .. admonition:: Work-in-Progress

        Initially, class ``SetIndexed`` only provides features of
        ``set`` necessary for Factsheet.  The implementation starts with
        ``Collection`` methods.  See also Issue #125.

    .. admonition:: Enhancement Opportunity

        The built-in ``set`` class cannot contain non-hashable objects.
        Class ``SetIndexed`` uses indexes, in part, to work around this
        limit.  There are other alternatives. See Issue #124.

    :param p_members: unlabeled values for elements of the set.  Default
       is an empty set.
    """

    def __contains__(self, p_other: typing.Any) -> bool:
        """Return True when object is indexed element in set.

        .. admonition:: Open Question

            The current implementation checks an entire indexed element,
            both member and index.  Should the containment check be
            limited to the member.

            Moreover, should other comparisons be limited to members,
            for example equality?  See Issue #125

        :param p_other: object to test.
        """
        try:
            index = p_other.index
            other_member = p_other.member
        except AttributeError:
            return False

        try:
            member = self._elements[index]
        except KeyError:
            return False

        return member == other_member

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True if other is indexed set with equal elements, or
        False otherwise.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, SetIndexed):
            return False

        return self._elements == p_other._elements

    def __init__(
            self, p_members: typing.Iterable[MemberGeneric] = None) -> None:
        self._elements: typing.Dict[
            MELEMENT.IndexElement, MemberGeneric] = dict()
        if p_members is None:
            return

        index_next = 0
        for member in p_members:
            if member is None:
                continue
            if member in self._elements.values():
                continue
            self._elements[MELEMENT.IndexElement(index_next)] = member
            index_next += 1

    def __iter__(self) -> typing.Iterator[Element]:
        """Return iterator over indexed elements in set."""
        for i, m in self._elements.items():
            element = Element(p_member=m, p_index=i)
            yield element

    def __len__(self) -> int:
        """Return number of elements in set."""
        return len(self._elements)

    def __str__(self) -> str:
        """Return printable representation of set."""
        return '<SetIndexed: ' + str(sorted(self._elements.items())) + '>'

#     def indices(self) -> typing.Iterator[MELEMENT.IndexElement]:
#         """Return iterator over indices of elements in the set."""
#         for i in self._elements.keys():
#             yield i

    def find_element(self, *, p_index: MELEMENT.IndexElement = None,
                     p_member: MemberGeneric = None
                     ) -> typing.Optional[Element]:
        """Return element matching given information or None.

        Return None when no element matches all given information.

        :param p_index: index of desired element.
        :param p_member: member of desired element.
        """
        if p_index is None:
            if p_member is None:
                return None

            for index, member in self._elements.items():
                if member == p_member:
                    element = Element(p_member=member, p_index=index)
                    return element

            return None

        try:
            member = self._elements[p_index]
        except KeyError:
            return None

        element = Element(p_member=member, p_index=p_index)
        if p_member is None:
            return element

        if member == p_member:
            return element

        return None

    @classmethod
    def new_from_elements(cls, p_elements: typing.Iterable[Element] = []
                          ) -> 'SetIndexed[MemberGeneric]':
        """Return set containing given indexed elements.

        Method ``new_from_elements`` enforces the restrictions listed in
        the class description.  The method omits each element with
        member None, with a duplicate index, or with a duplicate member.

        :param p_elements: collection of indexed elements for the set.
        """
        new_set = SetIndexed[MemberGeneric]()
        for element in p_elements:
            index = element.index
            member = element.member
            if member is None:
                continue
            if index in new_set._elements:
                continue
            if member in new_set._elements.values():
                continue
            new_set._elements[index] = member
        return new_set

#     @classmethod
#     def new_product_set(cls, px_components):
#         raise NotImplementedError
#         """Return product set with the given components.

#         Methos new_product_set does not check elements of individual
#         components.  The order of components in the product is the same
#         as the order of presentation.

#         Formal Parameters
#             px_components: component sets
#         """
#         if 0 == len(px_components):
#             return TaggedSet()
#         else:
#             return TaggedSet(IT.product(*px_components))

#     def values(self) -> typing.AbstractSet[Value]:
#         """Return dictionary view of set values."""
#         return self._elements.values()

#     def value_of(self, p_tag: MELEMENT.IndexElement) -> Value:
#         """Return value corresponding to given tag.

#         Formal Parameters
#             p_tag: tag to test.
#         """
#         return self._elements.get(p_tag)


# def subsets_size_n(p_set: TaggedSet, p_n: int) -> typing.Iterator:
#     raise NotImplementedError
#     """Return iterator to subsets of given size.

#     Formal Parameters
#         p_set: source set of elements.
#         p_n: size of subset.
#     """
#     subsets = IT.combinations(p_set, p_n)
#     for s in subsets:
#         yield TaggedSet.new_from_elements(s)


# def subsets_all(p_set: TaggedSet) -> typing.Iterator:
#     raise NotImplementedError
#     """Return iterator to all subsets.

#     Formal Parameters
#         p_set: source set of elements.
#     """
#     for n in range((1 + len(p_set))):
#         for ts in subsets_size_n(p_set, n):
#             yield ts
