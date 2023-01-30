"""
Unit tests for :mod:`.ui_factory`.

.. include:: /test/refs_include_pytest.txt
"""
from gi.repository import Gtk   # type: ignore[import]
import importlib
import pytest

import factsheet.ui_bricks.ui_factory as FACTORY
import factsheet.ui_bricks.ui_abc.brick_abc as BABC
import factsheet.ui_bricks.ui_gtk3.markup_gtk3 as BMARKUPGTK3


class Sheet:
    """TBD"""

    def __init__(self):
        """TBD"""
        self._name = FACTORY.new_brick.markup.new_model()

    def get_name(self) -> BABC.ModelAbc:
        """TBD"""
        return self._name


class ControlSheet:
    """TBD"""

    def __init__(self):
        """TBD"""
        self._model = Sheet()
        model_name = self._model.get_name()
        self._control_name = (
            FACTORY.new_brick.markup.new_control(p_model=model_name))
        self._control_track_name = (
            FACTORY.new_brick.markup.new_control_track(p_model=model_name))


class TestModule:
    """TBD"""

    def test_ui_factory(self):
        """TBD"""
        # Setup
        target = ControlSheet()
        # Test
        assert target._model is not None
        model_name = target._model.get_name()
        assert model_name is not None
        assert isinstance(model_name, BMARKUPGTK3.ModelMarkupGtk3)
        control_name = target._control_name
        assert control_name is not None
        assert isinstance(control_name, BMARKUPGTK3.ControlMarkupGtk3)
        control_track_name = target._control_track_name
        assert control_track_name is not None
        assert isinstance(control_track_name,
                          BMARKUPGTK3.ControlMarkupTrackGtk3)

    def test_check_gtk_fail(self, monkeypatch, caplog):
        """Confirm GTK version check.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        MAJOR = 9
        monkeypatch.setattr(Gtk, 'MAJOR_VERSION', MAJOR)
        MINOR = 8
        monkeypatch.setattr(Gtk, 'MINOR_VERSION', MINOR)
        MICRO = 7
        monkeypatch.setattr(Gtk, 'MICRO_VERSION', MICRO)
        N_LOGS = 1
        LAST = -1
        log_message = ('Unsupported user interface toolkit: GTK {}.{}.{}'
                       ''.format(MAJOR, MINOR, MICRO))
        # Test
        with pytest.raises(NotImplementedError):
            _ = importlib.reload(FACTORY)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'CRITICAL' == record.levelname
