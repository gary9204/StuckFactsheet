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
    """Unit tests for :class:`.ControlTextMarkupGtk3`."""

    class StubObserver(BMARKUPGTK3.ObserverMarkupAbc):

        def on_notice(self, p_store_ui, **kwargs):
            del kwargs
            self._store_ui = p_store_ui

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ControlTextMarkupGtk3(p_model=MODEL)
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
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
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
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        OBSERVER = self.StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))
        target._observers[ID_OBSERVER] = OBSERVER

        N_LOGS = 1
        LAST = -1
        log_message = ('Observer already being notified. id: {} '
                       '(ControlTextMarkupGtk3.attach)'.format(
                           hex(ID_OBSERVER)))
        # Test
        target.attach(OBSERVER)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_detach(self):
        """| Confirm control will not notify observer.
        | Case: initially control already notifying observer.
        """
        # Setup
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
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
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        OBSERVER = self.StubObserver()
        ID_OBSERVER = BMARKUPGTK3.IdObserverMarkup(id(OBSERVER))

        N_LOGS = 1
        LAST = -1
        log_message = ('Observer not being notified. id: {} '
                       '(ControlTextMarkupGtk3.detach)'.format(
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
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
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
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        EXPECT = not CHANGED
        # Test
        target._changed = CHANGED
        assert target.has_not_changed() is EXPECT

    def test_mark_changed(self):
        """Confirm text marked as changed"""
        # Setup
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        target._changed = False
        target.mark_changed()
        assert target._changed

    def test_mark_not_changed(self):
        """Confirm text marked as not changed"""
        # Setup
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        target._changed = True
        target.mark_not_changed()
        assert not target._changed

    def test_new_model(self):
        """Confirm model construction."""
        # Setup
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        assert isinstance(target._model, BMARKUPGTK3.ModelTextMarkupGtk3)
        assert target._model._control is target


class TestModelMarkupGtk3:
    """Unit tests for :class:`.ModelTextMarkupGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        CONTROL = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ModelTextMarkupGtk3(p_control=CONTROL)
        assert target._control is CONTROL

    def test_new_store_ui(self):
        """Confirm storage object construction."""
        # Setup
        target = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        assert isinstance(target._store_ui, BMARKUPGTK3.StoreUiTextMarkup)

    def test_new_control(self):
        """Confirm control construction."""
        # Setup
        target = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        assert isinstance(target._control, BMARKUPGTK3.ControlTextMarkupGtk3)
        assert target._control._model is target


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
        (BMARKUPGTK3.StoreUiDisplay, Gtk.Label),
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
