"""
Unit tests for factsheet-level model.  See :mod:`~factsheet.model`.

.. include:: /test/refs_include_pytest.txt
"""
import pytest

import factsheet.bridge_ui as BUI
import factsheet.model.sheet as MSHEET
import factsheet.model.topic as MTOPIC


class TestModule:
    """Unit tests for module-level components of :mod:`.sheet`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (MSHEET.Name, BUI.x_b_t_ModelTextMarkup),
        (MSHEET.Summary, BUI.ModelTextStyled),
        (MSHEET.OutlineTopics.__dict__['__origin__'], BUI.ModelOutlineMulti),
        (MSHEET.OutlineTopics.__dict__['__args__'], (MTOPIC.Topic, )),
        (MSHEET.Title, BUI.x_b_t_ModelTextMarkup),
        (MSHEET.TagSheet.__qualname__, 'NewType.<locals>.new_type'),
        (MSHEET.TagSheet.__dict__['__supertype__'], int),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestSheet:
    """Unit tests for :class:`~.model.sheet.Sheet`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: identity difference
        #. Case: topic outline difference
        #. Case: Equivalence
        """
        # Setup
        TITLE_SOURCE = 'The Parrot Sketch'
        source = MSHEET.Sheet(p_title=TITLE_SOURCE)
        # Test: type difference
        assert not source.__eq__(TITLE_SOURCE)
        # Test: identity difference
        TITLE_TARGET = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_TARGET)
        assert not source.__eq__(target)
        # Test: topic outline difference
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        topic = MTOPIC.Topic(p_name='Killer Rabbit', p_summary='', p_title='')
        _index = target._topics.insert_child(topic, None)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, new_id_args):
        """| Confirm initialization.
        | Case: explicit arguments.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        # Test
        target = MSHEET.Sheet(**ID_ARGS)
        assert ID_ARGS['p_name'] == target.name.text
        assert ID_ARGS['p_summary'] == target.summary.text
        assert ID_ARGS['p_title'] == target.title.text
        assert isinstance(target._topics, BUI.ModelOutlineMulti)
        assert not list(target._topics.items())
        assert not target._stale

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        NAME_DEFAULT = 'Unnamed'
        SUMMARY_DEFAULT = 'Edit factsheet description here.'
        TITLE_DEFAULT = 'New Factsheet'
        # Test
        target = MSHEET.Sheet()
        assert NAME_DEFAULT == target.name.text
        assert SUMMARY_DEFAULT == target.summary.text
        assert TITLE_DEFAULT == target.title.text

    def test_clear(self, monkeypatch):
        """Confirm outline marked stale and method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        clear_called = False

        def clear(self):
            nonlocal clear_called
            clear_called = True  # pylint: disable=unused-variable

        monkeypatch.setattr(BUI.ModelOutlineMulti, 'clear', clear)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # Test
        target.clear()
        assert target.is_stale()
        assert clear_called

    def test_get_tag(self, new_id_args):
        """| Confirm tag is for topic at line.
        | Case: line contains topic.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            name = 'Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        I_TOPIC = 0
        parent = target._topics._ui_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            parent = target.insert_topic_child(topic, parent)
            if I_TOPIC == j:
                tag_topic = topic.tag
                line_topic = parent
        # Test
        result = target.get_tag(line_topic)
        assert tag_topic == result

    def test_get_tag_none(self, new_id_args):
        """| Confirm tag is for topic at line.
        | Case: line contains None.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        NO_TAG = 0
        line_none = target.insert_topic_before(None, None)
        # Test
        result = target.get_tag(line_none)
        assert NO_TAG == result

    @pytest.mark.parametrize('PATCH, METHOD', [
        ('insert_after', 'insert_topic_after'),
        ('insert_before', 'insert_topic_before'),
        ('insert_child', 'insert_topic_child'),
        ])
    def test_insert_topic(self, monkeypatch, PATCH, METHOD):
        """Confirm method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param PATCH: outline method to patch.
        :param METHOD: method under test.
        """
        # Setup
        class PatchInsert:
            def __init__(self):
                self.called = False
                self.topic = None
                self.line = 'Oops'

            def insert(self, p_topic, p_line):
                self.called = True
                self.topic = p_topic
                self.line = p_line

        patch_insert = PatchInsert()
        monkeypatch.setattr(
            BUI.ModelOutlineMulti, PATCH, patch_insert.insert)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        target.set_fresh()
        target_method = getattr(target, METHOD)
        TOPIC = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        # Test
        _ = target_method(TOPIC, None)
        assert patch_insert.called
        assert patch_insert.topic is TOPIC
        assert patch_insert.line is None
        assert target.is_stale()

    def test_is_fresh(self, new_id_args):
        """Confirm return is accurate.

        #. Case: Sheet stale, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info stale, topics fresh
        #. Case: Sheet fresh, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info fresh, topics stale

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            name = 'Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        parent = target._topics._ui_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            parent = target.insert_topic_child(topic, parent)
        for topic in target._topics.items():
            topic.set_fresh()
        I_MIDDLE = 1
        # Test: Sheet stale, ID info fresh, topics fresh
        target._stale = True
        target._summary.set_fresh()
        assert not target.has_not_changed()
        assert target._stale
        # Test: Sheet fresh, ID info stale, topics fresh
        target._stale = False
        target._summary.set_stale()
        assert not target.has_not_changed()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, topics fresh
        target._stale = False
        target._summary.set_fresh()
        assert target.has_not_changed()
        assert not target._stale
        # Test: Sheet fresh, ID info fresh, topics fresh
        target._stale = False
        target._summary.set_fresh()
        for i, topic in enumerate(target._topics.items()):
            if i == I_MIDDLE:
                topic.set_stale()
            else:
                topic.set_fresh()
        assert target.is_stale()
        assert target._stale

    def test_is_stale(self, new_id_args):
        """Confirm return is accurate.

        #. Case: Sheet stale, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info stale, topics fresh
        #. Case: Sheet fresh, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info fresh, leaf topic stale
        #. Case: Sheet fresh, ID info fresh, last topic stale

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            name = 'Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        parent = target._topics._ui_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            parent = target.insert_topic_child(topic, parent)
        I_LEAF = 2
        I_LAST = 4
        # Test: Sheet stale, ID info fresh
        target._stale = True
        target._name.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info stale
        target._stale = False
        target._name.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, topics fresh
        target._stale = False
        target._name.set_fresh()
        assert not target.is_stale()
        assert not target._stale
        # Test: Sheet fresh, ID info fresh, leaf topic stale
        target._stale = False
        target._name.set_fresh()
        for i, topic in enumerate(target._topics.items()):
            if i == I_LEAF:
                topic.set_stale()
            else:
                topic.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, last topic stale
        target._stale = False
        target._name.set_fresh()
        for i, topic in enumerate(target._topics.items()):
            if i == I_LAST:
                topic.set_stale()
            else:
                topic.set_fresh()
        assert target.is_stale()
        assert target._stale

    def test_is_stale_warn(self, new_id_args, caplog):
        """Confirm warning when topics outline contains line with None.

        :param new_id_args: fixture :func:`.new_id_args`.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        target._topics._ui_model.append(None, [None])
        N_LOGS = 1
        LAST = -1
        log_message = ('Topics outline contains line with no topic ('
                       'Sheet.is_stale)')
        # Test
        result = target.is_stale()
        assert not result
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('outline_topics', '_topics'),
        ])
    def test_property_access(self, new_id_args, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param new_id_args: fixture :func:`.new_id_args`.
        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        attr = getattr(target, NAME_ATTR)
        CLASS = MSHEET.Sheet
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_property_tag(self, new_id_args):
        """Confirm value and access limits of tag property.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        target_prop = getattr(MSHEET.Sheet, 'tag')
        # Test
        assert target_prop.fget is not None
        assert id(target) == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_remove_topic(self, monkeypatch):
        """Confirm outline marked stale and method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        remove_called = False
        remove_line = None

        def remove(self, p_line):
            nonlocal remove_called
            remove_called = True  # pylint: disable=unused-variable
            nonlocal remove_line
            remove_line = p_line  # pylint: disable=unused-variable

        monkeypatch.setattr(BUI.ModelOutlineMulti, 'remove', remove)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        target.set_fresh()
        LINE = BUI.LineOutline()
        # Test
        target.remove_topic(LINE)
        assert target.is_stale()
        assert remove_called
        assert remove_line is LINE

    def test_set_fresh(self, new_id_args):
        """Confirm all attributes marked fresh.

        #. Case: Sheet fresh, ID info fresh, topics fresh
        #. Case: Sheet stale, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info stale, topics fresh
        #. Case: Sheet stale, ID info stale, topics fresh
        #. Case: Sheet fresh, ID info fresh, topics stale
        #. Case: Sheet stale, ID info fresh, topics stale

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            name = 'Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        parent = target._topics._ui_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            parent = target.insert_topic_child(topic, parent)
        # Test: Sheet fresh, ID info fresh
        target._stale = False
        target._title.set_fresh()
        for topic in target._topics.items():
            topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        # Test: Sheet stale, ID info fresh, topics fresh
        target._stale = True
        target._title.set_fresh()
        for topic in target._topics.items():
            topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        # Test: Sheet fresh, ID info stale, topics fresh
        target._stale = False
        target._title.set_stale()
        for topic in target._topics.items():
            topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        # Test: Sheet stale, ID info stale, topics fresh
        target._stale = True
        target._title.set_stale()
        for topic in target._topics.items():
            topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        # Test: Sheet fresh, ID infor fresh, topics stale
        target._stale = False
        target._title.set_stale()
        for i, topic in enumerate(target._topics.items()):
            if i % 2:
                topic.set_stale()
            else:
                topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        for topic in target._topics.items():
            assert topic.has_not_changed()
        # Test: Sheet stale, ID info fresh, topics stale
        target._stale = True
        target._title.set_stale()
        for i, topic in enumerate(target._topics.items()):
            if not i % 2:
                topic.set_stale()
            else:
                topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.has_not_changed()
        for topic in target._topics.items():
            assert topic.has_not_changed()

    def test_set_fresh_warn(self, new_id_args, caplog):
        """Confirm warning when topics outline contains line with None.

        :param new_id_args: fixture :func:`.new_id_args`.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        target._topics._ui_model.append(None, [None])
        N_LOGS = 1
        LAST = -1
        log_message = ('Topics outline contains line with no topic ('
                       'Sheet.set_fresh)')
        # Test
        target.set_fresh()
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_topics(self, new_id_args):
        """Confirm iterations over topics."""
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        N_TOPICS = 5
        TOPICS = list()
        for i in range(N_TOPICS):
            name = 'Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title='')
            TOPICS.append(topic)
        I_TAIL = 2
        parent = None
        line_tail = None
        for i, topic in enumerate(TOPICS):
            parent = target.insert_topic_child(topic, parent)
            if I_TAIL == i:
                line_tail = parent
        line_last = parent
        # Test
        assert TOPICS == list(target.topics())
        assert TOPICS[2:] == list(target.topics(line_tail))
        assert TOPICS[4:] == list(target.topics(line_last))

    def test_topics_warn(self, new_id_args, caplog):
        """Confirm warning when topics outline contains line with None.

        :param new_id_args: fixture :func:`.new_id_args`.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        target._topics._ui_model.append(None, [None])
        N_LOGS = 1
        LAST = -1
        log_message = ('Topics outline contains line with no topic ('
                       'Sheet.topics)')
        # Test
        with pytest.raises(StopIteration):
            _ = next(target.topics())
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
