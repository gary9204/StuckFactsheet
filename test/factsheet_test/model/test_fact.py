"""
Unit tests for fact-level model. See :mod:`~.fact`.
"""
import enum
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI
import factsheet.model.aspect as MASPECT
import factsheet.model.fact as MFACT
import factsheet.model.idcore as MIDCORE


@pytest.fixture
def fact_sample_with_view(request, fact_sample):
    """| Fixture to return sample fact with a view.
    | Case: view other than aspect view
    """
    fact = fact_sample()
    marker = request.node.get_closest_marker("name_method")
    name_method = marker.args[0]
    view = None
    method = getattr(fact, name_method, None)
    if method is not None:
        view = method()
    yield fact, view
    # Teardown
    if view is not None:
        view.destroy()


@pytest.fixture
def fact_sample_with_view_aspect(request, fact_sample):
    """| Fixture to return sample fact with a view.
    | Case: aspect view
    """
    fact = fact_sample()
    marker = request.node.get_closest_marker("name_aspect")
    name_aspect = marker.args[0]
    view = fact.new_view_aspect(p_name_aspect=name_aspect)
    yield fact, view
    # Teardown
    view.destroy()


class PatchTopic(MIDCORE.IdCore[
        BUI.ViewTextMarkup, BUI.ViewTextTagged, BUI.ViewTextMarkup]):
    """Stub for Topic class."""

    def __init__(self, **kwargs):
        super().__init__(p_name='Oops! No name', p_summary='Oops! no summary',
                         p_title='Oops! no title', **kwargs)
        self._tag = id(self)

    def _new_model(self):
        name = BUI.ModelTextMarkup()
        summary = BUI.ModelGtkTextBuffer()
        title = BUI.ModelTextMarkup()
        return name, summary, title

    @property
    def tag(self): return self._tag


