"""
Unit tests for fact-level model. See :mod:`~.fact`.
"""
import enum
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI
import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE


class PatchTopic(MIDCORE.IdCore[
        MFACT.NameTopic, MFACT.SummaryTopic, MFACT.TitleTopic]):

    def __init__(self):
        self._stale = False
        self._name = MFACT.NameTopic
        self._summary = MFACT.SummaryTopic
        self._title = MFACT.TitleTopic
        self._tag = MFACT.TagTopic(id(self))

    @property
    def name(self): return self._name

    @property
    def summary(self): return self._summary

    @property
    def title(self): return self._title

    @property
    def tag(self): return self._tag


class TestAspectStatus:
    """Unit tests for :class:`~.AspectStatus`."""

    @pytest.mark.parametrize('STATUS', MFACT.StatusOfFact)
    def test_transcribe(self, STATUS):
        """| Confirm peersistent form of status.
        | Case: status is not None.
        """
        # Setup
        target = MFACT.AspectStatus()
        # Test
        assert STATUS.name == target.transcribe(STATUS)

    def test_transcribe_none(self):
        """| Confirm peersistent form of status.
        | Case: status is None.
        """
        # Setup
        target = MFACT.AspectStatus()
        STATUS = MFACT.StatusOfFact.UNCHECKED
        # Test
        assert STATUS.name == target.transcribe(None)


