"""
Unit tests for :mod:`.markup_gtk3`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import pytest
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC
import factsheet.ui_bricks.ui_gtk3.markup_gtk3 as BMARKUPGTK3

from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


class StubObserver(BMARKUPGTK3.ObserverMarkupAbc):
    """Stub for :data:`.ObserverMarkupAbc`."""

    def __init__(self):
        self.store_ui = None

    def on_notice(self, p_store_ui, **kwargs):
        """Record GTK 3 store object to confirm call."""
        del kwargs
        self.store_ui = p_store_ui


class TestControlMarkupGtk3:
    """Unit tests for :class:`.ControlMarkupGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ControlMarkupGtk3(p_model=MODEL)
        assert target._model is MODEL
        assert isinstance(target._observers, typing.MutableMapping)
        assert not target._observers

    @pytest.mark.parametrize('ORIGIN, NAME_SIGNAL, N_DEFAULT', [
            (BMARKUPGTK3.StoreUiTextMarkup, 'deleted-text', 0),
            (BMARKUPGTK3.StoreUiTextMarkup, 'inserted-text', 0),
            ])
    def test_init_signals(self, ORIGIN, NAME_SIGNAL, N_DEFAULT):
        """Confirm GTK 3 signal connection.

        :param ORIGIN: GTK class origin of signal.
        :param NAME_SIGNAL: name of signal to check.
        :param N_DEFAULT: count of default signal handlers.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        target = BMARKUPGTK3.ControlMarkupGtk3()
        source = target._model.get_store_ui()
        # Test
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                source, GO.SignalMatchType.ID, signal, 0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(source, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    def test_attach(self):
        """| Confirm control will notify observer.
        | Case: initially control not notifying observer.
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        OBSERVER = StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))
        # Test
        target.attach(p_observer=OBSERVER)
        assert target._observers[ID_OBSERVER] is OBSERVER

    def test_attach_present(self, caplog):
        """| Confirm control will notify observer.
        | Case: initially control already notifying observer.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        OBSERVER = StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))
        target._observers[ID_OBSERVER] = OBSERVER

        N_LOGS = 1
        LAST = -1
        log_message = ('Observer already being notified. id: {} '
                       '(ControlMarkupGtk3.attach)'.format(
                           hex(ID_OBSERVER)))
        # Test
        target.attach(OBSERVER)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_bypass(self):
        """Confirm return of model text as GTK 3 object."""
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        MODEL = target._model._store_ui
        # Test
        assert target.bypass() is MODEL

    def test_detach(self):
        """| Confirm control will not notify observer.
        | Case: initially control already notifying observer.
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        OBSERVER = StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))
        target._observers[ID_OBSERVER] = OBSERVER
        # Test
        target.detach(p_observer=OBSERVER)
        assert ID_OBSERVER not in target._observers

    def test_detach_absent(self, caplog):
        """| Confirm control will not notify observer.
        | Case: initially control not notifying observer.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        OBSERVER = StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))

        N_LOGS = 1
        LAST = -1
        log_message = ('Observer not being notified. id: {} '
                       '(ControlMarkupGtk3.detach)'.format(
                           hex(ID_OBSERVER)))
        # Test
        target.detach(OBSERVER)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_new_model(self):
        """Confirm model construction."""
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        # Test
        assert isinstance(target._model, BMARKUPGTK3.ModelMarkupGtk3)

    def test_notify(self):
        """Confirm notification of observers."""
        # Setup
        N_OBSERVERS = 5
        OBSERVERS = [StubObserver() for _ in range(N_OBSERVERS)]
        target = BMARKUPGTK3.ControlMarkupGtk3()
        for observer in OBSERVERS:
            target.attach(p_observer=observer)
        STORE = target._model.get_store_ui()
        # Test
        target.notify()
        for observer in OBSERVERS:
            assert observer.store_ui is STORE

    def test_model_change(self):
        """Confirm transient aspect updates."""
        # Setup
        N_OBSERVERS = 5
        OBSERVERS = [StubObserver() for _ in range(N_OBSERVERS)]
        target = BMARKUPGTK3.ControlMarkupGtk3()
        for observer in OBSERVERS:
            target.attach(p_observer=observer)
        STORE = target._model.get_store_ui()
        # Test
        target.on_model_change()
        for observer in OBSERVERS:
            assert observer.store_ui is STORE


class TestControlMarkupTrackGtk3:
    """Unit tests for :class:`.ControlMarkupTrackGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ControlMarkupTrackGtk3(p_model=MODEL)
        assert target._model is MODEL
        assert hasattr(target, '_observers')
        assert isinstance(target._changed, bool)
        assert not target._changed

    @pytest.mark.parametrize('CHANGED', [
        False,
        True
        ])
    def test_has_changed(self, CHANGED):
        """Confirm return matches change state.

        :param CHANGED: change state
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupTrackGtk3()
        # Test
        target._changed = CHANGED
        assert target.has_changed() is CHANGED

    @pytest.mark.parametrize('CHANGED', [
        False,
        True
        ])
    def test_has_not_changed(self, CHANGED):
        """Confirm return negates change state.

        :param CHANGED: change state
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupTrackGtk3()
        EXPECT = not CHANGED
        # Test
        target._changed = CHANGED
        assert target.has_not_changed() is EXPECT

    def test_mark_changed(self):
        """Confirm text marked as changed"""
        # Setup
        target = BMARKUPGTK3.ControlMarkupTrackGtk3()
        # Test
        target._changed = False
        target.mark_changed()
        assert target._changed

    def test_mark_not_changed(self):
        """Confirm text marked as not changed"""
        # Setup
        target = BMARKUPGTK3.ControlMarkupTrackGtk3()
        # Test
        target._changed = True
        target.mark_not_changed()
        assert not target._changed

    def test_model_change(self):
        """Confirm transient aspect updates."""
        # Setup
        N_OBSERVERS = 5
        OBSERVERS = [StubObserver() for _ in range(N_OBSERVERS)]
        target = BMARKUPGTK3.ControlMarkupTrackGtk3()
        for observer in OBSERVERS:
            target.attach(p_observer=observer)
        STORE = target._model.get_store_ui()
        target._changed = False
        # Test
        target.on_model_change()
        for observer in OBSERVERS:
            assert observer.store_ui is STORE
        assert target._changed


