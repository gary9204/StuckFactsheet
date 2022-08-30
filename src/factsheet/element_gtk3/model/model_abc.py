"""
Define abstract base class for facade classes of storage elements.

.. data:: UiModelOpaque

    Placeholder type hint for a toolkit-specific storage element.

.. data:: PersistOpaque

    Placeholder type hint for model representation suitable
    for persistent storage.
"""
import abc
import logging
import typing

logger = logging.getLogger('Main.element.model')

UiModelOpaque = typing.TypeVar('UiModelOpaque')
PersistOpaque = typing.TypeVar('PersistOpaque')


class Consistency:
    pass


class Conversion:
    pass


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


class ModelGtk3(ModelAbc[UiModelOpaque],
                typing.Generic[UiModelOpaque, PersistOpaque]):
    """Abstract base class for facade classes of storage elements.

    :class:`~.element_gtk3.model.model_abc.ModelGtk3` is generic with
    respect to toolkit storage element.  A subclass must provide a
    specific storage element type and override
    :meth:`~.element_gtk3.model.model_abc.ModelGtk3.new_ui_model` to
    return storage of that type. For example, see
    :class:`.element_gtk3.model.text.ModelText`.

    :class:`~.element_gtk3.model.model_abc.ModelGtk3` is generic with
    respect to persistent storage.  A subclass must provide a specific
    type that ``Pickle`` can store and load.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other is equivalent to self.

        Two model facades are equivalent when their persistent forms are
        equal.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self.get_persist() != p_other.get_persist():
            return False

        return True

    def __getstate__(self) -> typing.Dict[str, typing.Any]:
        """Return content of storage element in form pickle can store.

        A subclass with transient content must extend this method to
        remove such content from the returned state.
        """
        state = self.__dict__.copy()
        state['ex_ui_model'] = self.get_persist()
        del state['_ui_model']
        return state

    def __init__(self) -> None:
        """Initialize storage element."""
        self._ui_model = self.new_ui_model()

    def __setstate__(
            self, p_state: typing.MutableMapping[str, typing.Any]) -> None:
        """Reconstruct storage element from content that pickle loads.

        A subclass with transient content must extend this method to
        initialize such content in addition to prsistent content.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._ui_model = self.new_ui_model()
        self.set_persist(self.ex_ui_model)   # type: ignore[attr-defined]
        del self.ex_ui_model       # type: ignore[attr-defined]

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self.get_persist())

    @abc.abstractmethod
    def get_persist(self) -> PersistOpaque:
        """Return storage element in form suitable for persistent storage."""
        raise NotImplementedError

    # @abc.abstractmethod
    # def new_ui_model(self) -> UiModelOpaque:
    #     """Return a user interface storage element.
    #
    #     Method :meth:`~.element_gtk3.model.model_abc.ModelGtk3.__init__`
    #     uses :meth:`~.element_gtk3.model.model_abc.ModelGtk3.new_ui_model`
    #     to create the facade's storage element.  This method is intended
    #     for overriding rather than for external use.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def set_persist(self, p_persist: PersistOpaque) -> None:
        """Set storage element from content in persistent form.

        :param p_persist: persistent form for storage element content.
        """
        raise NotImplementedError

    @property
    def ui_model(self) -> UiModelOpaque:
        """Return underlying user interface storage element.

        Property :attr:`~.element_gtk3.model.model_abc,ModelGtk3.ui_model`
        is intended only for use by classes in packages element and
        view.
        """
        return self._ui_model
