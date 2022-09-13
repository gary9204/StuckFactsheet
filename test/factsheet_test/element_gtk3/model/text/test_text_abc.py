"""
Unit tests for text storage element facade base class.  See
:mod:`.element_gtk3.model.text.text_abc`.
"""
import pytest

import factsheet.element_gtk3.model.text.text_abc as EMTEXT


class PatchText(EMTEXT.TextAbc[str]):
    """:class:`.element_gtk3.model.text.text_abc.TextAbc` subclass
    with stubs for abstract methods.

        :param args: patch and superclass positional parameters.
        :param kwargs: patch and superclass keyword parameters.
    """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def new_ui_model(self):
        """Stub: return empty string."""
        # self._ui_model = ''
        return ''

    def set_internal(self, p_external):
        """Stub: set model to string."""
        self._ui_model = str(p_external)

    def to_external(self):
        """Stub: return model string."""
        return self._ui_model


class TestModelText:
    """Unit tests for :class:`.element_gtk3.model.text.text_abc.TextAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (EMTEXT.TextAbc, 'new_ui_model'),
        (EMTEXT.TextAbc, 'set_internal'),
        (EMTEXT.TextAbc, 'to_external'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: class that should be abstract.
        :param NAME_METHOD: method that should be abstract.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self):
        """Confirm equality comparison.

        #. Case: not a text model.
        #. Case: different text.
        #. Case: equal
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        source = PatchText()
        source.set_internal(TEXT)
        # Test: not a text attribute.
        assert not source.__eq__(TEXT)
        # Test: different content.
        TEXT_DIFFER = 'Something completely different.'
        target = PatchText()
        target.set_internal(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equal
        target = PatchText()
        target.set_internal(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    # @pytest.mark.skip
    # def test_get_set_state(self, tmp_path):
    #     """Confirm conversion to and from pickle format.
    #
    #     :param tmp_path: built-in fixture `Pytest tmp_path`_.
    #     """
    #     # Setup
    #     PATH = Path(str(tmp_path / 'get_set.fsg'))
    #     source = PatchText()
    #     TEXT = 'The Parrot Sketch'
    #     source._set_persist(TEXT)
    #     source._stale = True
    #     # Test
    #     with PATH.open(mode='wb') as io_out:
    #         pickle.dump(source, io_out)
    #     with PATH.open(mode='rb') as io_in:
    #         target = pickle.load(io_in)
    #     assert source.to_external() == target.to_external()
    #     assert not target._stale

    def test_init(self):
        """| Confirm initialization.
        | Case: non-default text.
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        # Test
        target = PatchText(p_text=TEXT)
        assert hasattr(target, '_ui_model')
        assert TEXT == target._ui_model
        # assert isinstance(target._stale, bool)
        # assert not target._stale

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default text.
        """
        # Setup
        BLANK = ''
        # Test
        target = PatchText()
        assert hasattr(target, '_ui_model')
        assert BLANK == target._ui_model
        # assert isinstance(target._stale, bool)
        # assert not target._stale

    def test_str(self):
        """Confirm return is class name with model text. """
        # Setup
        TEXT = 'The Parrot Sketch'
        target = PatchText()
        target.set_internal(p_external=TEXT)
        expect = '<{}: {}>'.format(type(target).__name__, TEXT)
        # Test
        assert expect == str(target)

    # @pytest.mark.skip
    # def test_alike(self):
    #     """Confirm return matches state. """
    #     # Setup
    #     target = PatchText()
    #     target._stale = False
    #     # Test
    #     assert target.is_fresh()
    #     target._stale = True
    #     assert not target.is_fresh()

    # @pytest.mark.skip
    # def test_differ(self):
    #     """Confirm return matches state. """
    #     # Setup
    #     target = PatchText()
    #     target._stale = False
    #     # Test
    #     assert not target.is_stale()
    #     target._stale = True
    #     assert target.is_stale()

    # @pytest.mark.skip
    # def test_set_alike(self):
    #     """Confirm attribute marked fresh. """
    #     # Setup
    #     target = PatchText()
    #     target._stale = True
    #     # Test
    #     target.set_fresh()
    #     assert not target._stale

    # @pytest.mark.skip
    # def test_set_differ(self):
    #     """Confirm attribute marked stale. """
    #     # Setup
    #     target = PatchText()
    #     target._stale = False
    #     # Test
    #     target.set_stale()
    #     assert target._stale

    def test_text(self):
        """Confirm access limits of text property."""
        # Setup
        target_class = PatchText
        target = target_class()
        TEXT = 'The Parrot Sketch'
        target.set_internal(TEXT)
        TEXT_NEW = 'Something completely different.'
        # Test
        assert target_class.text.fget is not None
        assert TEXT == target.text
        assert target_class.text.fset is not None
        target.text = TEXT_NEW
        assert TEXT_NEW == target.to_external()
        assert target_class.text.fdel is None
