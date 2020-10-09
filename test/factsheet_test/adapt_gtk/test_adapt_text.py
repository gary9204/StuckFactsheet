"""
Unit tests for GTK-based classes that implement abstract identification
information classes.  See :mod:`.adapt_text`.
"""
import gi   # type: ignore[import]
import logging
import pickle
import pytest   # type: ignore[import]
import typing

from pathlib import Path

import factsheet.adapt_gtk.adapt_text as ATEXT

from factsheet.adapt_gtk.adapt_text import TextStaticGtk
from factsheet.adapt_gtk.adapt_text import ViewTextStatic

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchAdaptText(ATEXT.AdaptText[typing.Any]):
    """Class with stub for methods abstract in :class:`.AdaptText`."""

    def __init__(self):
        super().__init__()
        self._text = 'Oops! no text assigned.'

    def attach_view(self, _view): pass

    def detach_view(self, _view): pass

    @property
    def text(self): return self._text

    @text.setter
    def text(self, p_text): self._text = p_text


class TestAdaptText:
    """Unit tests for :class:`.AdaptText`.

    See :mod:`.abc_common` for additional tests to confirm method and
    property definitions of :class:`.AdaptText`.
    """

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: not a text attribute.
        #. Case: different content.
        #. Case: equal
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        source = PatchAdaptText()
        source.text = TEXT
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchAdaptText()
        target.text = TEXT_DIFFER
        assert not source.__eq__(target)
        # Test: equal
        target = PatchAdaptText()
        target.text = TEXT
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = PatchAdaptText()
        source._stale = True
        I_ENTRY = 0
        source._views[I_ENTRY] = TextStaticGtk()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = PatchAdaptText()
        assert target._stale is not None
        assert isinstance(target._views, dict)
        assert not target._views

    def test_str(self):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = PatchAdaptText()
        target._text = TEXT
        # Test
        assert TEXT == str(target)

    def test_is_fresh(self):
        """Confirm return matches state. """
        # Setup
        target = PatchAdaptText()
        target._stale = False
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self):
        """Confirm return matches state. """
        # Setup
        target = PatchAdaptText()
        target._stale = False
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self):
        """Confirm attribute marked fresh. """
        # Setup
        target = PatchAdaptText()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self):
        """Confirm attribute marked stale. """
        # Setup
        target = PatchAdaptText()
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale


