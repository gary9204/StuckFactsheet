"""
Abstract facade and interface classes for model and control cp,[pmemts.

This module provides an abstract facade class for a model component. A
concrete subclass may implement the facade with a user interface toolkit
object or a Pyhton object.  The module includes a corresponding
abstract control class.  Abstract interfaces partition control
functions.

.. data:: StorePyOpaque

    Type variable for storage object independent of user interface
    toolkits.  The storage object is a Python object.  The type variable
    serves as parameter for generic classes.

.. data:: StoreUiOpaque

    Type variable for storage object specific to a user interface
    toolkit.  The object may be a tookit component or a Python object,
    depending on the toolkit.  The type variable serves as parameter for
    generic classes.
"""

import abc
import typing

StorePyOpaque = typing.TypeVar('StorePyOpaque')
StoreUiOpaque = typing.TypeVar('StoreUiOpaque')


class BypassAbc(abc.ABC):
    """Abstract interface to bypass model facade and control classes.

    An user interface toolkit may provide mechanisms for communication
    between storage and view components.  This interface exposes a
    model's storage component for direct connection to a toolkit view.
    """

    @abc.abstractmethod
    def bypass(self) -> StoreUiOpaque:
        """Return user interface toolkit storage component for a model."""
        raise NotImplementedError


class ControlAbc(abc.ABC, typing.Generic[StorePyOpaque, StoreUiOpaque]):
    """Abstract class representing transient aspects of model.

    See :class:`.ModelAbc` regarding persistant aspects of model.
    """

    def __init__(self, p_model: 'ModelAbc[StorePyOpaque, StoreUiOpaque]'
                 = None) -> None:
        """Initialize model component of control.

        A control manages one model component and one or more view
        components.  The control may relay user requests from views to
        its model.  The control may update views in response to changes
        in its model.

        :param p_model: model to associate with this control.  If None,
            create a new model.
        """
        if p_model is None:
            self._model = self.new_model()
        else:
            self._model = p_model

    @abc.abstractmethod
    def on_model_change(self) -> None:
        """Update transient aspects of model.

        Update may include tracking changes (see
        :class:`.TrackChangesAbc`) or notifying observers (see
        :class:`.SubjectAbc` and :class:`.ObserverAbc`).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_model(self) -> 'ModelAbc[StorePyOpaque, StoreUiOpaque]':
        """Return new model facade for control initialization.

        Class delegates model facade construction to each subclass.
        """
        raise NotImplementedError


class ModelAbc(abc.ABC, typing.Generic[StorePyOpaque, StoreUiOpaque]):
    """Abstract facade class representing persistent aspects of model.

    See :class:`.ControlAbc` regarding transient aspects of model.

    .. note::

        Two model facades are equivalent when their toolkit-independent
        storage objects are equal.  Their corresponding controls may
        differ.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other is equivalent to self.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self.get_store_py() != p_other.get_store_py():
            return False

        return True

    def __getstate__(self) -> typing.Dict[str, typing.Any]:
        """Return model facade in form pickle can store.

        The returned object does not include transient aspects of the
        model.  In particular, the return does not include the control
        corresponding to the model.

        A subclass with transient content must extend this method to
        remove such content from the returned object.
        """
        state = self.__dict__.copy()
        state['ex_store'] = self.get_store_py()
        del state['_store_ui']
        # del state['_control']
        return state

    def __init__(self) -> None:
        """Initialize storage for model."""
        # if p_control is None:
        #     self._control = self.new_control()
        # else:
        #     self._control = p_control
        self._store_ui = self.new_store_ui()

    def __setstate__(
            self, p_state: typing.MutableMapping[str, typing.Any]) -> None:
        """Reconstruct model facade from content that pickle loads.

        The retruned model facade includes a new control.

        A subclass with transient content must extend this method to
        initialize such content in addition to persistent content.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._store_ui = self.new_store_ui()
        self.set_store_ui(self.ex_store)   # type: ignore[attr-defined]
        del self.ex_store  # type: ignore[attr-defined]
        # self._control = self.new_control()

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self.get_store_ui())

    # def get_control(self) -> 'ControlAbc[StorePyOpaque, StoreUiOpaque]':
    #     """Return control associated with this model facade"""
    #     return self._control

    @abc.abstractmethod
    def get_store_py(self) -> StorePyOpaque:
        """Return model storage as toolkit-independent object."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_store_ui(self) -> StoreUiOpaque:
        """Return model storage as toolkit-specific object."""
        raise NotImplementedError

    # @abc.abstractmethod
    # def new_control(self) -> ControlAbc[StorePyOpaque, StoreUiOpaque]:
    #     """Return new control for this model facade for initialization.
    #
    #     Class delegates control construction to each subclass.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def new_store_ui(self) -> StoreUiOpaque:
        """Return new storage object for model facade for initialization.

        Class delegates storage object construction to each subclass.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_store_ui(self, p_store_py: StorePyOpaque) -> None:
        """Set facade storage content from toolkit-independent object.

        :param p_store_py: toolkit-independent model storage object.
        """
        raise NotImplementedError


class ObserverAbc(abc.ABC, typing.Generic[StoreUiOpaque]):
    """Abstract interface for :class:`.SubjectAbc` to notify an observer.

    An observer must register with a subject in order to receive
    notification.  See :meth:`.SubjectAbc.attach`.
    """

    @abc.abstractmethod
    def on_notice(self, p_store_ui: StoreUiOpaque, **kwargs: typing.Any
                  ) -> None:
        """Respond to notification from the observer's subject.

        :param p_store_ui: user interface toolkit storage component for
            subject.
        :param kwargs: keyword parameters for extensions.
        """
        raise NotImplementedError


class SubjectAbc(abc.ABC):
    """Abstract interface for the subject of one or more observers.
    A subject notifies each :class:`.ObserverAbc` attached to the
    subject.
    """

    @abc.abstractmethod
    def attach(self, p_observer: ObserverAbc) -> None:
        """Start notifying an observer.

        :param p_observer: start to notify this observer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self, p_observer: ObserverAbc) -> None:
        """Stop notifying an observer.

        :param p_observer: cease to notify this observer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self) -> None:
        """Notify all observers."""
        raise NotImplementedError


class TrackChangesAbc(abc.ABC):
    """Abstract interface to track whether an object has changed.

    Each subclass should document what constitutes a change in an object
    of that class.

    This base class does not include interfaces for history of changes
    (for example, recording or undoing changes).
    """

    @abc.abstractmethod
    def has_changed(self) -> bool:
        """Return True if and only if object has changed."""
        raise NotImplementedError

    @abc.abstractmethod
    def has_not_changed(self) -> bool:
        """Return True if and only if object has not changed."""
        raise NotImplementedError

    @abc.abstractmethod
    def mark_changed(self) -> None:
        """Mark object as changed"""
        raise NotImplementedError

    @abc.abstractmethod
    def mark_not_changed(self) -> None:
        """Mark object as not changed."""
        raise NotImplementedError
