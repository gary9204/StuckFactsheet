"""
Defines GTK-based adapters and type hints for fact value formats.
"""
import abc
import gi   # type: ignore[import]
import logging
import typing

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

ValueAny = typing.Any
ValueOpaque = typing.TypeVar('ValueOpaque')
ValueTextGtk = str

AspectValueOpaque = typing.TypeVar('AspectValueOpaque')
AspectValueText = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.adapt_value')


class AdaptValue(typing.Generic[AspectValueOpaque], abc.ABC):
    """Common ancestor of fact value formats.

    A format for a fact value provides the value in a form compatible
    with a GTK display element.  The display element is called a value
    aspect.

    Formats have transient data for attached aspects in addition to
    persistant format content.
    """

    def __getstate__(self) -> typing.Dict:
        """Return format in form pickle can persist.

        Persistent form of format consists of value data only.
        """
        state = self.__dict__.copy()
        del state['_aspects']
        return state

    def __init__(self, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError("AdaptValue.__init__() called with extra "
                            "argument(s): {}".format(kwargs))
        self.__init_transient()

    def __init_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._aspects: typing.MutableMapping[int, AspectValueOpaque] = dict()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct format from state pickle loads.

        Reconstructed format has no aspects attached.

        :param px_state: unpickled state of stored format.
        """
        self.__dict__.update(px_state)
        self.__init_transient()

    @abc.abstractmethod
    def attach_aspect(self, p_aspect: AspectValueOpaque) -> None:
        """Add GTK display element to show format.

        Log warning when requested aspect is already attached.

        :param p_aspect: aspect to add.
        """
        raise NotImplementedError

    def detach_all(self) -> None:
        """Detach all aspects from format."""
        aspects = self._aspects.values()
        while aspects:
            aspect = next(iter(aspects))
            self.detach_aspect(aspect)

    @abc.abstractmethod
    def detach_aspect(self, p_aspect: AspectValueOpaque) -> None:
        """Remove aspect from format.

        Log warning when requested aspect is not attached.

        :param p_aspect: aspect to remove.
        """
        raise NotImplementedError


class AdaptValueText(AdaptValue[AspectValueText]):
    """Plain text format for a fact value.

    :param p_value: fact value to format.
    """

    def __init__(self, *, p_value: ValueAny) -> None:
        super().__init__()
        self._value_gtk = str(p_value)

    def attach_aspect(self, p_aspect: AspectValueText) -> None:
        """Add aspect to display format.

        Log warning when requested aspect is already attached.

        :param p_aspect: aspect to add.
        """
        id_aspect = id(p_aspect)
        if id_aspect in self._aspects.keys():
            logger.warning('Duplicate aspect: {} ({}.{})'
                           ''.format(hex(id_aspect), type(self).__name__,
                                     self.attach_aspect.__name__))
            return

        p_aspect.set_text(self._value_gtk)
        self._aspects[id_aspect] = p_aspect

    def detach_aspect(self, p_aspect: AspectValueOpaque) -> None:
        """Remove aspect from format.

        Log warning when requested aspect is not attached.

        :param p_aspect: aspect to remove.
        """
        pass
        id_aspect = id(p_aspect)
        try:
            aspect = self._aspects.pop(id_aspect)
        except KeyError:
            logger.warning('Missing aspect: {} ({}.{})'
                           ''.format(hex(id_aspect), self.__class__.__name__,
                                     self.detach_aspect.__name__))
            return

        aspect.hide()
