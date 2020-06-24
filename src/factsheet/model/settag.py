"""
Defines classes for Factsheet-specific implementation of set-like type.

The intent is for Factsheet to support sets of mappings and sets of
sets.  Python's built-in ``set`` type cannot represent such sets since
their elements are not hashable.

Module ``settag`` defines classes to represent sets with non-hashable
elements.  The classes are neither a complete nor an efficient
replacement for built-in ``set``.

.. data:: Tag

    Type for marking elements of a tagged set.
"""

import collections as COL
import dataclasses as DC
import itertools as IT
import typing


# Application-specific types
# Tag = int
# Value = typing.Any
TaggedElement = COL.namedtuple('TaggedElement', 'tag, value')


Tag = typing.NewType('Tag', int)
GenericRep = typing.TypeVar('GenericRep')


@DC.dataclass(frozen=True)
class ElementGeneric(typing.Generic[GenericRep]):
    """Defines an element of a tagged set."""
    rep: GenericRep
    tag: Tag


class TaggedSet(COL.abc.Set):
    pass

#     """Set-like collection containing TaggedElements.
# 
#     The built-in set class cannot contain non-hashable objects.  Class
#     TaggedSet provides the parts of the set interface necessary for
#     application Alpha.  TaggedSet accommondates non-hashable values by
#     using TaggedElements, which associates an identifying tag with
#     value.
# 
#     A TaggedSet cannot be altered after construction.  Tag content is an
#     implementation detail, which is subject to change.
# 
#     Class methods
#         new_from_elements: return TaggedSet containing given elements.
# 
#     Public Methods
#         __contains__: return element in set.
#         __init__: initialize set with given values.
#         __iter__: return iterator to elements in set.
#         __len__: return number of elements in set.
#         __str__: return printable representation of set.
#         tags: return set tags.
#         tag_of: return tag corresponding to given value.
#         values: return set values.
#         value_of: return value corresponding to given tag.
#     """
# 
#     def __contains__(self, p_element: TaggedElement) -> bool:
#         """Return element in set.
# 
#         Formal Parameters
#             p_element: element to test.
#         """
#         return p_element in self._elements.items()
# 
#     def __init__(self, p_values: typing.Iterable = []) -> None:
#         """Initialize set with given values.
# 
#         Add elements to the inspect set for the given values.  Ignore
#         None and repeated values.  The method assigns a unique tag to
#         each value.
# 
#         Formal Parameters
#             p_values: collection of values for the set.  Default is an
#                 empty set.
#         """
#         # Initialize default empty set.
#         self._elements = dict()
#         # Add elements
#         tag = 0
#         for value in p_values:
#             if value is None:
#                 continue
#             if value in self._elements.values():
#                 continue
#             self._elements[tag] = value
#             tag += 1
# 
#     def __iter__(self) -> typing.Iterator:
#         """Iterator for elements in set.
# 
#         Iterates over elements, each of which is a TaggedElement.
#         Consequently. Set.__eq__ compares elements rather than just
#         values.
#         """
#         for e in self._elements.items():
#             yield TaggedElement(*e)
# 
#     def __len__(self) -> int:
#         """Return number of elements in set."""
#         return len(self._elements)
# 
#     def __str__(self) -> str:
#         """Return printable representation of set."""
#         return 'TaggedSet: ' + str(sorted(self._elements.items()))
# 
    @classmethod
    def new_from_elements(cls, p_elements):
        raise NotImplementedError
#         """Return TaggedSet containing given elements.
# 
#         new_from_elements enforces the same restriction as __init__on
#         values.
# 
#         Formal Parameters
#             p_elements: collection of elements for the new set.
#         """
#         new_set = TaggedSet()
#         for tag, value in p_elements:
#             if value is None:
#                 continue
#             if value in new_set._elements.values():
#                 continue
#             new_set._elements[tag] = value
#         return new_set
# 
    @classmethod
    def new_product_set(cls, px_components):
        raise NotImplementedError
#         """Return product set with the given components.
# 
#         Methos new_product_set does not check elements of individual
#         components.  The order of components in the product is the same
#         as the order of presentation.
# 
#         Formal Parameters
#             px_components: component sets
#         """
#         if 0 == len(px_components):
#             return TaggedSet()
#         else:
#             return TaggedSet(IT.product(*px_components))
# 
#     def tags(self) -> typing.AbstractSet[Tag]:
#         """Return dictionary view of set tags."""
#         return self._elements.keys()
# 
#     def tag_of(self, p_value: Value) -> Tag:
#         """Return tag corresponding to given value.
# 
#         Formal Parameters
#             p_value: value to test.
#         """
#         for tag, value in self._elements.items():
#             if value == p_value:
#                 return tag
#         return None
# 
#     def values(self) -> typing.AbstractSet[Value]:
#         """Return dictionary view of set values."""
#         return self._elements.values()
# 
#     def value_of(self, p_tag: Tag) -> Value:
#         """Return value corresponding to given tag.
# 
#         Formal Parameters
#             p_tag: tag to test.
#         """
#         return self._elements.get(p_tag)
# 
# 
def subsets_size_n(p_set: TaggedSet, p_n: int) -> typing.Iterator:
    raise NotImplementedError
#     """Return iterator to subsets of given size.
# 
#     Formal Parameters
#         p_set: source set of elements.
#         p_n: size of subset.
#     """
#     subsets = IT.combinations(p_set, p_n)
#     for s in subsets:
#         yield TaggedSet.new_from_elements(s)
# 
# 
def subsets_all(p_set: TaggedSet) -> typing.Iterator:
    raise NotImplementedError
#     """Return iterator to all subsets.
# 
#     Formal Parameters
#         p_set: source set of elements.
#     """
#     for n in range((1 + len(p_set))):
#         for ts in subsets_size_n(p_set, n):
#             yield ts
