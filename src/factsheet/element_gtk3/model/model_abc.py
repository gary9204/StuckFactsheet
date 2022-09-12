"""
Define abstract base class for facade classes of storage elements.

.. data:: ExternalOpaque

    Placeholder type hint for model representation that is not specific
    to any user interface toolkit.

.. data:: UiModelOpaque

    Placeholder type hint for a toolkit-specific storage element.
"""
import abc
import logging
import typing

logger = logging.getLogger('Main.element.model')

ExternalOpaque = typing.TypeVar('ExternalOpaque')
UiModelOpaque = typing.TypeVar('UiModelOpaque')


class Consistency(abc.ABC):
    """Abstract interface to track consistency between two representations.

    A class implements interface
    :class:`~.element_gtk.model.model_abc.Consistency` to track an
    object's representation against a target representation.  The
    implementation determines what makes two representations consistent
    (such as equality or equivalence).

    .. admonition:: Maintain

        The initial use for interface
        :class:`~.element_gtk.model.model_abc.Consistency` is to track
        an obejct's representation in memory against its
        representaton in persistent storage.
    """

    @abc.abstractmethod
    def alike(self) -> bool:
        """Return True when self and target are consistent."""

    @abc.abstractmethod
    def differ(self) -> bool:
        """Return True when self and target inconsistent."""

    @abc.abstractmethod
    def set_alike(self):
        """Mark self as consistent with target."""

    @abc.abstractmethod
    def set_differ(self):
        """Mark self as inconsistent with target."""


class Conversion(abc.ABC, typing.Generic[ExternalOpaque]):
    """Abstract interface for conversion between element representations.

    A representation of a storage element may be specific to a user
    interface toolkit.  Call this kind of representation an **internal**
    representation.  A representation of a storage element may not
    rely on any user interface toolkit.  Call this kind of
    representation is an **external** representation.

    :class:`~.element_gtk3.model.model_abc.Conversion` is generic with
    respect to external representation.  A implementation of the
    interface must provide a specific type.  Likewise, the
    implementation determines both the internal and external
    representations.

    .. admonition:: Maintain

        Pickle cannot store GTK 3 objects directly.  A workaround is to
        convert a GTK 3 object to a plain Python representation and
        override a model element's ``__getstate__`` method to replace
        the GTK 3 object with that external representation.  For
        loading, overwrite a model element's ``__setstate__`` method to
        replace the external representation with the corresponding GTK 3
        object.

    .. admonition:: Plan

        GTK 3 has mechanisms to persist objects.  Factsheet uses Pickle
        to reduce dependence on GTK 3.
    """

    @abc.abstractmethod
    def set_internal(self, p_external) -> None:
        """Set storage element from external representation.

        :param p_external: external representation of desired content.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_external(self) -> ExternalOpaque:
        """Return external representation of storage element.
        """
        raise NotImplementedError


class ModelAbc(abc.ABC, typing.Generic[UiModelOpaque]):
    """Abstract base class for facade classes of storage elements.

    :class:`~.element_gtk3.model.model_abc.ModelAbc` is generic with
    respect to storage element type.  A subclass must provide a
    specific storage element type, typically specific to a user
    interface toolkit.
    """

    @abc.abstractmethod
    def new_ui_model(self) -> UiModelOpaque:
        """Return a user interface storage element.

        Use method
        :meth:`~.element_gtk3.model.model_abc.ModelAbc.new_ui_model` in
        the ``__init__`` method of a subclass to create the facade's
        storage element.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def ui_model(self) -> UiModelOpaque:
        """Return underlying storage element.

        Property :attr:`~.element_gtk3.model.model_abc,ModelABC.ui_model`
        is intended only for use by classes in ``element_*`` and
        :mod:`~.factsheet.view` packages.
        """
        raise NotImplementedError


class ModelGtk3(ModelAbc[UiModelOpaque], Conversion[ExternalOpaque],
                typing.Generic[UiModelOpaque, ExternalOpaque]):
    """Abstract base class for facade classes of storage elements.

    See :class:`~.element_gtk3.model.model_abc.Conversion` regarding
    generic type :data:`.ExternalOpaque`.
    See :class:`~.element_gtk3.model.model_abc.ModelAbc` regarding
    generic type :data:`UiModelOpaque`.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other is equivalent to self.

        Two model facades are equivalent when their external
        representations are equal.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self.to_external() != p_other.to_external():
            return False

        return True

    def __getstate__(self) -> typing.Dict[str, typing.Any]:
        """Return content of storage element in form pickle can store.

        A subclass with transient content must extend this method to
        remove such content from the returned state.
        """
        state = self.__dict__.copy()
        state['ex_ui_model'] = self.to_external()
        del state['_ui_model']
        return state

    def __init__(self) -> None:
        """Initialize storage element."""
        self._ui_model = self.new_ui_model()

    def __setstate__(
            self, p_state: typing.MutableMapping[str, typing.Any]) -> None:
        """Reconstruct storage element from content that pickle loads.

        A subclass with transient content must extend this method to
        initialize such content in addition to persistent content.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._ui_model = self.new_ui_model()
        self.set_internal(self.ex_ui_model)   # type: ignore[attr-defined]
        del self.ex_ui_model       # type: ignore[attr-defined]

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self.to_external())

    @property
    def ui_model(self) -> UiModelOpaque:
        return self._ui_model
