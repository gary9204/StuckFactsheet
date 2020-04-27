"""
Defines abstract classes to represent outlines and their presentations.

:doc:`../guide/devel_notes` describes the use of abstract classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_outline`` defines abstract classes for
outlines of model compoents and corresponding views.

An outline consists of a collection of items.  Factsheet uses outlines
containing templates, topics, forms, and facts. Items may be grouped
into sections. A section consists of an item (called parent) together
with a collection of items (called descendants).  The content of each
item is partitioned into fields.  The meaning of a field's content
depends on the outline. An outline has the same number of fields for
each of its items.

.. data:: GenericIndex

    Generic type for an index of an item within an outline.

.. data:: GenericItem

    Generic type for an item within an outline.

.. data:: GenericOutline

    Generic type for an outline.  Serves as an outline placeholder for
    derived classes.
"""
import abc
import typing

GenericIndex = typing.TypeVar('GenericIndex')
GenericItem = typing.TypeVar('GenericItem')
GenericOutline = typing.TypeVar('GenericOutline')


class AbstractOutline(abc.ABC, typing.Generic[
        GenericIndex, GenericItem, GenericOutline]):
    """Defines interfaces common to outlines of model components.

    .. admonition:: About Equality

        Two outlines are equivalent when they have the same structure
        (fields, items, and sections) and corresponding items are equal.
    """

    @abc.abstractmethod
    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True if other is an outline with same structure and
        content as self.  Otherwise, return False.

        :param px_other: other object to compare to self.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __ne__(self, px_other: typing.Any) -> bool:
        """Return False if other is an outline with same structure and
        content as self.  Otherwise, return True.

        : param px_other: other object to compare to self.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def deepcopy_section_child(self, pm_target: GenericOutline,
                               px_i_source: GenericIndex = None,
                               px_i_target: GenericIndex = None) -> None:
        """Deepcopy section of outline to another outline.

        :param pm_target: outline to copy section to.
        :param px_i_source: index of item to copy along with all
            descendents.  Default is to copy all items.
        :param px_i_target: index in target of copied section.  Default
                is top level after existing top-level items.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def extract_section(self, px_i: GenericIndex) -> None:
        """Remove section from outline.

        :param px_i: index of parent item to remove along with all
            descendants.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_next(
            self, px_target: typing.Any, px_i_after: GenericIndex = None,
            px_derive: typing.Callable[[typing.Any], typing.Any] = (
                lambda v: v)) -> GenericIndex:
        """Return index of next item where the target value equals value
        derived from item's content in given field, or None if no match.

        Search covers entire hierarchy by wrapping at end if necessary.

        :param px_target: search for this value.
        :param px_i_after: start search immediately after item at this
            index.  Default starts search at top item in outline.
        :param px_derive: function to derive value to compare to target
                value.  Function takes input from given field.  Default
                uses field content unaltered.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_item(self, px_i: GenericIndex) -> typing.Optional[GenericItem]:
        """Returns item at given index or None when no item at index.

        :param px_i: index of desired item.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def indices(self, px_i: GenericIndex = None
                ) -> typing.Iterator[GenericIndex]:
        """Return iterator over indices of items in a section.

        The iterator is recursive (that is, includes items from sections
        within a section).

        :param px_i: index of parent item of section.  Default
            iterates over entire outline.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def insert_after(self, px_item: GenericItem,
                     px_i: GenericIndex) -> GenericIndex:
        """Adds item to outline after item at given index.

        If index is None, adds item at beginning of outline.

        :param px_item: new item to add.
        :param px_i: index of item to precede new item.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def insert_before(self, px_item: GenericItem,
                      px_i: GenericIndex) -> GenericIndex:
        """Adds item to outline before item at given index.

        If index is None, adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of item to follow new item.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def insert_child(self, px_item: GenericItem,
                     px_i: GenericIndex) -> GenericIndex:
        """Adds item to outline as child of item at given index.

        Method adds item after all existing children.  If index is None,
        it adds item at end of outline.

        :param px_item: new item to add.
        :param px_i: index of parent item for new item.
        """
        raise NotImplementedError


class AbstractViewOutline(abc.ABC, typing.Generic[
        GenericIndex, GenericOutline]):
    """Defines interfaces common to views of outlines.

    A view of an outline may have one distinguished item.  The
    distinguished item is called the selected item.  The view
    presentation and the effects of user's actions may change depending
    on which item is selected, or if no item is selected.
    """

    @abc.abstractmethod
    def get_selected(self) -> typing.Optional[GenericIndex]:
        """Return the index of the selected item or None when no item
        selected.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def select(self, px_i: GenericIndex = None) -> None:
        """Select the item at the given index.

        :param px_i: index of new selection.  If None, then no item is
            selected.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_model(self, pm_model: GenericOutline) -> None:
        """Associates view with given model.

        :param pm_model: new model for view.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def unselect_all(self) -> None:
        """Clear selection so that no item is selected."""
        raise NotImplementedError
