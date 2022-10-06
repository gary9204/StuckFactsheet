"""
Unit tests for identity attributes common to Factsheet model components.
See :class:`~.IdCore`.

.. include:: /test/refs_include_pytest.txt
"""
import copy
from pathlib import Path
import pickle
import pytest
import re
import typing

import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE


class PatchIdCore(MIDCORE.IdCore[BUI.x_b_t_ModelTextMarkup,
                                 BUI.ModelTextStyled,
                                 BUI.x_b_t_ModelTextMarkup]):
    """Stub subclass for testing :class:`.IdCore` methods."""

    def __init__(self, p_name, p_summary, p_title, **kwargs):
        self._name = BUI.x_b_t_ModelTextMarkup(p_name)
        self._summary = BUI.ModelTextStyled(p_summary)
        self._title = BUI.x_b_t_ModelTextMarkup(p_title)
        super().__init__(**kwargs)


class TestIdCore:
    """Unit tests for :class:`.IdCore`."""

    def test_eq(self):
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
        source = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        TEXT = 'Something completely different.'
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: name difference.
        target = copy.deepcopy(source)
        target.name._set_persist(TEXT)
        assert not source.__eq__(target)
        # Test: summary difference.
        target = copy.deepcopy(source)
        target.summary._set_persist(TEXT)
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target.title._set_persist(TEXT)
        assert not source.__eq__(target)
        # Test: equivalent
        target = copy.deepcopy(source)
        target._stale = True
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        source = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        source._stale = True
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source._name == target._name
        assert source._summary == target._summary
        assert source._title == target._title
        assert not target._stale

    def test_init(self):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        # Test
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert isinstance(target._stale, bool)
        assert not target._stale

    @pytest.mark.parametrize('ATTR, HINT', [
        ('_name', '~ModelName'),
        ('_summary', '~ModelSummary'),
        ('_title', '~ModelTitle'),
        ])
    def test_init_attr(self, ATTR, HINT):
        """| Confirm initialization.
        | Case: missing attribute definition.

        :param ATTR: missing attribute.
        :param HINT: type hint for missing attribute.
        """
        # Setup
        class PatchPartial(MIDCORE.IdCore[BUI.x_b_t_ModelTextMarkup,
                                          BUI.ModelTextStyled,
                                          BUI.x_b_t_ModelTextMarkup]):
            """Partially defines attributes for  :func:`.IdCore.__init__`."""

            def __init__(self, p_name, p_summary, p_title, **kwargs):
                self._name = BUI.x_b_t_ModelTextMarkup(p_name)
                self._summary = BUI.ModelTextStyled(p_summary)
                self._title = BUI.x_b_t_ModelTextMarkup(p_title)
                delattr(self, ATTR)
                super().__init__(**kwargs)

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        ERROR = re.escape('PatchPartial: IdCore subclasses must define '
                          '{} attribute with type {} and then call '
                          'super().__init__()'.format(ATTR, HINT))
        # Test
        with pytest.raises(AttributeError, match=ERROR):
            _ = PatchPartial(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)

    def test_init_extra(self):
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
            _ = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                            extra='Oops!')

    @pytest.mark.parametrize('IS_STALE', [
        True,
        False,
        ])
    def test_is_fresh(self, IS_STALE, monkeypatch):
        """Confirm negation of :meth:`~.IdCore.is_stale`.

        :param IS_STALE: state to report for sheet.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
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
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # Test
        assert target.has_not_changed() is not IS_STALE
        assert patch.called

    def test_is_stale(self):
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
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
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

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('name', '_name'),
        ('summary', '_summary'),
        ('title', '_title'),
        ])
    def test_property_access(
            self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        attr = getattr(target, NAME_ATTR)
        CLASS = MIDCORE.IdCore
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_set_fresh(self):
        """Confirm instance marked fresh."""
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    @pytest.mark.parametrize('ATTR', [
        '_name',
        '_summary',
        '_title',
        ])
    def test_set_fresh_attr(self, ATTR):
        """Confirm all attributes marked fresh.

        :param ATTR: name of attribute.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = True
        attribute = getattr(target, ATTR)
        attribute.set_stale()
        # Test
        target.set_fresh()
        assert attribute.has_not_changed()

    def test_set_stale(self, monkeypatch):
        """Confirm instance marked stale and attributes unchanged.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchAttrSetStale:
            def __init__(self):
                self.called = False

            def set_stale(self):
                self.called = True

        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        target = PatchIdCore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        target._stale = False

        patch = PatchAttrSetStale()
        monkeypatch.setattr(BTEXT.ModelText, 'set_stale', patch.set_stale)
        # Test
        target.set_stale()
        assert not patch.called
        assert target._stale


class TestIdCoreTypes:
    """Unit tests for type hint definitions in :mod:`.idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (type(MIDCORE.ModelName), typing.TypeVar),
        (MIDCORE.ModelName.__constraints__, (
            BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)),
        (type(MIDCORE.ModelSummary), typing.TypeVar),
        (MIDCORE.ModelSummary.__constraints__, (
            BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)),
        (type(MIDCORE.ModelTitle), typing.TypeVar),
        (MIDCORE.ModelTitle.__constraints__, (
            BUI.x_b_t_ModelTextMarkup, BUI.ModelTextStyled)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
