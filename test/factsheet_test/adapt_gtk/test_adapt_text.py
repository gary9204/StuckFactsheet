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


class TestAdaptText:
    """Unit tests for :class:`.AdaptText`.

    See :mod:`.abc_common` for additional tests to confirm method and
    property definitions of :class:`.AdaptText`.
    """

    def test_eq(self, patch_adapt_text):
        """Confirm equality comparison.

        #. Case: not a text attribute.
        #. Case: different content.
        #. Case: equal
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        source = patch_adapt_text()
        source.text = TEXT
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = patch_adapt_text()
        target.text = TEXT_DIFFER
        assert not source.__eq__(target)
        # Test: equal
        target = patch_adapt_text()
        target.text = TEXT
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_adapt_text):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = patch_adapt_text()
        TEXT = 'Something completely different'
        source.text = TEXT
        source._stale = True
        I_ENTRY = 0
        source._views[I_ENTRY] = TextStaticGtk()
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source.text == target.text
        assert not hasattr(target, 'ex_text')
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init(self, patch_adapt_text):
        """Confirm initialization."""
        # Setup
        # Test
        target = patch_adapt_text()
        assert target._stale is not None
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._text_gtk, str)
        assert not target._text_gtk

    def test_str(self, patch_adapt_text):
        """Confirm return is attribute content. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = patch_adapt_text()
        target._text_gtk = TEXT
        # Test
        assert TEXT == str(target)

    def test_attach_view(self, patch_adapt_text):
        """| Confirm addition of view.
        | Case: view not attached initially
        """
        # Setup
        target = patch_adapt_text()
        N_VIEWS = 3
        views = [ATEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert views == target.bound

    def test_attach_view_warn(
            self, patch_adapt_text, monkeypatch, PatchLogger):
        """| Confirm addition of view.
        | Case: view attached initially
        """
        # Setup
        target = patch_adapt_text()
        N_VIEWS = 3
        views = [ATEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.bound.clear()
        I_DUP = 1
        view_dup = views[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} ({}.attach_view)'
            ''.format(hex(id(view_dup)), type(target).__name__))
        # Test
        target.attach_view(view_dup)
        assert len(views) == len(target._views)
        assert not target.bound
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_view(self, patch_adapt_text):
        """| Confirm removal of view.
        | Case: view attached initially
        """
        # Setup
        target = patch_adapt_text()

        N_VIEWS = 3
        views = [ATEXT.ViewTextMarkup() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view
        assert [view_remove] == target.loosed

    def test_detach_view_warn(
            self, patch_adapt_text, monkeypatch, PatchLogger):
        """| Confirm removal of view.
        | Case: view not attached initially
        """
        # Setup
        target = patch_adapt_text()

        N_VIEWS = 3
        views = [ATEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        target.detach_view(view_remove)
        target.loosed.clear()
        assert len(views) == len(target._views)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} ({}.detach_view)'
            ''.format(hex(id(view_remove)), type(target).__name__))
        # Test
        target.detach_view(view_remove)
        assert not target.loosed
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_is_fresh(self, patch_adapt_text):
        """Confirm return matches state. """
        # Setup
        target = patch_adapt_text()
        target._stale = False
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self, patch_adapt_text):
        """Confirm return matches state. """
        # Setup
        target = patch_adapt_text()
        target._stale = False
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self, patch_adapt_text):
        """Confirm attribute marked fresh. """
        # Setup
        target = patch_adapt_text()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self, patch_adapt_text):
        """Confirm attribute marked stale. """
        # Setup
        target = patch_adapt_text()
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
        source = CLASS_ADAPT()
        source._stale = True
        TEXT = 'The Parrot Sketch'
        source.text = TEXT
        I_ENTRY = 0
        source._views[I_ENTRY] = CLASS_TEXT()
        # Warning: GO.signal_lookup fails unless there is a prior
        #    reference to CLASS_TEXT.  Reference loads GObject class.
        origin_gtype = GO.type_from_name(GO.type_name(CLASS_TEXT))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        NO_SIGNAL = 0
        PATH = Path(str(tmp_path / 'get_set.fsg'))
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


