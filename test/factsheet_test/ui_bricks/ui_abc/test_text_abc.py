"""
Unit tests for :mod:`~.ui_abc.text_abc`.
"""
import pytest

import factsheet.ui_bricks.ui_abc.text_abc as BTEXT


class TestControlTextAbc:
    """Unit tests for :class:`.ControlTextAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.ControlTextAbc, 'new_model'),
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


class TestModelTextAbc:
    """Unit tests for :class:`.ModelTextAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.ModelTextAbc, 'get_store_py'),
        (BTEXT.ModelTextAbc, 'new_control'),
        (BTEXT.ModelTextAbc, 'set_store_ui'),
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


class TestFactoryTextMarkupAbc:
    """Unit tests for :class:`.FactoryTextMarkupAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.FactoryTextMarkupAbc, '__call__'),
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


class TestFactoryTextStyledAbc:
    """Unit tests for :class:`.FactoryTextStyledAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BTEXT.FactoryTextStyledAbc, '__call__'),
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


class TestModule:
    """Unit tests for module-level components of :mod:`.text_markup_gtk3`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BTEXT.StorePyTextMarkup, str),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
