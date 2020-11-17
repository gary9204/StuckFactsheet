"""
Unit tests for generic control to add and remove views of
:class:`~.IdCore` identity attributes.  See :mod:`~.control_idcore`.
"""
import pytest   # type: ignore[import]
# import re
import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_idcore as CIDCORE


class PatchControlIdCore(CIDCORE.ControlIdCore):
    """ """

    def __init__(self, p_idcore):
        self._idcore = p_idcore

    @property
    def idcore(self):
        return self._idcore


class TestControlIdCore:
    """Unit tests for :class:`.ControlIdCore`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (CIDCORE.ControlIdCore, 'idcore'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    @pytest.mark.parametrize('NAME_PROP, HAS_SETTER', [
        ('idcore', False),
        ])
    def test_property_access(self, NAME_PROP, HAS_SETTER):
        """Confirm access limits of each property."""
        # Setup
        # Test
        target = getattr(CIDCORE.ControlIdCore, NAME_PROP)
        with pytest.raises(NotImplementedError):
            target.fget(self)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                target.fset(self, 'Oops!')
        else:
            assert target.fset is None
        assert target.fdel is None

    @pytest.mark.parametrize('ATTACH, ATTR', [
        ('attach_name', 'name'),
        ('attach_summary', 'summary'),
        ('attach_title', 'title'),
        ])
    def test_attach(self, patch_idcore, ATTACH, ATTR):
        """Confirm control relays requests to identity."""
        # Setup
        IDCORE = patch_idcore()
        target = PatchControlIdCore(p_idcore=IDCORE)
        attach = getattr(target, ATTACH)
        attr = getattr(IDCORE, ATTR)
        # Test
        view = attach()
        assert view.get_buffer() is attr._model

    @pytest.mark.parametrize('ATTACH, DETACH, ATTR', [
        ('attach_name', 'detach_name', 'name'),
        ('attach_summary', 'detach_summary', 'summary'),
        ('attach_title', 'detach_title', 'title'),
        ])
    def test_detach(self, patch_idcore, ATTACH, DETACH, ATTR):
        """Confirm control relays requests to identity."""
        # Setup
        IDCORE = patch_idcore()
        target = PatchControlIdCore(p_idcore=IDCORE)
        attach = getattr(target, ATTACH)
        view = attach()
        detach = getattr(target, DETACH)
        attr = getattr(IDCORE, ATTR)
        # Test
        detach(view)
        assert view.get_buffer() is not attr._model


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(CIDCORE.ViewName), typing.TypeVar),
        (CIDCORE.ViewName.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        (type(CIDCORE.ViewSummary), typing.TypeVar),
        (CIDCORE.ViewSummary.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        (type(CIDCORE.ViewTitle), typing.TypeVar),
        (CIDCORE.ViewTitle.__constraints__, (
            BUI.ViewTextFormat, BUI.ViewTextMarkup, BUI.ViewTextStatic)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
