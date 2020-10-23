"""
Unit tests for generic control to add and remove views of
:class:`~.IdCore` identity attributes.  See :mod:`~.control_idcore`.
"""
import pytest   # type: ignore[import]
# import re
import typing

import factsheet.adapt_gtk.adapt as ADAPT
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

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = CIDCORE.ControlIdCore()

    @pytest.mark.parametrize('NAME_PROP, HAS_SETTER', [
        ('idcore', False),
        ])
    def test_property_abstract(self, NAME_PROP, HAS_SETTER):
        """Confirm access limits of each abstract property."""
        # Setup
        class PatchAbstract(CIDCORE.ControlIdCore):

            @property
            def idcore(self):
                prop = getattr(CIDCORE.ControlIdCore, 'idcore')
                prop.fget(self)

        _ = PatchAbstract()  # Confirms abstract method override.
        # Test
        target = getattr(PatchAbstract, NAME_PROP)
        with pytest.raises(NotImplementedError):
            target.fget(self)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                target.fset(self, 'Oops!')
        else:
            assert target.fset is None
        assert target.fdel is None

    @pytest.mark.parametrize('METHOD, ATTR_TARGET, ATTRS_OTHER, MARKER', [
        ('attach_name', 'name', ['summary', 'title'], 'attached'),
        ('detach_name', 'name', ['summary', 'title'], 'detached'),
        ('attach_summary', 'summary', ['name', 'title'], 'attached'),
        ('detach_summary', 'summary', ['name', 'title'], 'detached'),
        ('attach_title', 'title', ['name', 'summary'], 'attached'),
        ('detach_title', 'title', ['name', 'summary'], 'detached'),
        ])
    def test_attach_detach(
            self, patch_idcore, METHOD, ATTR_TARGET, ATTRS_OTHER, MARKER):
        """Confirm control relays requests to identity."""
        # Setup
        IDCORE = patch_idcore()
        target = PatchControlIdCore(p_idcore=IDCORE)
        method = getattr(target, METHOD)
        attr_t = getattr(IDCORE, ATTR_TARGET)
        marks_t = getattr(attr_t, MARKER)
        attrs_o = [getattr(IDCORE, attr) for attr in ATTRS_OTHER]
        marks_o = [getattr(attr, MARKER) for attr in attrs_o]
        VIEW = 'A shrubbery'
        # Test
        method(VIEW)
        for mark in marks_o:
            assert not mark
        assert [VIEW] == marks_t


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_idcore`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (type(CIDCORE.ViewNameAdapt), typing.TypeVar),
        (CIDCORE.ViewNameAdapt.__constraints__, (ADAPT.ViewTextFormat,
                                                 ADAPT.ViewTextMarkup,
                                                 ADAPT.ViewTextStatic)),
        (type(CIDCORE.ViewSummaryAdapt), typing.TypeVar),
        (CIDCORE.ViewSummaryAdapt.__constraints__, (ADAPT.ViewTextFormat,
                                                    ADAPT.ViewTextMarkup,
                                                    ADAPT.ViewTextStatic)),
        (type(CIDCORE.ViewTitleAdapt), typing.TypeVar),
        (CIDCORE.ViewTitleAdapt.__constraints__, (ADAPT.ViewTextFormat,
                                                  ADAPT.ViewTextMarkup,
                                                  ADAPT.ViewTextStatic)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