class TestAdaptTextCommon:
    """Unit tests common common to descendants of :class:`.AdaptText`.

    Parameters specialize the tests for each class.  Some descendants
    may need individualized tests (for example,
    :class:`.AdaptTextStatic`).
    """

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_VIEW', [
            (ATEXT.AdaptTextFormat, ATEXT.ViewTextFormat),
            (ATEXT.AdaptTextMarkup, ATEXT.ViewTextMarkup),
        ])
    def test_get_set_state(self, tmp_path, CLASS_ADAPT, CLASS_VIEW):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'The Parrot Sketch'
        source = CLASS_ADAPT()
        source._stale = True
        source.text = TEXT
        I_ENTRY = 0
        source._views[I_ENTRY] = CLASS_VIEW()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source.text == target.text
        assert not hasattr(target, 'ex_text')
        assert not target._stale
        assert not target._views

    @pytest.mark.parametrize(
        'CLASS_ADAPT, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            (ATEXT.AdaptTextFormat, ATEXT.TextFormatGtk, 'changed', 0),
            (ATEXT.AdaptTextMarkup, ATEXT.TextMarkupGtk, 'inserted-text', 0),
            (ATEXT.AdaptTextMarkup, ATEXT.TextMarkupGtk, 'inserted-text', 0),
        ])
    def test_get_set_signals(self, tmp_path, CLASS_ADAPT, CLASS_TEXT,
                             NAME_SIGNAL, N_DEFAULT):
        """Confirm reconstruction of signal connections."""
        # Setup
        # Warning: GO.signal_lookup fails unless there is a prior
        #    reference to CLASS_TEXT.  Reference loads GObject class.
        origin_gtype = GO.type_from_name(GO.type_name(CLASS_TEXT))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'The Parrot Sketch'
        source = CLASS_ADAPT()
        source._stale = True
        source.text = TEXT
        I_ENTRY = 0
        source._views[I_ENTRY] = CLASS_TEXT()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._text_gtk, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if NO_SIGNAL == id_signal:
                break
            n_handlers += 1
            GO.signal_handler_disconnect(target._text_gtk, id_signal)
        assert (N_DEFAULT + 1) == n_handlers

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_TEXT', [
            (ATEXT.AdaptTextFormat, ATEXT.TextFormatGtk),
            (ATEXT.AdaptTextMarkup, ATEXT.TextMarkupGtk),
            (ATEXT.AdaptTextStatic, ATEXT.TextStaticGtk),
        ])
    def test_init(self, CLASS_ADAPT, CLASS_TEXT):
        """Confirm initialization. """
        # Setup
        # Test
        target = CLASS_ADAPT()
        assert not target._stale
        assert not target._views
        assert isinstance(target._text_gtk, CLASS_TEXT)
        assert not target.text

    @pytest.mark.parametrize(
        'CLASS_ADAPT, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT', [
            (ATEXT.AdaptTextFormat, ATEXT.TextFormatGtk, 'changed', 0),
            (ATEXT.AdaptTextMarkup, ATEXT.TextMarkupGtk, 'deleted-text', 0),
            (ATEXT.AdaptTextMarkup, ATEXT.TextMarkupGtk, 'inserted-text', 0),
        ])
    def test_init_signals(
            self, CLASS_ADAPT, CLASS_TEXT, NAME_SIGNAL, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(CLASS_TEXT))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        # Test
        target = CLASS_ADAPT()
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._text_gtk, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if NO_SIGNAL == id_signal:
                break
            n_handlers += 1
            GO.signal_handler_disconnect(target._text_gtk, id_signal)
        assert (N_DEFAULT + 1) == n_handlers

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_VIEW', [
        (ATEXT.AdaptTextFormat, ATEXT.ViewTextFormat),
        (ATEXT.AdaptTextMarkup, ATEXT.ViewTextMarkup),
        ])
    def test_attach_view(self, CLASS_ADAPT, CLASS_VIEW):
        """| Confirm addition of view.
        | Case: view not attached initially
        """
        # Setup
        target = CLASS_ADAPT()
        N_VIEWS = 3
        views = [CLASS_VIEW() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
        assert len(views) == len(target._views)
        for view in views:
            assert target._text_gtk is view.get_buffer()
            assert target._views[id(view)] is view

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_VIEW', [
        (ATEXT.AdaptTextFormat, ATEXT.ViewTextFormat),
        (ATEXT.AdaptTextMarkup, ATEXT.ViewTextMarkup),
        ])
    def test_attach_view_warn(
            self, CLASS_ADAPT, CLASS_VIEW, monkeypatch, PatchLogger):
        """| Confirm addition of view.
        | Case: view attached initially
        """
        # Setup
        class PatchSetBuffer:
            def __init__(self): self.called = False

            def set_buffer(self, _buffer): self.called = True

        target = CLASS_ADAPT()
        N_VIEWS = 3
        views = [CLASS_VIEW() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUP = 1
        view_dup = views[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} ({}.attach_view)'
            ''.format(hex(id(view_dup)), type(target).__name__))

        patch_set = PatchSetBuffer()
        monkeypatch.setattr(
            ATEXT.ViewTextMarkup, 'set_buffer', patch_set.set_buffer)
        # Test
        target.attach_view(view_dup)
        assert len(views) == len(target._views)
        assert not patch_set.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_VIEW', [
        (ATEXT.AdaptTextFormat, ATEXT.ViewTextFormat),
        (ATEXT.AdaptTextMarkup, ATEXT.ViewTextMarkup),
        ])
    def test_detach_view(self, CLASS_ADAPT, CLASS_VIEW):
        """| Confirm removal of view.
        | Case: view attached initially
        """
        # Setup
        target = CLASS_ADAPT()

        N_VIEWS = 3
        views = [CLASS_VIEW() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        view_remove.set_visible(True)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        assert not view_remove.get_visible()
        for view in views:
            assert target._text_gtk is view.get_buffer()
            assert target._views[id(view)] is view

    @pytest.mark.parametrize('CLASS_ADAPT, CLASS_VIEW', [
        (ATEXT.AdaptTextFormat, ATEXT.ViewTextFormat),
        (ATEXT.AdaptTextMarkup, ATEXT.ViewTextMarkup),
        ])
    def test_detach_view_warn(
            self, CLASS_ADAPT, CLASS_VIEW, monkeypatch, PatchLogger):
        """| Confirm removal of view.
        | Case: view not attached initially
        """
        # Setup
        target = CLASS_ADAPT()

        N_VIEWS = 3
        views = [CLASS_VIEW() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        target.detach_view(view_remove)
        assert len(views) == len(target._views)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} ({}.detach_view)'
            ''.format(hex(id(view_remove)), type(target).__name__))
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message


