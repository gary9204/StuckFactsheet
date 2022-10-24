"""
Unit tests for :mod:`.text_markup_gtk3`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import pytest
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC
import factsheet.ui_bricks.ui_gtk3.text_markup.text_markup_gtk3 as BMARKUPGTK3

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402


class TestControlMarkupGtk3:
    """Unit tests for :class:`.ControlMarkupGtk3`."""

    class StubObserver(BMARKUPGTK3.ObserverMarkupAbc):
        """Stub for :data:`.ObserverMarkupAbc`."""

        def __init__(self):
            self.store_ui = None

        def on_notice(self, p_store_ui, **kwargs):
            """Record GTK 3 store object to confirm call."""
            del kwargs
            self.store_ui = p_store_ui

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ControlMarkupGtk3(p_model=MODEL)
        assert target._model is MODEL
        assert isinstance(target._changed, bool)
        assert not target._changed
        assert isinstance(target._observers, typing.MutableMapping)
        assert not target._observers

    def test_attach(self):
        """| Confirm control will notify observer.
        | Case: initially control not notifying observer.
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        OBSERVER = self.StubObserver()
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
        OBSERVER = self.StubObserver()
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
        OBSERVER = self.StubObserver()
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
        OBSERVER = self.StubObserver()
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

    @pytest.mark.parametrize('CHANGED', [
        False,
        True
        ])
    def test_has_changed(self, CHANGED):
        """Confirm return matches change state.

        :param CHANGED: change state
        """
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
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
        target = BMARKUPGTK3.ControlMarkupGtk3()
        EXPECT = not CHANGED
        # Test
        target._changed = CHANGED
        assert target.has_not_changed() is EXPECT

    def test_mark_changed(self):
        """Confirm text marked as changed"""
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        # Test
        target._changed = False
        target.mark_changed()
        assert target._changed

    def test_mark_not_changed(self):
        """Confirm text marked as not changed"""
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        # Test
        target._changed = True
        target.mark_not_changed()
        assert not target._changed

    def test_new_model(self):
        """Confirm model construction."""
        # Setup
        target = BMARKUPGTK3.ControlMarkupGtk3()
        # Test
        assert isinstance(target._model, BMARKUPGTK3.ModelMarkupGtk3)
        assert target._model._control is target

    def test_notify(self):
        """Confirm notification of observers."""
        # Setup
        N_OBSERVERS = 5
        OBSERVERS = [self.StubObserver() for _ in range(N_OBSERVERS)]
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
        OBSERVERS = [self.StubObserver() for _ in range(N_OBSERVERS)]
        target = BMARKUPGTK3.ControlMarkupGtk3()
        for observer in OBSERVERS:
            target.attach(p_observer=observer)
        STORE = target._model.get_store_ui()
        target.mark_not_changed()
        # Test
        target.on_model_change()
        assert target.has_changed()
        for observer in OBSERVERS:
            assert observer.store_ui is STORE


class TestModelMarkupGtk3:
    """Unit tests for :class:`.ModelMarkupGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        CONTROL = BMARKUPGTK3.ControlMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ModelMarkupGtk3(p_control=CONTROL)
        assert target._control is CONTROL

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

    def test_new_control(self):
        """Confirm control construction."""
        # Setup
        target = BMARKUPGTK3.ModelMarkupGtk3()
        # Test
        assert isinstance(target._control, BMARKUPGTK3.ControlMarkupGtk3)
        assert target._control._model is target

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
