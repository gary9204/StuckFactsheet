"""
Defines abstract classes for content outlines.

Factsheet uses outlines containing templates, topics, forms, and facts.
"""
import abc
import typing

AbstractIndex = typing.TypeVar('AbstractIndex')
AbstractItem = typing.TypeVar('AbstractItem')


class AbstractOutline(abc.ABC, typing.Generic[AbstractIndex, AbstractItem]):
    """Base class for model outlines. """

    @abc.abstractmethod
    def get_item(self, i: AbstractIndex) -> AbstractItem:
        raise NotImplementedError

    @abc.abstractmethod
    def insert_before(self, px_item: AbstractItem,
                      i: AbstractIndex) -> AbstractIndex:
        raise NotImplementedError


class AbstractViewOutline(abc.ABC):
    """TBD"""

    @abc.abstractmethod
    def set_model(self, pm_model:
                  AbstractOutline[AbstractIndex, AbstractItem]) -> None:
        """TBD"""
        raise NotImplementedError
