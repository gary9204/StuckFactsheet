"""
Abstract model facade, control, and factory classes for formatted text.

This module provides an abstract model facade class for formatted text.
The module includes a corresponding abstract control class.

A subclass may support formatting with manually-entered markup or with
style tags embedded programatically.  The module includes abstract
factory classes for each method of formatting.

.. data:: StorePyTextMarkup

    Type alias for text storage object independent of user interface
    toolkits.
"""
import abc
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC

StorePyTextMarkup = str


class ControlTextAbc(BABC.ControlAbc[StorePyTextMarkup, BABC.StoreUiOpaque],
                     typing.Generic[BABC.StoreUiOpaque]):
    """Abstract class representing transient aspects of text model.

    See :class:`.ModelTextAbc` regarding persistant aspects of model.
    """

    @abc.abstractmethod
    def new_model(self) -> 'ModelTextAbc[BABC.StoreUiOpaque]':
        """Return new text model facade for control initialization.

        Class delegates text model facade construction to each subclass.
        """
        raise NotImplementedError


class ModelTextAbc(BABC.ModelAbc[StorePyTextMarkup, BABC.StoreUiOpaque],
                   typing.Generic[BABC.StoreUiOpaque]):
    """Abstract class representing persistent aspects of text model.

    See :class:`.ControlTextAbc` regarding transient aspects of model.
    """

    @abc.abstractmethod
    def get_store_py(self) -> StorePyTextMarkup:
        """Return model storage as string.

        Return may contain both text and format information.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_store_ui(self, p_store_py: StorePyTextMarkup) -> None:
        """Set facade storage content from string.

        :param p_store_py: text and format information to store.
        """
        raise NotImplementedError


class FactoryMarkupAbc(abc.ABC, typing.Generic[BABC.StoreUiOpaque]):
    """Abstract factory for text facade with manually-entered markup."""

    @abc.abstractmethod
    def __call__(self) -> ModelTextAbc[BABC.StoreUiOpaque]:
        """Return text facade with support for manually-entered markup."""
        raise NotImplementedError


class FactoryStyledAbc(abc.ABC, typing.Generic[BABC.StoreUiOpaque]):
    """Abstract factory for text facade with embedded style tags."""

    @abc.abstractmethod
    def __call__(self) -> ModelTextAbc[BABC.StoreUiOpaque]:
        """Return text facade with support for embedded style tags."""
        raise NotImplementedError