class TestFact:
    """Unit tests for :class:`~.Fact`."""

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: identity difference.
        #. Case: topic difference
        #. Case: aspects difference.
        #. Case: aspect names difference.
        #. Case: note difference.
        #. Case: status difference.
        #. Case: value difference.
        #. Case: equivalence.
        """
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        TOPIC = PatchTopic()
        source = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        NOTE = 'A Norwegian Blue.'
        source._note.text = NOTE
        TEXT_DIFF = 'Something completely different'
        TOPIC_DIFF = PatchTopic()
        TOPIC_DIFF._name.text = TEXT_DIFF
        # Test: type difference
        assert not source.__eq__(TITLE)
        # Test: identity difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        target._title.text = TEXT_DIFF
        assert not source.__eq__(target)
        # Test: topic difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC_DIFF)
        target._note.text = NOTE
        assert not source.__eq__(target)
        # Test: aspects difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        target._aspects['Oops'] = None
        assert not source.__eq__(target)
        # Test: aspect names difference.
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        target._names_aspects.insert_before(TEXT_DIFF)
        assert not source.__eq__(target)
        # Test: note difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = TEXT_DIFF
        assert not source.__eq__(target)
        # Test: status difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        target._status = MFACT.StatusOfFact.DEFINED
        assert not source.__eq__(target)
        # Test: value difference
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        target._value = NOTE
        assert not source.__eq__(target)
        # Test: Equivalence
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        target._note.text = NOTE
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, fact_sample):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))
        source = fact_sample()
        NOTE = 'A Norwegian Blue.'
        source._note.text = NOTE
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
        """Confirm initialization."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        NAME = 'Parrot'
        SUMMARY = 'The parrot is a Norwegian Blue.'
        TITLE = 'The Parrot Sketch'
        TOPIC = PatchTopic()
        WARNING = 'This fact does not support the aspect you requested'
        STATUS = MFACT.StatusOfFact.UNDEFINED
        NAMES_ASPECTS = {'Plain'}
        # Test
        target = Fact(p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                      p_topic=TOPIC)
        assert isinstance(target._name, MFACT.NameFact)
        assert NAME == target.name
        assert isinstance(target._summary, MFACT.SummaryFact)
        assert SUMMARY == target.summary
        assert isinstance(target._title, MFACT.TitleFact)
        assert TITLE == target.title
        assert not target._stale
        assert isinstance(target._aspects, dict)
        assert isinstance(target._aspect_missing, MFACT.AspectValuePlain)
        view_aspect_missing = target._aspect_missing.new_view()
        assert WARNING == view_aspect_missing.get_text()
        view_aspect_missing.destroy()
        assert isinstance(
            target._names_aspects, type(MFACT.NamesAspects()))
        assert isinstance(target._note, MFACT.NoteFact)
        assert target._status is STATUS
        assert isinstance(target._aspect_status, MFACT.AspectStatus)
        view_status = target._aspect_status.new_view()
        assert STATUS.name == view_status.get_text()
        view_status.destroy()
        assert id(target) == target._tag
        assert isinstance(target._aspect_tag, MFACT.AspectTagFact)
        view_tag = target._aspect_tag.new_view()
        assert str(target._tag) == view_tag.get_text()
        view_tag.destroy()
        assert target._topic is TOPIC
        assert target._value is None
        assert isinstance(target._aspects['Plain'], MFACT.AspectValuePlain)
        assert NAMES_ASPECTS == set(target._names_aspects.items())

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_note', 'note'),
        ('_status', 'status'),
        ('_tag', 'tag'),
        ('_value', 'value'),
        ])
    def test_property(self, fact_sample, NAME_ATTR, NAME_PROP):
        """Confirm values of and access limits of properties."""
        # Setup
        target = fact_sample()
        VALUE = 'Something completely different'
        target._value = VALUE
        target_prop = getattr(MFACT.Fact, NAME_PROP)
        value_attr = getattr(target, NAME_ATTR)
        # Test
        assert target_prop.fget is not None
        assert value_attr is target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_add_aspect(self, fact_sample):
        """Confirm addition of aspect."""
        # Setup
        target = fact_sample()
        NAME = 'Something completely different'
        aspect = MASPECT.AspectPlain()
        # Test
        target.add_aspect_value(p_name=NAME, p_aspect=aspect)
        assert target._aspects[NAME] is aspect
        assert set(target._names_aspects.items()) == target._aspects.keys()

    def test_check(self, fact_sample):
        """Confirm base fact check."""
        # Setup
        target = fact_sample()
        STATUS = MFACT.StatusOfFact.DEFINED
        target._status = STATUS
        VALUE = 'Something completely different.'
        target._value = VALUE
        target.add_aspect_value(
            p_name='Oops', p_aspect=MFACT.AspectValuePlain())
        assert 1 < len(target._aspects)
        target.set_fresh()
        # Test
        result = target.check()
        assert result is STATUS
        assert target.is_stale()
        for aspect in target._aspects.values():
            view = aspect.new_view()
            assert VALUE == view.get_text()
            view.destroy()

    def test_clear(self, fact_sample):
        """Confirm base fact clear."""
        # Setup
        target = fact_sample()
        STATUS = MFACT.StatusOfFact.UNDEFINED
        target._status = STATUS
        VALUE = 'Something completely different.'
        target._value = VALUE
        target.add_aspect_value(
            p_name='Oops', p_aspect=MFACT.AspectValuePlain())
        assert 1 < len(target._aspects)
        for aspect in target._aspects.values():
            aspect.set_presentation(p_subject=target._value)
        target.set_fresh()
        BLANK = ''
        # Test
        result = target.clear()
        assert result is STATUS
        assert target.is_stale()
        assert target._value is None
        for aspect in target._aspects.values():
            view = aspect.new_view()
            assert BLANK == view.get_text()
            view.destroy()

    def test_is_stale(self, fact_sample):
        """Confirm state test matches change mark.

        #. Case: Fact stale, identity fresh, note fresh
        #. Case: Fact fresh, identity stale, note fresh
        #. Case: Fact fresh, identity fresh, note stake
        #. Case: Fact fresh, identity fresh, note fresh
        """
        # Setup
        target = fact_sample()
        # Test: Fact stale, identity fresh, note fresh
        target.set_fresh()
        target._stale = True
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity stale, note fresh
        target.set_fresh()
        target._summary.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity fresh, note stale
        target.set_fresh()
        target.note.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Fact fresh, identity fresh, note fresh
        target.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_new_model(self, fact_sample):
        """Confirm store for identity components."""
        # Setup
        target = fact_sample()
        # Test
        name, summary, title = target._new_model()
        assert isinstance(name, MFACT.NameFact)
        assert isinstance(summary, MFACT.SummaryFact)
        assert isinstance(title, MFACT.TitleFact)

    @pytest.mark.name_aspect('Plain')
    def test_new_view_aspect(self, fact_sample_with_view_aspect):
        """| Confirm method returns aspect view.
        | Case: aspect found
        """
        # Setup
        fact, view = fact_sample_with_view_aspect
        fact._value = 'Something completely different'
        fact.check()
        # Test
        assert isinstance(view, BUI.ViewAny)
        assert fact.value == view.get_text()

    @pytest.mark.name_aspect('Oops!')
    def test_new_view_aspect_missing(self, fact_sample_with_view_aspect):
        """| Confirm method returns aspect view.
        | Case: aspect is missing
        """
        # Setup
        _, view = fact_sample_with_view_aspect
        WARNING = 'This fact does not support the aspect you requested'
        # Test
        assert isinstance(view, BUI.ViewAny)
        assert WARNING == view.get_text()

    @pytest.mark.name_method('new_view_names_aspects')
    def test_new_view_names_aspects(self, fact_sample_with_view):
        """Confirm returned view of aspect names."""
        # Setup
        fact, view = fact_sample_with_view
        names = [name for name in fact._names_aspects.lines()]
        # Test
        assert isinstance(view, MFACT.ViewNamesAspects)
        assert view.get_model() is not None
        assert len(names) == len(view.get_model())

    @pytest.mark.name_method('new_view_note')
    def test_new_view_note(self, fact_sample_with_view):
        """Confirm method returns note view."""
        # Setup
        fact, view = fact_sample_with_view
        fact.note.text = 'Something completely different'
        # Test
        assert isinstance(view, MFACT.ViewNoteFact)
        assert fact.note.text == view.get_text()

    @pytest.mark.name_method('new_view_status')
    def test_new_view_status(self, fact_sample_with_view):
        """Confirm method returns status view."""
        # Setup
        fact, view = fact_sample_with_view
        # Test
        assert isinstance(view, MFACT.ViewAspectStatus)
        assert fact.status.name == view.get_text()

    @pytest.mark.name_method('new_view_tag')
    def test_new_view_tag(self, fact_sample_with_view):
        """Confirm returned view of tag."""
        # Setup
        fact, view = fact_sample_with_view
        # Test
        assert isinstance(view, MFACT.ViewAspectTagFact)
        assert str(fact.tag) == view.get_text()

    def test_set_fresh(self, fact_sample):
        """| Confirm fact marked fresh.
        | Case: change mark on fact
        """
        # Setup
        target = fact_sample()
        target._stale = True
        target._note.set_stale()
        # Test
        target.set_fresh()
        assert not target._stale
        assert target._note.is_fresh()

    @pytest.mark.parametrize('ATTR', [
        '_name',
        '_note',
        '_summary',
        '_title',
        ])
    def test_set_fresh_attr(self, fact_sample, ATTR):
        """| Confirm fact marked fresh.
        | Case: change mark on each fact attribute
        """
        # Setup
        target = fact_sample()
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

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (MFACT.NameFact, BUI.ModelTextMarkup),
        (MFACT.SummaryFact, BUI.ModelGtkTextBuffer),
        (MFACT.TitleFact, BUI.ModelTextMarkup),
        (MFACT.ViewNameFact, BUI.ViewTextMarkup),
        (MFACT.ViewSummaryFact, BUI.ViewTextTagged),
        (MFACT.ViewTitleFact, BUI.ViewTextMarkup),
        (MFACT.NamesAspects, BUI.BridgeOutlineSelect[str]),
        (MFACT.ViewNamesAspects, BUI.ViewOutlineSelect),
        (MFACT.NoteFact, BUI.ModelTextMarkup),
        (MFACT.ViewNoteFact, BUI.ViewTextMarkup),
        (MFACT.AspectStatus, MASPECT.AspectPlain),
        (MFACT.ViewAspectStatus, MASPECT.ViewAspectPlain),
        (MFACT.TagFact.__supertype__, int),  # type: ignore[attr-defined]
        (MFACT.AspectTagFact, MASPECT.AspectPlain),
        (MFACT.ViewAspectTagFact, MASPECT.ViewAspectPlain),
        (type(MFACT.ValueOpaque), typing.TypeVar),
        (MFACT.ValueOpaque.__constraints__, ()),
        (MFACT.AspectValuePlain, MASPECT.AspectPlain),
        (type(MFACT.TopicOpaque), typing.TypeVar),
        (MFACT.TopicOpaque.__constraints__, ()),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
