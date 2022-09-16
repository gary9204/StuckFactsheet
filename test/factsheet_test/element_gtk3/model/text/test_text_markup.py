"""
Unit tests for text storage element facade base class.  See
:mod:`.element_gtk3.model.text.text_markup`.

.. include:: /test/refs_include_pytest.txt
"""
import gi  # type: ignore[import]
from pathlib import Path
import pickle

import factsheet.element_gtk3.model.text.text_markup as EMMARKUP

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402


class TestModelTextMarkup:
    """Unit tests for
    :class:`.element_gtk3.model.text.text_markup.TextMarkup`.
    """

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        source = EMMARKUP.TextMarkup()
        TEXT = 'Something completely different'
        source.set_internal(TEXT)
        source._stale = True
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source.to_external() == target.to_external()
        # assert not target._stale

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TEXT = 'The Parrot Sketch'
        # Test
        target = EMMARKUP.TextMarkup(p_text=TEXT)
        assert isinstance(target._ui_model, Gtk.EntryBuffer)
        assert TEXT == target._ui_model.get_text()

    def test_to_external(self):
        """Confirm return of external representation."""
        # Setup
        target = EMMARKUP.TextMarkup()
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        # Test
        assert TEXT == target.to_external()

    def test_new_model(self):
        """Confirm GTK 3 model element returned."""
        # Setup
        target = EMMARKUP.TextMarkup()
        # Test
        ui_model_new = target.new_ui_model()
        assert isinstance(ui_model_new, Gtk.EntryBuffer)

    def test_set_internal(self):
        """Confirm content set from external representation."""
        # Setup
        target = EMMARKUP.TextMarkup()
        # target_buffer = target._ui_model
        TEXT = 'The Parrot Sketch.'
        ALL = -1
        target._ui_model.set_text(TEXT, ALL)
        # target.set_fresh()
        TEXT_NEW = 'Something completely different.'
        # Test
        target.set_internal(TEXT_NEW)
        assert TEXT_NEW == target._ui_model.get_text()
