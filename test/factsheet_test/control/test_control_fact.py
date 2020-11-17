"""
Unit test for control to add and remove views of :class:`~.Fact'
attributes.  See :mod:`~.control_fact`.
"""
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_fact as CFACT
import factsheet.model.fact as MFACT


class TestControlFact:
    """Unit tests for :class:`.ControlFact`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        # Test
        target = CFACT.ControlFact(p_fact=FACT)
        assert target._fact is FACT

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP, HAS_SETTER', [
        ('_fact', 'fact', False),
        ('_fact', 'idcore', False),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP, HAS_SETTER):
        """Confirm values and access limits of properties."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        target_prop = getattr(CFACT.ControlFact, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        REPLACE = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        if HAS_SETTER:
            target_prop.fset(target, REPLACE)
            value_attr = getattr(target, NAME_ATTR)
            assert value_attr is REPLACE
        else:
            assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.parametrize('ATTACH, ATTR, GET_STORE', [
        ('attach_note', 'note', 'get_buffer'),
        ('attach_names_aspect', 'names_aspect', 'get_model'),
        ])
    def test_attach(self, ATTACH, ATTR, GET_STORE):
        """Confirm view associated with attribute of fact."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        attach = getattr(target, ATTACH)
        attr = getattr(FACT, ATTR)
        # Test
        view = attach()
        get_store = getattr(view, GET_STORE)
        assert get_store() is attr._model

    @pytest.mark.parametrize('ATTACH, DETACH, ATTR, GET_STORE', [
        ('attach_note', 'detach_note', 'note', 'get_buffer'),
        ('attach_names_aspect', 'detach_names_aspect', 'names_aspect',
            'get_model'),
        ])
    def test_detach(self, ATTACH, DETACH, ATTR, GET_STORE):
        """Confirm view disassociated from attribute of fact."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        attach = getattr(target, ATTACH)
        view = attach()
        get_store = getattr(view, GET_STORE)
        detach = getattr(target, DETACH)
        attr = getattr(FACT, ATTR)
        # Test
        detach(view)
        assert get_store() is not attr._model

    @pytest.mark.parametrize('NAME', [
        'Plain',
        'Status',
        ])
    def test_attach_detach_aspect(self, NAME):
        """Confirm view association/disassociation with aspect of fact."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        # NAME = 'Plain'
        aspect = FACT._aspects[NAME]
        TYPE_VIEW = BUI.ViewAspectAny
        # Test
        view = target.attach_aspect(NAME)
        assert isinstance(view, TYPE_VIEW)
        id_view = id(view)
        assert aspect._views[id_view] is view
        target.detach_aspect(NAME, view)
        with pytest.raises(KeyError):
            _ = aspect._views[id_view]

    def test_attach_aspect_missing(self):
        """Confirm view returned for missing aspect of fact."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        NAME = 'Dinsdale?'
        WARNING = ('Aspect \'{}\' not found. Please report omission.'
                   ''.format(NAME))
        # Test
        view = target.attach_aspect(NAME)
        assert isinstance(view, CFACT.ViewAspectMissing)
        assert WARNING == view.get_text()

    def test_detach_aspect_missing(self, monkeypatch):
        """Confirm noop for missing aspect of fact."""
        # Setup
        class PatchAspect:
            def __init__(self): self.called = False

            def detach_view(self, _view): self.called = True

        patch_aspect = PatchAspect()
        monkeypatch.setattr(
            BUI.BridgeAspect, 'detach_view', patch_aspect.detach_view)

        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        NAME = 'Dinsdale?'
        VIEW = None
        # Test
        target.detach_aspect(NAME, VIEW)
        assert not patch_aspect.called


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_fact`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (CFACT.ViewAspectMissing, BUI.ViewAspectMissing),
        (CFACT.ViewAspect, BUI.ViewAspectAny),
        (CFACT.ViewNameFact, BUI.ViewTextMarkup),
        (CFACT.ViewNoteFact, BUI.ViewTextFormat),
        (CFACT.ViewSummaryFact, BUI.ViewTextFormat),
        (CFACT.ViewTitleFact, BUI.ViewTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