class TestFact:
    """Unit tests for :class:`~.Fact`."""

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: topic tag difference
        #. Case: identity difference.
        #. Case: aspects difference.
        #. Case: note difference.
        #. Case: status difference.
        #. Case: value difference.
        #. Case: Equivalence.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = PatchTopic()
        source = Fact(p_topic=TOPIC)
        TITLE = 'The Parrot Sketch'
        source.title.text = TITLE
        NOTE = 'A Norwegian Blue.'
        source.note.text = NOTE
        TEXT = 'Something completely different'
        # Test: type difference
        assert not source.__eq__(TITLE)
        # Test: topic tag difference
        target = Fact(p_topic=PatchTopic())
        target.title.text = TITLE
        target.note.text = NOTE
        assert not source.__eq__(target)
        # Test: identity difference
        target = Fact(p_topic=TOPIC)
        target.title.text = TEXT
        target.note.text = NOTE
        assert not source.__eq__(target)
        # Test: aspects difference
        target = Fact(p_topic=TOPIC)
        target.title.text = TITLE
        target.note.text = NOTE
        target._aspects['Oops'] = None
        assert not source.__eq__(target)
        # Test: note difference
        target = Fact(p_topic=TOPIC)
        target.title.text = TITLE
        target.note.text = TEXT
        assert not source.__eq__(target)
        # Test: status difference
        target = Fact(p_topic=TOPIC)
        target.title.text = TITLE
        target.note.text = NOTE
        target._status = MFACT.StatusOfFact.DEFINED
        assert not source.__eq__(target)
        # Test: value difference
        target = Fact(p_topic=TOPIC)
        target.title.text = TITLE
        target.note.text = NOTE
        target._value = TEXT
        assert not source.__eq__(target)
        # Test: Equivalence
        target = Fact(p_topic=TOPIC)
        target.title.text = TITLE
        target.note.text = NOTE
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = PatchTopic()
        source = Fact(p_topic=TOPIC)
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
        assert source._tag != target._tag
        assert not target._stale
        assert source == target

    def test_init(self):
        """| Confirm initialization.
        | Case: attributes except aspects.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = PatchTopic()
        # Test
        target = Fact(p_topic=TOPIC)
        assert not target._stale
        assert isinstance(target._aspects, dict)
        assert isinstance(target._names_aspect, type(MFACT.NamesAspect()))
        assert isinstance(target._name, MFACT.NameFact)
        assert isinstance(target._note, MFACT.NoteFact)
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert isinstance(target._summary, MFACT.SummaryFact)
        assert id(target) == target._tag
        assert isinstance(target._title, MFACT.TitleFact)
        assert target._topic is TOPIC
        assert target._value is None

    @pytest.mark.parametrize('KEY, ASPECT', [
        ('Plain', type(MFACT.AspectValuePlain())),
        ('Status', MFACT.AspectStatus),
        ])
    def test_init_aspects(self, KEY, ASPECT):
        """| Confirm initialization.
        | Case: aspects and aspect names attributes.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        # Test
        target = Fact(p_topic=None)
        assert isinstance(target._aspects[KEY], ASPECT)
        assert set(target._names_aspect.items()) == target._aspects.keys()

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_names_aspect', 'names_aspect'),
        ('_name', 'name'),
        ('_note', 'note'),
        ('_status', 'status',),
        ('_summary', 'summary'),
        ('_tag', 'tag'),
        ('_title', 'title'),
        ('_value', 'value'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm values and access limits of properties."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('name', 'name_topic'),
        ('summary', 'summary_topic'),
        ('tag', 'tag_topic'),
        ('title', 'title_topic'),
        ])
    def test_property_topic(self, NAME_ATTR, NAME_PROP):
        """Confirm values and access limits of topic properties."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = PatchTopic()
        target = Fact(p_topic=TOPIC)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_attr = getattr(target._topic, NAME_ATTR)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    @pytest.mark.parametrize('NAME_PROP', [
        'name_topic',
        'summary_topic',
        'title_topic',
        ])
    def test_property_topic_except(self, NAME_PROP):
        """| Confirm property exceptions for malformed topic.
        | Case: not tag property
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        ERROR = 'Malformed topic! please report.'
        target = Fact(p_topic=None)
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        # Test
        result = target_prop.fget(target)
        assert ERROR == result.text

    def test_property_tag_except(self):
        """| Confirm property exceptions for malformed topic.
        | Case: tag property
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        ERROR = -1
        target = Fact(p_topic=None)
        target_prop = getattr(MFACT.Fact, 'tag_topic')
        # Test
        result = target_prop.fget(target)
        assert ERROR == result

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
        # Test
        result = target.check()
        assert result is STATUS
        assert target.is_stale()
        assert VALUE == target._aspects['Plain']._model
        assert STATUS.name == target._aspects['Status']._model

    def test_clear(self):
        """Confirm default clear."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        STATUS = MFACT.StatusOfFact.UNDEFINED
        target._status = STATUS
        VALUE = 'Something completely different.'
        target._value = VALUE
        _ = target.check()
        target.set_fresh()
        BLANK = ''
        STATUS_NEW = MFACT.StatusOfFact.UNCHECKED
        # Test
        target.clear()
        assert target.is_stale()
        assert BLANK == target._aspects['Plain']._model
        assert STATUS_NEW.name == target._aspects['Status']._model

    def test_get_aspect(self):
        """| Confirm aspect matches name.
        | Case: fact has given aspect.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        NAME = 'Plain'
        # Test
        assert target.get_aspect(NAME) is target._aspects[NAME]

    def test_get_aspect_missing(self):
        """| Confirm aspect matches name.
        | Case: fact does not have given aspect.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        target = Fact(p_topic=None)
        NAME = 'Dinsdale?'
        # Test
        assert target.get_aspect(NAME) is None

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
    """Unit tests for type hint definitions in :mod:`.fact`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (MFACT.Aspect, BUI.BridgeAspect),
        (MFACT.AspectValuePlain, BUI.BridgeAspectPlain[typing.Any]),
        (MFACT.NameFact, BUI.BridgeTextMarkup),
        (MFACT.NamesAspect, BUI.BridgeOutlineSelect[str]),
        (MFACT.NameTopic, BUI.BridgeTextMarkup),
        (MFACT.NoteFact, BUI.BridgeTextFormat),
        (MFACT.PersistAspectStatus, BUI.PersistAspectPlain),
        (MFACT.SummaryFact, BUI.BridgeTextFormat),
        (MFACT.SummaryTopic, BUI.BridgeTextFormat),
        (MFACT.TagFact.__supertype__, int),  # type: ignore[attr-defined]
        (MFACT.TagTopic.__supertype__, int),  # type: ignore[attr-defined]
        (MFACT.TitleFact, BUI.BridgeTextMarkup),
        (MFACT.TitleTopic, BUI.BridgeTextMarkup),
        (type(MFACT.TopicOpaque), typing.TypeVar),
        (MFACT.TopicOpaque.__constraints__, ()),
        (type(MFACT.ValueOpaque), typing.TypeVar),
        (MFACT.ValueOpaque.__constraints__, ()),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