class TestAdaptTextMarkup:
    """Unit tests for :class:`.AdaptTextMarkup`.

    :class:`.TestAdaptTextCommon` contains all unit tests for
    :class:`.AdaptTestMarkup.
    """

    pass


class TestAdaptTextFormat:
    """Unit tests for :class:`.AdaptTextFormat`.

    :class:`.TestAdaptTextCommon` contains all unit tests for
    :class:`.AdaptTestFormat.
    """

    pass


class TestAdaptTextStatic:
    """Unit tests for :class:`.AdaptTextStatis`.

    See :class:`.TestAdaptTextCommon` for additional unit tests for
    :class:`.AdaptTestStatic.
    """
    def test_attach_view(self):
        """| Confirm addition of view.
        | Case: view not attached initially
        """
        # Setup
        TEXT = 'Something <i>completely </i>different.'
        target = ATEXT.AdaptTextStatic()
        target.text = TEXT
        N_VIEWS = 3
        views = [ViewTextStatic() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
        assert len(views) == len(target._views)
        for view in views:
            assert target._text_gtk == view.get_label()
            assert target._views[id(view)] is view

    def test_attach_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm addition of view.
        | Case: view attached initially
        """
        # Setup
        class PatchSetLabel:
            def __init__(self): self.called = False

            def set_label(self, _str): self.called = True

        target = ATEXT.AdaptTextStatic()
        N_VIEWS = 3
        views = [ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUP = 1
        view_dup = views[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} ({}.attach_view)'
            ''.format(hex(id(view_dup)), type(target).__name__))

        patch_set = PatchSetLabel()
        monkeypatch.setattr(
            ViewTextStatic, 'set_label', patch_set.set_label)
        # Test
        target.attach_view(view_dup)
        assert len(views) == len(target._views)
        assert not patch_set.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_view(self):
        """| Confirm removal of view.
        | Case: view attached initially
        """
        # Setup
        target = ATEXT.AdaptTextStatic()

        N_VIEWS = 3
        views = [ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        view_remove.set_visible(True)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        assert not view_remove.get_visible()
        for view in views:
            assert target._text_gtk == view.get_label()
            assert target._views[id(view)] is view

    def test_detach_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm removal of view.
        | Case: view not attached initially
        """
        # Setup
        target = ATEXT.AdaptTextStatic()

        N_VIEWS = 3
        views = [ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        target.detach_view(view_remove)
        assert len(views) == len(target._views)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} ({}.detach_view)'
            ''.format(hex(id(view_remove)), type(target).__name__))
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_text(self):
        """Confirm property access and freshness update.

        #. Case: get with fresh
        #. Case: get with stale
        #. Case: set with fresh
        #. Case: no delete
        """
        # Setup
        target = ATEXT.AdaptTextStatic()
        TEXT = 'The Parrot Sketch'
        target._text_gtk = TEXT
        target.set_fresh()
        # Test: get with fresh
        assert TEXT == target.text
        assert target.is_fresh()
        # Test: get with stale
        target.set_stale()
        assert TEXT == target.text
        assert target.is_stale()
        # Test: set with fresh
        target.set_fresh()
        TEXT_NEW = 'Something <i>completely </i>different!'
        target.text = TEXT_NEW
        assert TEXT_NEW == target.text
        assert target.is_stale()
        # Test: no delete
        prop = getattr(ATEXT.AdaptTextFormat, 'text')
        assert prop.fdel is None


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.adapt_text`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (ATEXT.TextFormatGtk, Gtk.TextBuffer),
        (ATEXT.TextMarkupGtk, Gtk.EntryBuffer),
        (ATEXT.TextStaticGtk, str),
        (ATEXT.ViewTextFormat, Gtk.TextView),
        (ATEXT.ViewTextMarkup, Gtk.Entry),
        (type(ATEXT.ViewTextOpaque), typing.TypeVar),
        (ATEXT.ViewTextStatic, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET is TYPE_SOURCE