class TestAdaptTextFormat:
    """Unit tests for :class:`.AdaptTextFormat`.

    :class:`.TestAdaptTextCommon` contains all unit tests for
    :class:`.AdaptTestFormat.
    """

    def test_bind_store(self):
        """Confirm widget association."""
        # Setup
        target = ATEXT.AdaptTextFormat()
        VIEW = ATEXT.ViewTextFormat()
        # Test
        target._bind_store(VIEW)
        assert target._text_gtk is VIEW.get_buffer()

    def test_loose_store(self):
        """Confirm widget disassociation."""
        # Setup
        target = ATEXT.AdaptTextFormat()
        VIEW = ATEXT.ViewTextFormat()
        target._bind_store(VIEW)
        assert target._text_gtk is VIEW.get_buffer()
        # Test
        target._loose_store(VIEW)
        assert target._text_gtk is not VIEW.get_buffer()

    def test_new_store_gtk(self):
        """Confirm storage type."""
        # Setup
        target = ATEXT.AdaptTextFormat()
        # Test
        assert isinstance(target._text_gtk, ATEXT.TextFormatGtk)


class TestAdaptTextMarkup:
    """Unit tests for :class:`.AdaptTextMarkup`.

    :class:`.TestAdaptTextCommon` contains additional unit tests for
    :class:`.AdaptTestMarkup.
    """

    def test_bind_store(self):
        """Confirm widget association."""
        # Setup
        target = ATEXT.AdaptTextMarkup()
        VIEW = ATEXT.ViewTextMarkup()
        # Test
        target._bind_store(VIEW)
        assert target._text_gtk is VIEW.get_buffer()

    def test_loose_store(self):
        """Confirm widget disassociation."""
        # Setup
        target = ATEXT.AdaptTextMarkup()
        VIEW = ATEXT.ViewTextMarkup()
        target._bind_store(VIEW)
        assert target._text_gtk is VIEW.get_buffer()
        # Test
        target._loose_store(VIEW)
        assert target._text_gtk is not VIEW.get_buffer()

    def test_new_store_gtk(self):
        """Confirm storage type."""
        # Setup
        target = ATEXT.AdaptTextMarkup()
        # Test
        assert isinstance(target._text_gtk, ATEXT.TextMarkupGtk)


class TestAdaptTextStatic:
    """Unit tests for :class:`.AdaptTextStatis`.

    See :class:`.TestAdaptTextCommon` for additional unit tests for
    :class:`.AdaptTestStatic.
    """

    def test_bind_store(self):
        """Confirm widget association."""
        # Setup
        target = ATEXT.AdaptTextStatic()
        TEXT = 'Something <i>completely </i>different!'
        target.text = TEXT
        VIEW = ATEXT.ViewTextStatic()
        # Test
        target._bind_store(VIEW)
        assert TEXT == VIEW.get_label()

    def test_loose_store(self):
        """Confirm widget disassociation."""
        # Setup
        target = ATEXT.AdaptTextStatic()
        VIEW = ATEXT.ViewTextStatic()
        TEXT = 'Something <i>completely </i>different!'
        VIEW.set_label(TEXT)
        BLANK = ''
        # Test
        target._loose_store(VIEW)
        target._bind_store(VIEW)
        assert BLANK == VIEW.get_label()

    def test_new_store_gtk(self):
        """Confirm storage type."""
        # Setup
        target = ATEXT.AdaptTextStatic()
        # Test
        assert isinstance(target._text_gtk, ATEXT.TextStaticGtk)

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
        # Test
        target.detach_view(view_remove)
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
        N_VIEWS = 3
        views = [ATEXT.ViewTextStatic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        target.set_fresh()
        # Test: get with fresh
        assert TEXT == target.text
        for view in views:
            assert TEXT == view.get_label()
        assert target.is_fresh()
        # Test: get with stale
        target.set_stale()
        assert TEXT == target.text
        for view in views:
            assert TEXT == view.get_label()
        assert target.is_stale()
        # Test: set with fresh
        target.set_fresh()
        TEXT_NEW = 'Something <i>completely </i>different!'
        target.text = TEXT_NEW
        assert TEXT_NEW == target.text
        for view in views:
            assert TEXT_NEW == view.get_label()
        assert target.is_stale()
        # Test: no delete
        prop = getattr(ATEXT.AdaptTextFormat, 'text')
        assert prop.fdel is None


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.adapt_text`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(ATEXT.TextOpaqueGtk), typing.TypeVar),
        (ATEXT.TextFormatGtk, Gtk.TextBuffer),
        (ATEXT.TextMarkupGtk, Gtk.EntryBuffer),
        (ATEXT.TextStaticGtk, str),
        (ATEXT.ViewTextFormat, Gtk.TextView),
        (ATEXT.ViewTextMarkup, Gtk.Entry),
        (type(ATEXT.ViewTextOpaque), typing.TypeVar),
        (ATEXT.ViewTextOpaque.__constraints__, ()),
        (ATEXT.ViewTextStatic, Gtk.Label),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
