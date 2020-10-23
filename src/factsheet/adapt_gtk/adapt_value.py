"""
Defines GTK-based adapters and type hints for fact values and formats.
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
AspectValuePlain = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.adapt_value')


class FormatValue(typing.Generic[ValueOpaque, AspectValueOpaque], abc.ABC):
    """Common ancestor of fact value formats.

    A format for a fact value provides the value in a form compatible
    with a GTK display element.  The display element is called an
    aspect.

    Formats have transient data for attached aspects in addition to
    persistant value representation.
    """

    def __getstate__(self) -> typing.Dict:
        """Return format in form pickle can persist.

        Persistent form of format consists of value representation only.
        """
        state = self.__dict__.copy()
        del state['_aspects']
        return state

    def __init__(self, **kwargs: typing.Any) -> None:
        if kwargs:
            raise TypeError('{}.__init__() called with extra argument(s): '
                            '{}'.format(type(self).__name__, kwargs))
        self.__init_transient()
        self.clear()

    def __init_transient(self) -> None:
        """Helper ensures initialization and pickling are consistent."""
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

    @abc.abstractmethod
    def clear(self) -> None:
        """Clear value representation along with attached aspects."""
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

    @abc.abstractmethod
    def set(self, p_value: ValueOpaque) -> None:
        """Set value representation along with attached aspects.

        :param p_value: value to format.
        """
        raise NotImplementedError


class FormatValuePlain(FormatValue[ValueAny, AspectValuePlain]):
    """Plain text format for a fact value.

    :param p_value: fact value to format.
    """

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has equal value representation.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, type(self)):
            return False

        if self._value_gtk != px_other._value_gtk:
            return False

        return True

    def attach_aspect(self, p_aspect: AspectValuePlain) -> None:
        """Add GTK display element to show format.

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

    def clear(self) -> None:
        """Clear value representation along with attached aspects."""
        self._value_gtk = ''
        self._update_aspects()

    def detach_aspect(self, p_aspect: AspectValuePlain) -> None:
        """Remove aspect from format.

        Log warning when requested aspect is not attached.

        :param p_aspect: aspect to remove.
        """
        id_aspect = id(p_aspect)
        try:
            aspect = self._aspects.pop(id_aspect)
        except KeyError:
            logger.warning('Missing aspect: {} ({}.{})'
                           ''.format(hex(id_aspect), self.__class__.__name__,
                                     self.detach_aspect.__name__))
            return

        aspect.hide()

    def set(self, p_value: ValueAny) -> None:
        """Set value representation along with attached aspects.

        :param p_value: value to format.
        """
        self._value_gtk = str(p_value)
        self._update_aspects()

    def _update_aspects(self) -> None:
        """Local helper updates each attached aspect with representation.
        """
        for aspect in self._aspects.values():
            aspect.set_text(self._value_gtk)
