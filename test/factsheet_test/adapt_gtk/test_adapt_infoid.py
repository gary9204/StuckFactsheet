"""
Unit tests for GTK-based classes that implement abstract identification
information classes.

See :mod:`.adapt_infoid`.
"""
import gi   # type: ignore[import]
import logging
import pickle
import pytest   # type: ignore[import]

from pathlib import Path

from factsheet.adapt_gtk import adapt_infoid as AINFOID

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def PatchConnect():
    """PyTest fixture."""
    class Connect:
        ID_STUB = 42

        def __init__(self): self.called_names = list()

        def connect(self, name, _function):
            self.called_names.append(name)
            return self.ID_STUB

    return Connect


class TestAdaptEntry:
    """Unit tests for :data:`.AdaptEntry` implementation of
    :class:`.AbstractTextModel`.
    """

    def test_adapt_entry(self):
        """Confirm definition of :data:`.AdaptEntry`."""
        # Setup
        # Test
        assert AINFOID.AdaptEntry is Gtk.Entry


class TestAdaptEntryBuffer:
    """Unit tests for :class:`.AdaptEntryBuffer` implementation of
    :class:`.AbstractTextModel`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        view = AINFOID.AdaptEntry()
        text = 'Something completely different'
        source = AINFOID.AdaptEntryBuffer(p_text=text)
        source.attach_view(view)
        source._stale = True
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert str(source) == str(target)
        assert not hasattr(target, 'ex_text')
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    @pytest.mark.parametrize('name_signal, n_default', [
        ('deleted-text', 0),
        ('inserted-text', 0),
        ])
    def test_get_set_signals(self, tmp_path, name_signal, n_default):
        """Confirm reconstruction of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.EntryBuffer))
        signal = GO.signal_lookup(name_signal, origin_gtype)

        path = Path(str(tmp_path / 'get_set.fsg'))
        text = 'Something completely different'
        source = AINFOID.AdaptEntryBuffer(p_text=text)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._buffer, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(target._buffer, id_signal)

        assert (n_default + 1) == n_handlers

    def test_init(self):
        """Confirm initialization with arguments. """
        # Setup
        text = 'Something completely different'
        # Test
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        assert isinstance(target._buffer, Gtk.EntryBuffer)
        assert text == str(target._buffer.get_text())

        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init_default(self):
        """Confirm initialization with default arguments. """
        # Setup
        text = ''
        # Test
        target = AINFOID.AdaptEntryBuffer()
        assert isinstance(target._buffer, Gtk.EntryBuffer)
        assert text == str(target._buffer.get_text())

    @pytest.mark.parametrize('name_signal, n_default', [
        ('deleted-text', 0),
        ('inserted-text', 0),
        ])
    def test_init_signals(self, name_signal, n_default):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.EntryBuffer))
        signal = GO.signal_lookup(name_signal, origin_gtype)
        # Test
        target = AINFOID.AdaptEntryBuffer()
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._buffer, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(target._buffer, id_signal)

        assert (n_default + 1) == n_handlers

    def test_str(self):
        """Confirm return is buffer text. """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        # Test
        assert text == str(target)

    def test_attach_view(self):
        """Confirm addition of view.
        Case: view not attached initially
        """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)

        N_VIEWS = 3
        views = [AINFOID.AdaptEntry() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
            assert target._buffer is view.get_buffer()
            assert target._views[id(view)] is view
        assert len(views) == len(target._views)

    def test_attach_view_warn(self, monkeypatch, PatchLogger):
        """Confirm addition of view.
        Case: view attached initially
        """
        # Setup
        class PatchSetBuffer:
            def __init__(self): self.called = False

            def set_buffer(self, _buffer): self.called = True
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)

        N_VIEWS = 3
        views = [AINFOID.AdaptEntry() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUPLICATE = 1
        view_duplicate = views[I_DUPLICATE]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} (AdaptEntryBuffer.attach_view)'
            ''.format(hex(id(view_duplicate))))

        patch_set_buffer = PatchSetBuffer()
        monkeypatch.setattr(
            AINFOID.AdaptEntry, 'set_buffer', patch_set_buffer.set_buffer)
        # Test
        target.attach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert not patch_set_buffer.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_view(self):
        """Confirm removal of view.
        Case: view attached initially
        """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)

        N_VIEWS = 3
        views = [AINFOID.AdaptEntry() for _ in range(N_VIEWS)]
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
            assert target._buffer is view.get_buffer()
            assert target._views[id(view)] is view

    def test_detach_view_warn(self, monkeypatch, PatchLogger):
        """Confirm removal of view.
        Case: view not attached initially
        """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)

        N_VIEWS = 3
        views = [AINFOID.AdaptEntry() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_DUPLICATE = 1
        view_duplicate = views.pop(N_DUPLICATE)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} (AdaptEntryBuffer.detach_view)'
            ''.format(hex(id(view_duplicate))))

        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        # Test
        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_is_fresh(self):
        """Confirm return matches state. """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self):
        """Confirm return matches state. """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self):
        """Confirm buffer marked fresh. """
        # Setup
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self):
        """Confirm buffer marked stale. """
        text = 'Something completely different'
        target = AINFOID.AdaptEntryBuffer(p_text=text)
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale


