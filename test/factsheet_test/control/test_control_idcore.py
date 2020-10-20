"""
Unit tests for generic control to add and remove views of
:class:`~.IdCore` identity attributes.  See :mod:`~.control_idcore`.
"""
import pytest   # type: ignore[import]
import re
import typing

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.control.control_idcore as CIDCORE


class TestControlIdCore:
    """Unit tests for :class:`.ControlIdCore`."""

    def test_init(self, patch_idcore):
        """| Confirm initialization.
        | Case: nominal.
        """
        # Setup
        IDCORE = patch_idcore()
        # Test
        target = CIDCORE.ControlIdCore(p_model=IDCORE)
        assert target._model is IDCORE

    def test_init_extra(self, patch_idcore):
        """| Confirm initialization.
        | Case: extra keyword argument.
        """
        # Setup
        IDCORE = patch_idcore()
        ERROR = re.escape("ControlIdCore.__init__() called with extra "
                          "argument(s): {'extra': 'Oops!'}")
        # Test
        with pytest.raises(TypeError, match=ERROR):
            _ = CIDCORE.ControlIdCore(p_model=IDCORE, extra='Oops!')

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
        """Confirm add and remove requests relayed to identity attribute."""
        # Setup
        IDCORE = patch_idcore()
        target = CIDCORE.ControlIdCore(p_model=IDCORE)
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