class TestModelMarkupGtk3:
    """Unit tests for :class:`.ModelMarkupGtk3`."""

    def test_get_store_py(self):
        """Confirm return of model text as string."""
        # Setup
        target = BMARKUPGTK3.ModelMarkupGtk3()
        TEXT = 'The Parrot Sketch'
        ALL = -1
        target._store_ui.set_text(TEXT, ALL)
        # Test
        assert TEXT == target.get_store_py()

    def test_get_store_ui(self):
        """Contirm return of model text as GTK 3 object."""
        # Setup
        target = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        assert target.get_store_ui() is target._store_ui

    def test_new_store_ui(self):
        """Confirm storage object construction."""
        # Setup
        target = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        assert isinstance(target._store_ui, BMARKUPGTK3.StoreUiTextMarkup)

    def test_set_store_ui(self):
        """Confirm text and markup set."""
        # Setup
        target = BMARKUPGTK3.ModelMarkupGtk3()
        TEXT = 'The Parrot Sketch'
        # Test
        target.set_store_ui(p_store_py=TEXT)
        assert TEXT == target._store_ui.get_text()


class TestModule:
    """Unit tests for module-level components of :mod:`.text_markup_gtk3`."""

    @pytest.mark.parametrize('CONSTANT, EXPECT', [
        (BMARKUPGTK3.VOID_ID_OBSERVER_MARKUP, 0),
        ])
    def test_constants(self, CONSTANT, EXPECT):
        """Confirm constant definitions.

        :param CONSTANT: constant under test.
        :param EXPECT: expected value of constant.
        """
        # Setup
        # Test
        assert EXPECT == CONSTANT

    def test_id_observer(self):
        """Confirm observer identity."""
        # Setup
        OBSERVER = None
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))
        # Test
        assert ID_OBSERVER == (
            BMARKUPGTK3.id_observer_markup(p_observer=OBSERVER))

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BMARKUPGTK3.IdObserverMarkup.__qualname__,
            'NewType.<locals>.new_type'),
        (BMARKUPGTK3.IdObserverMarkup.__dict__['__supertype__'], int),
        (BMARKUPGTK3.ObserverMarkupAbc,
            BABC.ObserverAbc[BMARKUPGTK3.StoreUiTextMarkup]),
        (BMARKUPGTK3.StoreUiTextMarkup, Gtk.EntryBuffer),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
