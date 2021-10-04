"""
Unit tests for identity attributes common to Factsheet model components.
See :class:`~.IdCore`.
"""
import copy
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import re
import typing

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE


class PatchIdCore(MIDCORE.IdCore[
        BUI.ModelTextMarkup, BUI.ModelTextStyled, BUI.ModelTextMarkup]):
    """TBD"""

    def __init__(self):
        self._name = BUI.ModelTextMarkup()
        self._summary = BUI.ModelTextStyled()
        self._title = BUI.ModelTextStyled()
        super().__init__()


class TestIdCore:
    """Unit tests for :class:`.IdCore`."""

    @pytest.mark.skip
    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: name difference.
        #. Case: summary difference.
        #. Case: title difference.
        #. Case: equivalent
        """
        # Setup
        NAME = BUI.ModelTextMarkup()
        NAME.text = 'Parrot'
        SUMMARY = BUI.ModelTextStyled()
        SUMMARY.text = 'The parrot is a Norwegian Blue.'
        TITLE = BUI.ModelTextMarkup()
        TITLE.text = 'The Parrot Sketch'
        source = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

    @pytest.mark.skip
    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        NAME = BUI.ModelTextMarkup()
        NAME.text = 'Parrot'
        SUMMARY = BUI.ModelTextStyled()
        SUMMARY.text = 'The parrot is a Norwegian Blue.'
        TITLE = BUI.ModelTextMarkup()
        TITLE.text = 'The Parrot Sketch'
        source = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        source._stale = True
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert NAME == target._name
        assert SUMMARY == target._summary
        assert TITLE == target._title
        assert not target._stale

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        # NAME = BUI.ModelTextMarkup()
        # NAME.text = 'Parrot'
        # SUMMARY = BUI.ModelTextStyled()
        # SUMMARY.text = 'The parrot is a Norwegian Blue.'
        # TITLE = BUI.ModelTextMarkup()
        # TITLE.text = 'The Parrot Sketch'
        # Test
        # target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target = PatchIdCore()
        assert isinstance(target._name, BUI.ModelTextMarkup)
        assert isinstance(target._summary, BUI.ModelTextStyled)
        assert isinstance(target._title, BUI.ModelTextStyled)
        assert isinstance(target._stale, bool)
        assert not target._stale

    @pytest.mark.skip
    def test_init_extra(self):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        ERROR = re.escape("IdCore.__init__() called with extra "
                          "argument(s): {'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY,
                               p_title=TITLE, extra='Oops!')

    @pytest.mark.skip
    @pytest.mark.parametrize('IS_STALE', [
        True,
        False,
        ])
    def test_is_fresh(self, IS_STALE, monkeypatch):
        """Confirm negation of :meth:`~.IdCore.is_stale`."""
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
        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # Test
        assert target.is_fresh() is not IS_STALE
        assert patch.called

    @pytest.mark.skip
    def test_is_stale(self):
        """Confirm return is accurate.

        #. Case: IdCore stale, name, summary, and title fresh
        #. Case: IdCore fresh, name stale, summary fresh, title fresh
        #. Case: IdCore fresh, name fresh, summary stale, title fresh
        #. Case: IdCore fresh, name fresh, summary fresh, title stale
        #. Case: IdCore fresh, name, summary, and title fresh
        """
        # Setup
        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

    @pytest.mark.skip
    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR, HAS_SETTER', [
        ('name', '_name', False),
        ('summary', '_summary', False),
        ('title', '_title', False),
        ])
    def test_property_access(
            self, NAME_PROP, NAME_ATTR, HAS_SETTER):
        """Confirm access limits of each property."""
        # Setup
        NAME = BUI.ModelTextMarkup()
        NAME.text = 'Parrot'
        SUMMARY = BUI.ModelTextStyled()
        SUMMARY.text = 'The parrot is a Norwegian Blue.'
        TITLE = BUI.ModelTextMarkup()
        TITLE.text = 'The Parrot Sketch'
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

    @pytest.mark.skip
    def test_set_fresh(self):
        """Confirm instance marked fresh."""
        # Setup
        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    @pytest.mark.skip
    @pytest.mark.parametrize('ATTR', [
        '_name',
        '_summary',
        '_title',
        ])
    def test_set_fresh_attr(self, ATTR):
        """Confirm all attributes marked fresh."""
        # Setup
        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = True
        attribute = getattr(target, ATTR)
        attribute.set_stale()
        # Test
        target.set_fresh()
        assert attribute.is_fresh()

    @pytest.mark.skip
    def test_set_stale(self, monkeypatch):
        """Confirm instance marked stale and attributes unchanged."""
        # Setup
        class PatchAttrSetStale:
            def __init__(self):
                self.called = False

            def set_stale(self):
                self.called = True

        NAME = BUI.ModelTextMarkup()
        SUMMARY = BUI.ModelTextStyled()
        TITLE = BUI.ModelTextMarkup()
        target = MIDCORE.IdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = False

        patch = PatchAttrSetStale()
        monkeypatch.setattr(BTEXT.ModelText, 'set_stale', patch.set_stale)
        # Test
        target.set_stale()
        assert not patch.called
        assert target._stale


class TestIdCoreTypes:
    """Unit tests for type hint definitions in :mod:`.idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(MIDCORE.ModelName), typing.TypeVar),
        (MIDCORE.ModelName.__constraints__, (
            BUI.ModelTextMarkup, BUI.ModelTextStyled)),
        (type(MIDCORE.ModelSummary), typing.TypeVar),
        (MIDCORE.ModelSummary.__constraints__, (
            BUI.ModelTextMarkup, BUI.ModelTextStyled)),
        (type(MIDCORE.ModelTitle), typing.TypeVar),
        (MIDCORE.ModelTitle.__constraints__, (
            BUI.ModelTextMarkup, BUI.ModelTextStyled)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
