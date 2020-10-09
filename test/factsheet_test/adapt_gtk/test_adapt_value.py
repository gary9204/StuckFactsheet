"""
Unit tests for value format adapters and type hints.  See
:mod:`~.adapt_value`.
"""
import logging
from pathlib import Path
import pickle
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import re
import typing

import factsheet.adapt_gtk.adapt_value as AVALUE

from factsheet.adapt_gtk.adapt_value import AspectValueOpaque
from factsheet.adapt_gtk.adapt_value import AspectValueText

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchAdaptValue(AVALUE.AdaptValue[typing.Any]):
    """Class with stub for methods abstract in :class:`.AdaptValue`."""

    def attach_aspect(self, _aspect): pass

    def detach_aspect(self, _aspect): pass


class TestAdaptValue:
    """Unit tests for :class:`~.AdaptValue`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        source = PatchAdaptValue()
        N_ASPECTS = 3
        for i in range(N_ASPECTS):
            source._aspects[i] = 'Aspect {}'.format(i)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert isinstance(target._aspects, dict)
        assert not target._aspects

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal."""
        # Setup
        # Test
        target = PatchAdaptValue()
        assert isinstance(target._aspects, dict)
        assert not target._aspects

    def test_init_extra(self):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        ERROR = re.escape("AdaptValue.__init__() called with extra "
                          "argument(s): {'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = PatchAdaptValue(extra='Oops!')

    def test_detach_all(self):
        """Confirm calls to remove each attached aspect."""
        # Setup

        class PatchDetach(AVALUE.AdaptValue[typing.Any]):

            def attach_aspect(self, _aspect): pass

            def detach_aspect(self, p_aspect):
                for i, aspect in self._aspects.items():
                    if aspect == p_aspect:
                        del self._aspects[i]
                        return
                raise NotImplementedError

        target = PatchDetach()
        N_ASPECTS = 3
        for i in range(N_ASPECTS):
            aspect = 'Aspect {}'.format(i)
            target._aspects[id(aspect)] = aspect
        # Test
        target.detach_all()
        assert isinstance(target._aspects, dict)
        assert not target._aspects


class TestAdaptValueText:
    """Unit tests for :class:`.AdaptValueText`.

    See :class:`.TestAdaptValueCommon` for additional unit tests for
    :class:`.AdaptValueText.
    """

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal."""
        # Setup
        VALUE = 42
        # Test
        target = AVALUE.AdaptValueText(p_value=VALUE)
        assert isinstance(target._aspects, dict)
        assert not target._aspects
        assert str(VALUE) == target._value_gtk

    def test_attach_aspect(self):
        """| Confirm addition of aspect.
        | Case: aspect not attached initially
        """
        # Setup
        VALUE = 42
        text = '<b>{}</b>'.format(VALUE)
        target = AVALUE.AdaptValueText(p_value=text)
        N_aspectS = 3
        aspects = [AspectValueText() for _ in range(N_aspectS)]
        # Test
        for aspect in aspects:
            target.attach_aspect(aspect)
        assert len(aspects) == len(target._aspects)
        for aspect in aspects:
            assert text == aspect.get_text()
            assert text == aspect.get_label()
            assert target._aspects[id(aspect)] is aspect

    def test_attach_aspect_warn(self, monkeypatch, PatchLogger):
        """| Confirm addition of aspect.
        | Case: aspect attached initially
        """
        # Setup
        class PatchSetText:
            def __init__(self): self.called = False

            def set_text(self, _buffer): self.called = True

        VALUE = 42
        target = AVALUE.AdaptValueText(p_value=VALUE)
        N_aspectS = 3
        aspects = [AspectValueText() for _ in range(N_aspectS)]
        for aspect in aspects:
            target.attach_aspect(aspect)
        I_DUP = 1
        aspect_dup = aspects[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate aspect: {} ({}.attach_aspect)'
            ''.format(hex(id(aspect_dup)), type(target).__name__))

        patch_set = PatchSetText()
        monkeypatch.setattr(
            AVALUE.AspectValueText, 'set_text', patch_set.set_text)
        # Test
        target.attach_aspect(aspect_dup)
        assert len(aspects) == len(target._aspects)
        assert not patch_set.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_aspect(self):
        """| Confirm removal of aspect.
        | Case: aspect attached initially
        """
        # Setup
        VALUE = 42
        text = '<b>{}</b>'.format(VALUE)
        target = AVALUE.AdaptValueText(p_value=text)
        N_ASPECTS = 3
        aspects = [AspectValueText() for _ in range(N_ASPECTS)]
        for aspect in aspects:
            target.attach_aspect(aspect)
        N_REMOVE = 1
        aspect_remove = aspects.pop(N_REMOVE)
        aspect_remove.set_visible(True)
        # Test
        target.detach_aspect(aspect_remove)
        assert len(aspects) == len(target._aspects)
        assert not aspect_remove.get_visible()
        for aspect in aspects:
            assert text == aspect.get_text()
            assert text == aspect.get_label()
            assert target._aspects[id(aspect)] is aspect

    def test_detach_aspect_warn(self, monkeypatch, PatchLogger):
        """| Confirm removal of aspect.
        | Case: aspect not attached initially
        """
        # Setup
        VALUE = 42
        text = '<b>{}</b>'.format(VALUE)
        target = AVALUE.AdaptValueText(p_value=text)
        N_aspectS = 3
        aspects = [AspectValueText() for _ in range(N_aspectS)]
        for aspect in aspects:
            target.attach_aspect(aspect)
        N_REMOVE = 1
        aspect_remove = aspects.pop(N_REMOVE)
        target.detach_aspect(aspect_remove)
        assert len(aspects) == len(target._aspects)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing aspect: {} ({}.detach_aspect)'
            ''.format(hex(id(aspect_remove)), type(target).__name__))
        # Test
        target.detach_aspect(aspect_remove)
        assert len(aspects) == len(target._aspects)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.adapt_value`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (AVALUE.ValueAny, typing.Any),
        (type(AVALUE.ValueOpaque), typing.TypeVar),
        (AVALUE.ValueTextGtk, str),
        (type(AspectValueOpaque), typing.TypeVar),
        (AspectValueText, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET is TYPE_SOURCE
