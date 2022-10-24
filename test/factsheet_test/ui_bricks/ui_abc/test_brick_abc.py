"""
Unit tests for :mod:`.brick_abc`.
"""
from pathlib import Path
import pickle
import pytest
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC


class TestBypassAbc:
    """Unit tests for :class:`.BypassAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.BypassAbc, 'bypass'),
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


class TestControlAbc:
    """Unit tests for :class:`.ControlAbc`."""

    stub_model = 'The Parrot Sketch'

    class StubControl(BABC.ControlAbc[str, str]):
        """Class with stubs for :class:`.ControlAbc` abstract methods."""
        def on_model_change(self): pass

        def new_model(self): return TestControlAbc.stub_model

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.ControlAbc, 'on_model_change'),
        (BABC.ControlAbc, 'new_model'),
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

    def test_init(self):
        """| Confirm initialization.
        | Case: with model parameter.
        """
        # Setup
        MODEL = 'Something completely different'
        # Test
        target = TestControlAbc.StubControl(p_model=MODEL)
        assert target._model is MODEL

    def test_init_default(self):
        """| Confirm initialization.
        | Case: without model parameter.
        """
        # Setup
        # Test
        target = TestControlAbc.StubControl()
        assert target._model is TestControlAbc.stub_model


class TestModelAbc:
    """Unit tests for :class:`.ModelAbc`."""

    stub_control = 'Something completely different'
    stub_store = 'Oops'

    class StubModel(BABC.ModelAbc[str, str]):
        """Class with stubs for :class:`.ModelAbc` abstract methods."""

        def get_store_py(self): return str(self._store_ui)

        def get_store_ui(self): return self._store_ui

        # def new_control(self): return str(TestModelAbc.stub_control)

        def new_store_ui(self): return str('Oops')

        def set_store_ui(self, p_store_py): self._store_ui = p_store_py

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.ModelAbc, 'get_store_py'),
        (BABC.ModelAbc, 'get_store_ui'),
        # (BABC.ModelAbc, 'new_control'),
        (BABC.ModelAbc, 'new_store_ui'),
        (BABC.ModelAbc, 'set_store_ui'),
        # (BABC.ModelAbc, 'TBD'),
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

        #. Case: type difference.
        #. Case: stored content difference.
        #. Case: equivalent.
        """
        # Setup
        TEXT = 'Parrot'
        source = TestModelAbc.StubModel()
        source.set_store_ui(TEXT)
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: storage element difference.
        TEXT_DIFFER = 'Something completely different.'
        target = TestModelAbc.StubModel()
        target.set_store_ui(TEXT_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = TestModelAbc.StubModel()
        target.set_store_ui(TEXT)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        PATH = Path(str(tmp_path / 'get_set.fsg'))
        # CONTROL = 'The Parrot Sketch'
        source = TestModelAbc.StubModel()
        TEXT = 'Parrot'
        source.set_store_ui(TEXT)
        # Test
        with PATH.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        # assert TestModelAbc.stub_control == target._control
        assert not hasattr(target, 'ex_store')
        assert source.get_store_py() == target.get_store_py()

    def test_init(self):
        """| Confirm initialization.
        | Case: with control parameter.
        """
        # Setup
        # CONTROL = 'The Parrot Sketch'
        # Test
        target = TestModelAbc.StubModel()
        # assert target._control is CONTROL
        assert TestModelAbc.stub_store == target._store_ui

    def test_init_default(self):
        """| Confirm initialization.
        | Case: without control parameter.
        """
        # Setup
        # Test
        target = TestModelAbc.StubModel()
        # assert target._control is TestModelAbc.stub_control
        assert TestModelAbc.stub_store == target._store_ui

    def test_str(self):
        """Confirm string representation."""
        # Setup
        TEXT = 'Parrot'
        target = TestModelAbc.StubModel()
        target.set_store_ui(TEXT)
        expect = '<StubModel: {}>'.format(TEXT)
        # Test
        assert expect == str(target)

    @pytest.mark.skip(reason='Moving control to toolkit-specific class')
    def test_get_control(self):
        """Confirm control access."""
        # Setup
        CONTROL = 'The Parrot Sketch'
        # Test
        target = TestModelAbc.StubModel(p_control=CONTROL)
        assert target.get_control() is CONTROL


class TestModule:
    """Unit tests for module-level components of :mod:`.brick_abc`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(BABC.StorePyOpaque), typing.TypeVar),
        (type(BABC.StoreUiOpaque), typing.TypeVar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestObserverAbc:
    """Unit tests for :class:`.ObserverAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.ObserverAbc, 'on_notice'),
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


class TestSubjectAbc:
    """Unit tests for :class:`.SubjectAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.SubjectAbc, 'attach'),
        (BABC.SubjectAbc, 'detach'),
        (BABC.SubjectAbc, 'notify'),
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


class TestTrackChangeAbc:
    """Unit tests for :class:`.TrackChangesAbc`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BABC.TrackChangesAbc, 'has_changed'),
        (BABC.TrackChangesAbc, 'has_not_changed'),
        (BABC.TrackChangesAbc, 'mark_changed'),
        (BABC.TrackChangesAbc, 'mark_not_changed'),
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
