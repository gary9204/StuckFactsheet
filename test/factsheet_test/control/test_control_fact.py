"""
Unit test for control to add and remove views of :class:`~.Fact'
attributes.  See :mod:`~.control_fact`.
"""
import logging
import pytest  # type: ignore[import]
import typing

import factsheet.adapt_gtk.adapt as ADAPT
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
        """Confirm access limits of each concrete property."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        target_prop = getattr(CFACT.ControlFact, NAME_PROP)
        REPLACE = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        # Test
        value_prop = getattr(target, NAME_PROP)
        assert target_prop.fget is not None
        value_attr = getattr(target, NAME_ATTR)
        assert value_prop == value_attr
        if HAS_SETTER:
            target_prop.fset(target, REPLACE)
            value_attr = getattr(target, NAME_ATTR)
            assert value_attr is REPLACE
        else:
            assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.skip(reason='Pending update of Outline classes for Fact')
    def test_missing_cases(self):
        'Reminder of incomplete testing'
        'attach_names_formats'
        'detach_names_formats'
        pass

    @pytest.mark.parametrize('ATTACH, DETACH, ATTR, VIEW', [
        ('attach_note', 'detach_note', 'note', CFACT.ViewNoteFact()),
        ])
    def test_attach_detach_view(self, ATTACH, DETACH, ATTR, VIEW):
        """Confirm control relays requests to fact."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        attach = getattr(target, ATTACH)
        detach = getattr(target, DETACH)
        attr = getattr(FACT, ATTR)
        id_view = id(VIEW)
        # Test
        attach(VIEW)
        assert attr._views[id_view] is VIEW
        detach(VIEW)
        with pytest.raises(KeyError):
            _ = attr._views[id_view]

    @pytest.mark.skip
    @pytest.mark.parametrize('ATTACH, DETACH, FORMAT, ASPECT', [
        ('attach_format_plain', 'detach_format_plain',
         'Plain', ADAPT.AspectValuePlain()),
        ])
    def test_attach_detach_aspect(self, ATTACH, DETACH, FORMAT, ASPECT):
        """Confirm control relays requests to fact formats."""
        # Setup
        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        target = CFACT.ControlFact(p_fact=FACT)
        attach = getattr(target, ATTACH)
        detach = getattr(target, DETACH)
        format_value = FACT._formats[FORMAT]
        id_aspect = id(ASPECT)
        # Test
        attach(ASPECT)
        assert format_value._aspects[id_aspect] is ASPECT
        detach(ASPECT)
        with pytest.raises(KeyError):
            _ = format_value._aspects[id_aspect]

    @pytest.mark.parametrize('METHOD', [
        'attach_format_plain',
        'detach_format_plain',
        ])
    def test_format_missing(self, monkeypatch, PatchLogger, METHOD):
        """Confirm logging of requests to missing fact formats."""
        # Setup
        class PatchFormat:
            def __init__(self): self.called = False

            def attach_aspect(self, _aspect): self.called = True

            def detach_aspect(self, _aspect): self.called = True

        patch_format = PatchFormat()
        monkeypatch.setattr(ADAPT.FormatValuePlain, 'attach_aspect',
                            patch_format.attach_aspect)
        monkeypatch.setattr(ADAPT.FormatValuePlain, 'detach_aspect',
                            patch_format.detach_aspect)

        FACT = MFACT.Fact[typing.Any, MFACT.ValueOpaque](p_topic=None)
        monkeypatch.setattr(
            MFACT.Fact, 'get_format', lambda _self, _name: None)
        target = CFACT.ControlFact(p_fact=FACT)
        method = getattr(target, METHOD)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'error', patch_logger.error)
        log_message = ('Format missing for {}.{}'
                       ''.format(type(target).__name__, METHOD))
        # Test
        method(None)
        assert not patch_format.called
        assert patch_logger.called
        assert PatchLogger.T_ERROR == patch_logger.level
        assert log_message == patch_logger.message


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_fact`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (CFACT.ViewNameFact, ADAPT.ViewTextMarkup),
        # (CFACT.ViewNameFact, ADAPT.ViewTextMarkup),
        (CFACT.ViewNoteFact, ADAPT.ViewTextFormat),
        (CFACT.ViewSummaryFact, ADAPT.ViewTextFormat),
        (CFACT.ViewTitleFact, ADAPT.ViewTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