class TestAdaptTextBuffer:
    """Unit tests for :class:`.AdaptTextBuffer` implementation of
    :class:`.AbstractTextModel`."""

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        view = AINFOID.AdaptTextView()
        TEXT = 'Something completely different'
        source = AINFOID.AdaptTextBuffer(p_text=TEXT)
        source.attach_view(view)
        source._stale = True
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert str(source) == str(target)
        assert not hasattr(target, 'ex_text')
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    @pytest.mark.parametrize('name_signal, n_default', [
        ('changed', 0),
        ])
    def test_get_set_signals(self, tmp_path, name_signal, n_default):
        """Confirm reconstruction of signal connections."""
        # Setup
        _PATCH = Gtk.TextBuffer()   # See Factsheet Issue #51 on GitHub.
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.TextBuffer))
        signal = GO.signal_lookup(name_signal, origin_gtype)

        path = Path(str(tmp_path / 'get_set.fsg'))
        TEXT = 'Something completely different'
        source = AINFOID.AdaptTextBuffer(p_text=TEXT)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._buffer, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(target._buffer, id_signal)

        assert (n_default + 1) == n_handlers

    def test_init(self):
        """Confirm initialization with arguments. """
        # Setup
        TEXT = 'Something completely different'
        # Test
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        assert isinstance(target._buffer, Gtk.TextBuffer)
        buffer = target._buffer
        start, end = buffer.get_bounds()
        text_target = str(
            target._buffer.get_text(start, end, target.INCLUDE_HIDDEN))
        assert TEXT == text_target
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views

    def test_init_default(self):
        """Confirm initialization with default arguments. """
        # Setup
        TEXT = ''
        # Test
        target = AINFOID.AdaptTextBuffer()
        assert isinstance(target._buffer, Gtk.TextBuffer)
        buffer = target._buffer
        start, end = buffer.get_bounds()
        text_target = str(
            target._buffer.get_text(start, end, target.INCLUDE_HIDDEN))
        assert TEXT == text_target

    @pytest.mark.parametrize('name_signal, n_default', [
        ('changed', 0),
        ])
    def test_init_signals(self, name_signal, n_default):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(Gtk.TextBuffer))
        signal = GO.signal_lookup(name_signal, origin_gtype)
        # Test
        target = AINFOID.AdaptTextBuffer()
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                target._buffer, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(target._buffer, id_signal)

        assert (n_default + 1) == n_handlers

    def test_str(self):
        """Confirm return is buffer text. """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        # Test
        assert TEXT == str(target)

    def test_attach_view(self):
        """Confirm addition of view.
        Case: view not attached initially
        """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)

        N_VIEWS = 3
        views = [AINFOID.AdaptTextView() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
            assert target._buffer is view.get_buffer()
            assert target._views[id(view)] is view
        assert len(views) == len(target._views)

    def test_attach_view_warn(self, monkeypatch, PatchLogger):
        """Confirm addition of view.
        Case: view attached initially
        """
        # Setup
        class PatchSetBuffer:
            def __init__(self): self.called = False

            def set_buffer(self, _buffer): self.called = True
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)

        N_VIEWS = 3
        views = [AINFOID.AdaptTextView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUPLICATE = 1
        view_duplicate = views[I_DUPLICATE]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} (AdaptTextBuffer.attach_view)'
            ''.format(hex(id(view_duplicate))))

        patch_set_buffer = PatchSetBuffer()
        monkeypatch.setattr(AINFOID.AdaptTextView,
                            'set_buffer', patch_set_buffer.set_buffer)
        # Test
        target.attach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert not patch_set_buffer.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_view(self):
        """Confirm removal of view.
        Case: view attached initially
        """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)

        N_VIEWS = 3
        views = [AINFOID.AdaptTextView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        view_remove.show()
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        assert view_remove.get_buffer() is not target._buffer
        for view in views:
            assert target._buffer is view.get_buffer()
            assert target._views[id(view)] is view

    def test_detach_view_warn(self, monkeypatch, PatchLogger):
        """Confirm removal of view.
        Case: view not attached initially
        """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)

        N_VIEWS = 3
        views = [AINFOID.AdaptTextView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_DUPLICATE = 1
        view_duplicate = views.pop(N_DUPLICATE)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} (AdaptTextBuffer.detach_view)'
            ''.format(hex(id(view_duplicate))))

        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        # Test
        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_is_fresh(self):
        """Confirm return matches state. """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        # Test
        assert target.is_fresh()
        target._stale = True
        assert not target.is_fresh()

    def test_is_stale(self):
        """Confirm return matches state. """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        # Test
        assert not target.is_stale()
        target._stale = True
        assert target.is_stale()

    def test_set_freah(self):
        """Confirm buffer marked fresh. """
        # Setup
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    def test_set_stale(self):
        """Confirm buffer marked stale. """
        TEXT = 'Something completely different'
        target = AINFOID.AdaptTextBuffer(p_text=TEXT)
        target._stale = False
        # Test
        target.set_stale()
        assert target._stale


class TestAdaptTextView:
    """Unit tests for :data:`.AdaptTextView` implementation of
    :class:`.AbstractTextModel`.
    """

    def test_adapt_textview(self):
        """Confirm definition of :data:`.AdaptTextView`."""
        # Setup
        # Test
        assert AINFOID.AdaptTextView is Gtk.TextView

    def test_str_adapt_textview(self):
        """Confirm conversion of :data:`.AdaptTextView` to text."""
        # Setup
        TEXT = 'Something completely different.'
        model = AINFOID.AdaptTextBuffer(TEXT)
        buffer = model._buffer
        target = AINFOID.AdaptTextView()
        target.set_buffer(buffer)
        # Test
        assert TEXT == AINFOID.str_adapt_textview(target)
