"""
Unit tests for identity attributes common to Factsheet model components.
See :class:`~.IdCore`."""
import copy
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import re
import typing

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE


class TestIdCore:
    """Unit tests for :class:`.IdCore`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (MIDCORE.IdCore, '_new_model'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR, HAS_SETTER', [
        ('name', '_name', False),
        ('summary', '_summary', False),
        ('title', '_title', False),
        ])
    def test_property_access(
            self, patch_idcore, NAME_PROP, NAME_ATTR, HAS_SETTER):
        """Confirm access limits of each property."""
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        attr = getattr(target, NAME_ATTR)
        CLASS = MIDCORE.IdCore
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert attr.text == target_prop.fget(target)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                target_prop.fset(None, 'Oops!')
        else:
            assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_eq(self, patch_idcore):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: name difference.
        #. Case: summary difference.
        #. Case: title difference.
        #. Case: equivalent
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        source = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        TEXT = 'Something completely different.'
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: name difference.
        target = copy.deepcopy(source)
        target._name.text = TEXT
        assert not source.__eq__(target)
        # Test: summary difference.
        target = copy.deepcopy(source)
        target._summary.text = TEXT
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target._title.text = TEXT
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
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        source = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        # Test
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert NAME == target._name.text
        assert target._name.is_fresh()
        assert SUMMARY == target._summary.text
        assert target._summary.is_fresh()
        assert TITLE == target._title.text
        assert target._title.is_fresh()
        assert isinstance(target._stale, bool)
        assert target.is_fresh()

    def test_init_extra(self, patch_idcore):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'

        ERROR = re.escape("IdCore.__init__() called with extra "
                          "argument(s): {'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                             extra='Oops!')

    @pytest.mark.parametrize('IS_STALE', [
        True,
        False,
        ])
    def test_is_fresh(self, IS_STALE, monkeypatch, patch_idcore):
        """Confirm negation of :meth:`~.BridgeText.is_stale."""
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
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

    @pytest.mark.parametrize('NEW_VIEW, ATTR', [
        ('new_view_name', '_name'),
        ('new_view_summary', '_summary'),
        ('new_view_title', '_title'),
        ])
    def test_new_view(self, patch_idcore, NEW_VIEW, ATTR):
        """Confirm control relays requests to identity."""
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        new_view = getattr(target, NEW_VIEW)
        attr = getattr(target, ATTR)
        # Test
        view = new_view()
        assert view.get_buffer() is attr._model

    def test_set_fresh(self, patch_idcore):
        """Confirm instance marked fresh."""
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    @pytest.mark.parametrize('ATTR', [
        '_name',
        '_summary',
        '_title',
        ])
    def test_set_fresh_attr(self, patch_idcore, ATTR):
        """Confirm all attributes marked fresh."""
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = False

        patch = PatchAttrSetStale()
        monkeypatch.setattr(BTEXT.BridgeText, 'set_stale', patch.set_stale)
        # Test
        target.set_stale()
        assert not patch.called
        assert target._stale


class TestIdCoreTypes:
    """Unit tests for type hint definitions in :mod:`.idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(MIDCORE.ViewName), typing.TypeVar),
        (MIDCORE.ViewName.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        (type(MIDCORE.ViewSummary), typing.TypeVar),
        (MIDCORE.ViewSummary.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        (type(MIDCORE.ViewTitle), typing.TypeVar),
        (MIDCORE.ViewTitle.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
