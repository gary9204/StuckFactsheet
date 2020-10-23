"""
Unit tests for fact-level model. See :mod:`~.fact`.
"""
# import dataclasses as DC
# import logging
import enum
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import typing

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.model.fact as MFACT


class TestFact:
    """Unit tests for :class:`~.Fact`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: identity difference
        #. Case: formats difference
        #. Case: note difference
        #. Case: status difference
        #. Case: value difference
        #. Case: Equivalence
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        source = Fact(p_topic=None)
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        NOTE = 'A Norwegian Blue.'
        source.note.text = NOTE
        TEXT = 'Something completely different'
        # Test: type difference
        assert not source.__eq__(TITLE)
        # Test: identity difference
        target = Fact(p_topic=None)
        target.title.text = TEXT
        target.note.text = NOTE
        assert not source.__eq__(target)
        # Test: formats difference
        target = Fact(p_topic=None)
        target.title.text = TITLE
        target.note.text = NOTE
        target._formats['Oops'] = None
        assert not source.__eq__(target)
        # Test: note difference
        target = Fact(p_topic=None)
        target.title.text = TITLE
        target.note.text = TEXT
        assert not source.__eq__(target)
        # Test: status difference
        target = Fact(p_topic=None)
        target.title.text = TITLE
        target.note.text = NOTE
        target._status = MFACT.StatusOfFact.DEFINED
        assert not source.__eq__(target)
        # Test: value difference
        target = Fact(p_topic=None)
        target.title.text = TITLE
        target.note.text = NOTE
        target._value = TEXT
        assert not source.__eq__(target)
        # Test: Equivalence
        target = Fact(p_topic=None)
        target.title.text = TITLE
        target.note.text = NOTE
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        source = Fact(p_topic=None)
        NAME = 'Parrot'
        source.name.text = NAME
        SUMMARY = 'The parrot is a Norwegian Blue.'
        source.summary.text = SUMMARY
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)
        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert source._tag != target._tag
        assert source == target

    def test_init(self):
        """Confirm initialization."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        KEY = 'Plain'
        # Test
        target = Fact(p_topic=None)
        assert not target._stale
        assert isinstance(target._formats, dict)
        assert isinstance(target._formats[KEY], ADAPT.FormatValuePlain)
        assert target._names_formats is None
        assert isinstance(target._name, MFACT.NameFact)
        assert isinstance(target._note, MFACT.NoteFact)
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert isinstance(target._summary, MFACT.SummaryFact)
        assert id(target) == target._tag
        assert isinstance(target._title, MFACT.TitleFact)
        assert target._value is None

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_names_formats', 'names_formats'),
        ('_name', 'name'),
        ('_note', 'note'),
        ('_status', 'status'),
        ('_summary', 'summary'),
        ('_title', 'title'),
        ('_value', 'value'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr is value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_check(self):
        """Confirm default check."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        STATUS = MFACT.StatusOfFact.DEFINED
        target._status = STATUS
        VALUE = 'Something completely different.'
        target._value = VALUE
        target.set_fresh()
        KEY = 'Plain'
        # Test
        result = target.check()
        assert result is STATUS
        assert target.is_stale()
        assert VALUE == target._formats[KEY]._value_gtk

    def test_clear(self):
        """Confirm default clear."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        STATUS = MFACT.StatusOfFact.UNCHECKED
        target._status = STATUS
        VALUE = 'Something completely different.'
        target._value = VALUE
        _ = target.check()
        target.set_fresh()
        KEY = 'Plain'
        BLANK = ''
        # Test
        target.clear()
        assert target.is_stale()
        assert BLANK == target._formats[KEY]._value_gtk

    def test_get_format(self):
        """| Confirm format matches name.
        | Case: format supported by fact.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        NAME = 'Plain'
        # Test
        assert target.get_format(NAME) is target._formats[NAME]

    def test_get_format_missing(self):
        """| Confirm format matches name.
        | Case: format not supported by fact.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        NAME = 'Oops!'
        # Test
        assert target.get_format(NAME) is None

    def test_is_stale(self):
        """Confirm return is accurate.

        #. Case: Fact stale, identity fresh, note fresh
        #. Case: Fact fresh, identity stale, note fresh
        #. Case: Fact fresh, identity fresh, note stake
        #. Case: Fact fresh, identity fresh, note fresh
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        # Test: Fact stale, identity fresh, note fresh
        target.set_fresh()
        target._stale = True
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity stale, note fresh
        target.set_fresh()
        target.summary.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity fresh, note stake
        target.set_fresh()
        target.note.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity fresh, note fresh
        target.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    @pytest.mark.skip(reason='replacing with property')
    def test_names_format(self):
        """Confirm format names."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        # Test
        assert target.names_format() == target._formats.keys()

    def test_set_fresh(self):
        """Confirm instance marked fresh."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        target._stale = True
        # Test
        target.set_fresh()
        assert not target._stale

    @pytest.mark.parametrize('ATTR', [
        'name',
        'note',
        'summary',
        'title',
        ])
    def test_set_fresh_attr(self, ATTR):
        """Confirm all attributes marked fresh."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        target._stale = True
        attribute = getattr(target, ATTR)
        attribute.set_stale()
        # Test
        target.set_fresh()
        assert not target._stale
        assert attribute.is_fresh()


class TestStatusOfFact:
    """Unit tests for enumeration :class:`.StatusOfFact`."""

    def test_types(self):
        """Confirm enumeration class nad members."""
        # Setup
        # Test
        assert issubclass(MFACT.StatusOfFact, enum.Enum)
        assert MFACT.StatusOfFact.BLOCKED
        assert MFACT.StatusOfFact.DEFINED
        assert MFACT.StatusOfFact.UNCHECKED
        assert MFACT.StatusOfFact.UNDEFINED


class TestTypes:
    """Unit tests for type hit definitions in :mod:`.fact`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (MFACT.NameFact, ADAPT.AdaptTextMarkup),
        (MFACT.NoteFact, ADAPT.AdaptTextFormat),
        (MFACT.SummaryFact, ADAPT.AdaptTextFormat),
        (MFACT.TagFact.__supertype__, int),  # type: ignore[attr-defined]
        (MFACT.TitleFact, ADAPT.AdaptTextMarkup),
        (type(MFACT.TopicOpaque), typing.TypeVar),
        (MFACT.ValueOpaque, ADAPT.ValueOpaque),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
