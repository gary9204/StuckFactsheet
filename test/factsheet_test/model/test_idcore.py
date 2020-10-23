"""
Unit tests for identity attributes common to Factsheet model components.
See :class:`~.IdCore`."""
import copy
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import re
import typing

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.model.idcore as MIDCORE


class TestIdCore:
    """Unit tests for :class:`.IdCore`."""

    def test_abstract_class(self):
        """Confirm  class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = MIDCORE.IdCore()

    def test_eq(self, patch_idcore):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: name difference.
        #. Case: summary difference.
        #. Case: title difference.
        #. Case: equivalent
        """
        # Setup
        source = patch_idcore()
        NAME = 'Parrot'
        source.name.text = NAME
        SUMMARY = 'The parrot is a Norwegian Blue.'
        source.summary.text = SUMMARY
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        TEXT = 'Something completely different.'
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: name difference.
        target = copy.deepcopy(source)
        target.name.text = TEXT
        assert not source.__eq__(target)
        # Test: summary difference.
        target = copy.deepcopy(source)
        target.summary.text = TEXT
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target.title.text = TEXT
        assert not source.__eq__(target)
        # Test: equivalent
        target = copy.deepcopy(source)
        target._stale = True
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_idcore):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        source = patch_idcore()
        NAME = 'Parrot'
        source.name.text = NAME
        SUMMARY = 'The parrot is a Norwegian Blue.'
        source.summary.text = SUMMARY
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        source._stale = True
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert not target._stale
        source._stale = False
        assert source == target

    def test_init(self, patch_idcore):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        # Test
        target = patch_idcore()
        assert isinstance(target._stale, bool)
        assert not target._stale

    def test_init_extra(self, patch_idcore):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        ERROR = re.escape("IdCore.__init__() called with extra "
                          "argument(s): {'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = patch_idcore(extra='Oops!')

    @pytest.mark.parametrize('IS_STALE', [
        True,
        False,
        ])
    def test_is_fresh(self, IS_STALE, monkeypatch, patch_idcore):
        """Confirm negation of :meth:`~.AdaptText.is_stale."""
        # Setup
        class PatchIsStale:
            def __init__(self, p_result):
                self.called = False
                self.result = p_result

            def is_stale(self):
                self.called = True
                return self.result

        patch = PatchIsStale(IS_STALE)
        monkeypatch.setattr(MIDCORE.IdCore, 'is_stale', patch.is_stale)
        target = patch_idcore()
        # Test
        assert target.is_fresh() is not IS_STALE
        assert patch.called

    def test_is_stale(self, patch_idcore):
        """Confirm return is accurate.

        #. Case: IdCore stale, name, summary, and title fresh
        #. Case: IdCore fresh, name stale, summary fresh, title fresh
        #. Case: IdCore fresh, name fresh, summary stale, title fresh
        #. Case: IdCore fresh, name fresh, summary fresh, title stale
        #. Case: IdCore fresh, name, summary, and title fresh
        """
        # Setup
        target = patch_idcore()
        # Test: IdCore stale, name, summary, and title fresh
        target._stale = True
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: IdCore fresh, name stale, summary fresh, title fresh
        target._stale = False
        target._name.set_stale()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: IdCore fresh, name fresh, summary stale, title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_stale()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: IdCore fresh, name fresh, summary fresh, title stale
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: IdCore fresh, name, summary and title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_set_fresh(self, patch_idcore):
        """Confirm instance marked fresh."""
        # Setup
        target = patch_idcore()
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    @pytest.mark.parametrize('ATTR', [
        'name',
        'summary',
        'title',
        ])
    def test_set_fresh_attr(self, patch_idcore, ATTR):
        """Confirm all attributes marked fresh."""
        # Setup
        target = patch_idcore()
        target._stale = True
        attribute = getattr(target, ATTR)
        attribute.set_stale()
        # Test
        target.set_fresh()
        assert not target._stale
        assert attribute.is_fresh()

    def test_set_stale(self, monkeypatch, patch_idcore):
        """Confirm instance marked stale and attributes unchanged."""
        # Setup
        class PatchAttrSetStale:
            def __init__(self):
                self.called = False

            def set_stale(self):
                self.called = True

        patch = PatchAttrSetStale()
        monkeypatch.setattr(ADAPT.AdaptText, 'set_stale', patch.set_stale)
        target = patch_idcore()
        target._stale = False
        # Test
        target.set_stale()
        assert not patch.called
        assert target._stale


class TestIdCoreAbstract:
    """Unit tests for abstract properties of :class:`.IdCore`."""

    def test_abstract_class(self):
        """Confirm  class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = MIDCORE.IdCore()

    @pytest.mark.parametrize('NAME_PROP, HAS_SETTER', [
        ('name', False),
        ('summary', False),
        ('title', False),
        ])
    def test_property_abstract(
            self, patch_idcore_abstract, NAME_PROP, HAS_SETTER):
        """Confirm access limits of each abstract property."""
        # Setup
        _ = patch_idcore_abstract()  # Confirms abstract method override.
        # Test
        target = getattr(patch_idcore_abstract, NAME_PROP)
        with pytest.raises(NotImplementedError):
            target.fget(None)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                target.fset(None, 'Oops!')
        else:
            assert target.fset is None
        assert target.fdel is None


class TestIdCoreTypes:
    """Unit tests for type hint definitions in :mod:`.idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(MIDCORE.NameAdapt), typing.TypeVar),
        (MIDCORE.NameAdapt.__constraints__, (ADAPT.AdaptTextFormat,
                                             ADAPT.AdaptTextMarkup,
                                             ADAPT.AdaptTextStatic)),
        (type(MIDCORE.SummaryAdapt), typing.TypeVar),
        (MIDCORE.SummaryAdapt.__constraints__, (ADAPT.AdaptTextFormat,
                                                ADAPT.AdaptTextMarkup,
                                                ADAPT.AdaptTextStatic)),
        (type(MIDCORE.TitleAdapt), typing.TypeVar),
        (MIDCORE.TitleAdapt.__constraints__, (ADAPT.AdaptTextFormat,
                                              ADAPT.AdaptTextMarkup,
                                              ADAPT.AdaptTextStatic)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
