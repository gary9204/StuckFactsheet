"""
Unit tests for class that mediates topic-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_topic`.
"""
import pytest  # type: ignore[import]
# import typing

# import factsheet.bridge_ui as BUI
import factsheet.control.control_topic as CTOPIC
import factsheet.model.topic as MTOPIC


class TestControlTopic:
    """Unit tests for :class:`~.control_topic.ControlTopic`."""

    def test_init(self, new_model_topic):
        """Confirm initialization.

        :param new_model_topic: fixture :func:`.new_model_topic`.
        """
        # Setup
        N_FACTS = 5
        MODEL = new_model_topic(N_FACTS)
        # facts = list(TOPIC.facts())
        # Test
        target = CTOPIC.ControlTopic(p_model=MODEL)
        assert target._model is MODEL
        model_name = target._model.name
        factory_display_name = target._factory_display_name
        assert isinstance(factory_display_name, MTOPIC.FactoryDisplayName)
        assert factory_display_name._ui_model is model_name._ui_model
        factory_editor_name = target._factory_editor_name
        assert isinstance(factory_editor_name, MTOPIC.FactoryEditorName)
        assert factory_editor_name._ui_model is model_name._ui_model

        model_summary = target._model.summary
        factory_display_summary = target._factory_display_summary
        assert isinstance(
            factory_display_summary, MTOPIC.FactoryDisplaySummary)
        assert factory_display_summary._ui_model is model_summary._ui_model
        factory_editor_summary = target._factory_editor_summary
        assert isinstance(factory_editor_summary, MTOPIC.FactoryEditorSummary)
        assert factory_editor_summary._ui_model is model_summary._ui_model

        model_title = target._model.title
        factory_display_title = target._factory_display_title
        assert isinstance(factory_display_title, MTOPIC.FactoryDisplayTitle)
        assert factory_display_title._ui_model is model_title._ui_model
        factory_editor_title = target._factory_editor_title
        assert isinstance(factory_editor_title, MTOPIC.FactoryEditorTitle)
        assert factory_editor_title._ui_model is model_title._ui_model

        # assert isinstance(target._controls_fact, dict)
        # assert len(facts) == len(target._controls_fact)
        # for fact in facts:
        #     assert target._controls_fact[fact.tag]._fact is fact

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_factory_display_name', 'new_display_name'),
        ('_factory_editor_name', 'new_editor_name'),
        ('_factory_display_summary', 'new_display_summary'),
        ('_factory_editor_summary', 'new_editor_summary'),
        ('_factory_display_title', 'new_display_title'),
        ('_factory_editor_title', 'new_editor_title'),
        ])
    def test_property(self, new_model_topic, NAME_ATTR, NAME_PROP):
        """Confirm model property is get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete

        :param new_model_topic: fixture :func:`.new_model_topic`.
        :param NAME_ATTR: name of attribute.
        :param NAME_PROP: name of property.
        """
        # Setup
        N_FACTS = 5
        MODEL = new_model_topic(N_FACTS)
        target = CTOPIC.ControlTopic(p_model=MODEL)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(CTOPIC.ControlTopic, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: get
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no set
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    # @pytest.mark.parametrize('NAME, ESCAPED', [
    #     ('<b>Parrot</b> Sketch', '<b>Parrot</b> Sketch'),
    #     ('<b>Parrot<b Sketch', '&lt;b&gt;Parrot&lt;b Sketch'),
    #     ])
    # def test_property_name(self, new_model_topic, NAME, ESCAPED):
    #     """| Confirm model name property is get-only without markup errors.
    #     | Case: name does not contain markup errors
    #
    #     #. Case: get
    #     #. Case: no set
    #     #. Case: no delete
    #
    #     :param new_model_topic: fixture :func:`.new_model_topic`.
    #     :param NAME: name of factsheet.
    #     :param ESCAPED: name of factsheet with markup errors escaped.
    #     """
    #     # Setup
    #     N_FACTS = 5
    #     MODEL = new_model_topic(N_FACTS)
    #     target = CTOPIC.ControlTopic(p_model=MODEL)
    #     target_prop = getattr(CTOPIC.ControlTopic, 'name')
    #     model_name = target._model.name
    #     model_name._set_persist(NAME)
    #     # Test: get
    #     assert target_prop.fget is not None
    #     assert ESCAPED == target.name
    #     # Test: no set
    #     assert target_prop.fset is None
    #     # Test: no delete
    #     assert target_prop.fdel is None

    # @pytest.mark.parametrize('NAME_ATTR, NAME_PROP, HAS_SETTER', [
    #     ('_topic', 'topic', False),
    #     ('_topic', 'idcore', False),
    #     ])
    # def test_property(self, NAME_ATTR, NAME_PROP, HAS_SETTER):
    #     """Confirm values and access limits of properties."""
    #     # Setup
    #     TOPIC = MTOPIC.Topic()
    #     target = CTOPIC.ControlTopic(p_topic=TOPIC)
    #     target_prop = getattr(CTOPIC.ControlTopic, NAME_PROP)
    #     value_attr = getattr(target, NAME_ATTR)
    #     REPLACE = MTOPIC.Topic()
    #     # Test
    #     assert target_prop.fget is not None
    #     assert value_attr is target_prop.fget(target)
    #     if HAS_SETTER:
    #         target_prop.fset(target, REPLACE)
    #         value_attr = getattr(target, NAME_ATTR)
    #         assert value_attr is REPLACE
    #     else:
    #         assert target_prop.fset is None
    #     assert target_prop.fdel is None


class TestTypes:
    """Unit tests for type definitions in :mod:`.control_topic`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        # (CTOPIC.ViewNameTopic, BUI.ViewTextMarkup),
        # (CTOPIC.ViewSummaryTopic, BUI.ViewTextTagged),
        # (CTOPIC.ViewTitleTopic, BUI.ViewTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
