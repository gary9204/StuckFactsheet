"""
Unit tests adapters and type hints for fact values and aspects.  See
:mod:`~.bridge_aspect`.
"""
# import logging
from pathlib import Path
import pickle
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
# import re
import typing

import factsheet.bridge_gtk.bridge_aspect as BASPECT

from factsheet.bridge_gtk.bridge_aspect import ViewAspectOpaque

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestAspect:
    """Unit tests for :class:`~.Aspect`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BASPECT.BridgeAspect, '_bind'),
        (BASPECT.BridgeAspect, '_get_persist'),
        (BASPECT.BridgeAspect, '_loose'),
        (BASPECT.BridgeAspect, '_new_model'),
        (BASPECT.BridgeAspect, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestAspectPlain:
    """Unit tests for :class:`.AspectPlain`.

    See :class:`.TestAspectCommon` for additional unit tests for
    :class:`.AspectPlain.
    """

    @pytest.mark.skip
    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle aspect."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        source = PatchAspect()
        N_ASPECTS = 3
        for i in range(N_ASPECTS):
            source._aspects[i] = 'Aspect {}'.aspect(i)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert isinstance(target._aspects, dict)
        assert not target._aspects

    # @pytest.mark.skip
    # def test_init(self):
    #     """| Confirm initialization.
    #     | Case: nominal.
    #     """
    #     # Setup
    #     # Test
    #     target = PatchAspect()
    #     assert target.called_clear
    #     assert isinstance(target._aspects, dict)
    #     assert not target._aspects

    @pytest.mark.skip
    def test_init(self):
        """Confirm initialization."""
        # Setup
        BLANK = ''
        # Test
        target = BASPECT.AspectPlain()
        assert isinstance(target._aspects, dict)
        assert not target._aspects
        assert BLANK == target._value_gtk

    @pytest.mark.skip
    def test_set(self):
        """Confirm aspect and aspects are set."""
        # Setup
        # target = BASPECT.AspectPlain()  # p_value=None)
        # N_ASPECTS = 3
        # aspects = [ViewAspectPlain() for _ in range(N_ASPECTS)]
        # for aspect in aspects:
        #     target.attach_aspect(aspect)
        # assert len(aspects) == len(target._aspects)
        # VALUE = 42
        # text = '<b>{}</b>'.aspect(VALUE)
        # # Test
        # target.set(text)
        # assert text == target._value_gtk
        # for aspect in aspects:
        #     assert text == aspect.get_text()
        #     assert text == aspect.get_label()
        #     assert target._aspects[id(aspect)] is aspect


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.bridge_aspect`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        # (BASPECT.ModelAspectPlain, typing.Any),
        # (type(BASPECT.ModelAspectOpaque), typing.TypeVar),
        # (BASPECT.ModelAspectOpaque.__constraints__, ()),
        # (type(ViewAspectOpaque), typing.TypeVar),
        # (BASPECT.ViewAspectOpaque.__constraints__, ()),
        # (BASPECT.ViewAspectPlain, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
