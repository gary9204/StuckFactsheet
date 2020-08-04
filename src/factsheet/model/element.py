"""
Defines generic class for Factsheet-specific implementation of set
element.  See :mod:`.setindexed`.

Each element of a :class:`.SetIndexed` object is a pair: the member of
the abstract set the object represents along with an index.

.. data:: IdStyleElement

    Type for labeling text style to format an element.

.. data:: IndexElement

    Type for labeling members of an abstract set.

.. data:: MemberGeneric

    Generic type for abstract set member.
"""
import typing

IdStyleElement = typing.NewType('IdStyleElement', str)
IndexElement = typing.NewType('IndexElement', int)
MemberGeneric = typing.TypeVar('MemberGeneric')


class ElementGeneric(typing.Generic[MemberGeneric]):
    """Defines an indexed element.

    An element of a :class:`.SetIndexed` object
    represents a member of an abstract set with an index
    (label).  For consistency, the terms "indexed element" and
    "element" refer to a member-index pair.

    :param member: member of new element.
    :param index: index of new element.
    """

    STYLE_DEFAULT = 'Plain'

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other has same member and index.

        :param p_other: object to compare with self.
        """
        try:
            index = p_other.index
            member = p_other.member
        except AttributeError:
            return False

        if self._index != index:
            return False

        if self._member != member:
            return False

        return True

    def __init__(
            self, p_member: MemberGeneric, p_index: IndexElement) -> None:
        self._member = p_member
        self._index = p_index
        self._apply_style: typing.Mapping[str, typing.Callable[[str], str]] = {
            'Label': self.style_label,
            'Element': self.style_element,
            'Index': self.style_index,
            'Member': self.style_member,
            'Plain': self.style_plain,
            }

    def format(self, p_id_style: IdStyleElement,
               p_symbol: str = 'a') -> str:
        """Return element as text in given style.

        .. _Pango markup:
            https://developer.gnome.org/pygtk/stable/
            pango-markup-language.html

        A style may include `Pango markup`_.

        :param p_style_id: identifier of style to use.
        :param p_symbol: symbol to use in label.
        """
        try:
            text = self._apply_style[p_id_style](p_symbol)
        except KeyError:
            text = self._apply_style[self.STYLE_DEFAULT](p_symbol)
        return text

    @property
    def index(self):
        """Return index of element."""
        return self._index

    @property
    def member(self):
        """Return member of element."""
        return self._member

    def ids_style(self) -> typing.Iterator[IdStyleElement]:
        """Return iterator over identifiers of styles the element supports."""
        for id_style in self._apply_style:
            yield IdStyleElement(id_style)

    def style_element(self, p_symbol: str = 'a') -> str:
        r"""Return element as '*symbol*\ :sub:`index` = member'."""
        text = ''.join(['<i>', str(p_symbol), '</i><sub>',
                        str(self.index), '</sub> = ', str(self.member)])
        return text

    def style_index(self, *_args: typing.Any) -> str:
        """Return element as 'index'."""
        return str(self.index)

    def style_label(self, p_symbol: str = 'a') -> str:
        r"""Return element as '*symbol*\ :sub:`index`\ '.

        :param p_symbol: symbol to use in label.
        """
        text = ''.join([
            '<i>', str(p_symbol), '</i><sub>', str(self.index), '</sub>'])
        return text

    def style_member(self, *_args: typing.Any) -> str:
        """Return element as 'member'."""
        return str(self.member)

    def style_plain(self, *_args: typing.Any) -> str:
        """Return element as 'index: member'."""
        text = ''.join([str(self.index), ': ', str(self.member)])
        return text
