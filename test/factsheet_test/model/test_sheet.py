"""
Unit tests for factsheet-level model.  See :mod:`~factsheet.model`.

.. include:: /test/refs_include_pytest.txt
"""
# import logging
# from pathlib import Path
# import pickle
import pytest   # type: ignore[import]
# import re

import factsheet.bridge_ui as BUI
import factsheet.model.sheet as MSHEET
# from factsheet.model import topic as MTOPIC
#
#
# @pytest.fixture
# def new_id_args():
#     """Pytest fixture: factory for stock identity arguments for
#     :class:`.Sheet`.
#     """
#     def new_args():
#         id_args = dict(
#             p_name='Parrot',
#             p_summary='The parrot is a Norwegian Blue.',
#             p_title='The Parrot Sketch',
#             )
#         return id_args
#
#     return new_args


class TestSheet:
    """Unit tests for :class:`~.model.sheet.Sheet`."""

    @pytest.mark.skip(reason='Topic outline check is incomplete.')
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
        # # Test: topic outline difference
        # target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        # topic = MTOPIC.Topic()
        # topic.init_identity(p_name='Killer Rabbit')
        # _index = target._topics.insert_child(topic, None)
        #
        # assert not source.__eq__(target)
        # Test: Equivalence
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, new_id_args):
        """| Confirm initialization.
        | Case: nominal.

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        # Test
        target = MSHEET.Sheet(**ID_ARGS)
        assert ID_ARGS['p_name'] == target.name.text
        assert ID_ARGS['p_summary'] == target.summary.text
        assert ID_ARGS['p_title'] == target.title.text
        # assert isinstance(target._topics, ABC_OUTLINE.AbstractOutline)
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

    # @pytest.mark.skip(reason='Method marked for deletion')
    # def test_attach_view_topics(self):
    #     """Confirm topics outline view addition."""
    #     # # Setup
    #     # TITLE_MODEL = 'Something completely different.'
    #     # target = MSHEET.Sheet(p_title=TITLE_MODEL)
    #     # VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     # # Test
    #     # target.attach_view_topics(VIEW_TOPICS)
    #     # assert target._topics._gtk_model is VIEW_TOPICS.gtk_view.get_model()

    @pytest.mark.skip
    def test_clear(self, monkeypatch):
        """| Confirm topics outline removal.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # class PatchClear:
        #     def __init__(self): self.called = False
        #
        #     def clear(self): self.called = True
        #
        # patch_outline = PatchClear()
        # monkeypatch.setattr(
        #     ASHEET.AdaptTreeStoreTopic, 'clear', patch_outline.clear)
        #
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     target.attach_page(page)
        #
        # N_TOPICS = 5
        # topics = [MTOPIC.Topic() for _ in range(N_TOPICS)]
        # parent = None
        # for topic in topics:
        #     parent = target.insert_topic_child(topic, parent)
        #
        # N_REMOVE = 5
        # ids_extracted = [t.tag for t in topics]
        # target.set_fresh()
        # # Test
        # target.clear()
        # assert target.is_stale()
        # for page in pages:
        #     assert page.called_close_topic == N_REMOVE
        #     assert ids_extracted == page.closed_topics
        # assert patch_outline.called

    # @pytest.mark.skip(reason='Method marked for deletion')
    # def test_detach_view_topics(self):
    #     """Confirm topics outline view removal."""
    #     # # Setup
    #     # TITLE_MODEL = 'Something completely different.'
    #     # target = MSHEET.Sheet(p_title=TITLE_MODEL)
    #     # VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
    #     # target.attach_view_topics(VIEW_TOPICS)
    #     # # Test
    #     # target.detach_view_topics(VIEW_TOPICS)
    #     # assert VIEW_TOPICS.gtk_view.get_model() is None

    @pytest.mark.skip
    def test_extract_topic(self, monkeypatch):
        """| Confirm method request relay to outline.
        | Case: relay index.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # class PatchExtract:
        #     def __init__(self): self.called = False
        #
        #     def extract_section(self, _index): self.called = True
        #
        # patch_outline = PatchExtract()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic, 'extract_section',
        #                     patch_outline.extract_section)
        #
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     target.attach_page(page)
        #
        # N_TOPICS = 5
        # topics = [MTOPIC.Topic() for _ in range(N_TOPICS)]
        # parent = None
        # for topic in topics:
        #     parent = target.insert_topic_child(topic, parent)
        #
        # N_REMOVE = 2
        # N_START = 3
        # gtk_model = target._topics._gtk_model
        # i_start = gtk_model.get_iter_first()
        # for _ in range(N_START):
        #     i_start = gtk_model.iter_children(i_start)
        # ids_extracted = [t.tag for t in topics[N_START:]]
        # target.set_fresh()
        # # Test
        # target.extract_topic(i_start)
        # assert target.is_stale()
        # for page in pages:
        #     assert page.called_close_topic == N_REMOVE
        #     assert ids_extracted == page.closed_topics
        # assert patch_outline.called

    @pytest.mark.skip
    def test_extract_topic_none(self, monkeypatch):
        """| Confirm method request relay to outline.
        | Case: drop None.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # class PatchExtract:
        #     def __init__(self): self.called = False
        #
        #     def extract_section(self, _index): self.called = True
        #
        # patch_outline = PatchExtract()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic, 'extract_section',
        #                     patch_outline.extract_section)
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # # Test
        # _ = target.extract_topic(None)
        # assert not patch_outline.called
        # assert target.is_fresh()

    @pytest.mark.skip
    def test_insert_topic_after(self, monkeypatch):
        """Confirm method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        # class PatchInsertAfter:
        #     def __init__(self): self.called = False
        #
        #     def insert_after(self, _item, _index): self.called = True
        #
        # patch_outline = PatchInsertAfter()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
        #                     'insert_after', patch_outline.insert_after)
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # target.set_fresh()
        # # Test
        # _ = target.insert_topic_after(None, None)
        # assert patch_outline.called
        # assert target.is_stale()

    @pytest.mark.skip
    def test_insert_topic_before(self, monkeypatch):
        """Confirm method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # class PatchInsertBefore:
        #     def __init__(self): self.called = False
        #
        #     def insert_before(self, _item, _index): self.called = True
        #
        # patch_outline = PatchInsertBefore()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
        #                     'insert_before', patch_outline.insert_before)
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # target.set_fresh()
        # # Test
        # _ = target.insert_topic_before(None, None)
        # assert patch_outline.called
        # assert target.is_stale()

    @pytest.mark.skip
    def test_insert_topic_child(self, monkeypatch):
        """Confirm method passes request to outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        # class PatchInsertChild:
        #     def __init__(self): self.called = False
        #
        #     def insert_child(self, _item, _index): self.called = True
        #
        # patch_outline = PatchInsertChild()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
        #                     'insert_child', patch_outline.insert_child)
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # target.set_fresh()
        # # Test
        # _ = target.insert_topic_child(None, None)
        # assert patch_outline.called
        # assert target.is_stale()

    def test_is_fresh(self, new_id_args):
        """Confirm return is accurate.

        #. Case: Sheet stale, ID info fresh
        #. Case: Sheet fresh, ID info stale
        #. Case: Sheet fresh, ID info fresh

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        # Test: Sheet stale, ID info fresh, no topics
        target._stale = True
        target._summary.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: Sheet fresh, ID info stale, no topics
        target._stale = False
        target._summary.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, no topics
        target._stale = False
        target._summary.set_fresh()
        assert target.is_fresh()
        assert not target._stale

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

        # N_TOPICS = 3
        # for i in range(N_TOPICS):
        #     topic = MTOPIC.Topic()
        #     topic.init_identity(p_name='Topic {}'.format(i))
        #     target.insert_topic_before(topic, None)
        # N_DESCEND = 2
        # parent = target._topics._gtk_model.get_iter_first()
        # for j in range(N_DESCEND):
        #     name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
        #     topic = MTOPIC.Topic()
        #     topic.init_identity(p_name=name)
        #     parent = target.insert_topic_child(topic, parent)
        # I_LEAF = 2
        # I_LAST = 4
        # # Test: Sheet stale, ID info fresh
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
        # # Test: Sheet fresh, ID info fresh, leaf topic stale
        # target._stale = False
        # target._infoid.set_fresh()
        # for i, index in enumerate(target._topics.indices()):
        #     topic = target._topics.get_item(index)
        #     if i == I_LEAF:
        #         topic.set_stale()
        #     else:
        #         topic.set_fresh()
        # assert target.is_stale()
        # assert target._stale
        # # Test: Sheet fresh, ID info fresh, last topic stale
        # target._stale = False
        # target._infoid.set_fresh()
        # for i, index in enumerate(target._topics.indices()):
        #     topic = target._topics.get_item(index)
        #     if i == I_LAST:
        #         topic.set_stale()
        #     else:
        #         topic.set_fresh()
        # assert target.is_stale()
        # assert target._stale

    # def test_new_model(self, new_id_args):
    #     """Confirm store for identity components.
    #
    #     :param new_id_args: fixture: factory for stock identity
    #         keyword arguments.
    #     """
    #     # Setup
    #     ID_ARGS = new_id_args()
    #     target = MSHEET.Sheet(**ID_ARGS)
    #     # Test
    #     name, summary, title = target._new_model()
    #     assert isinstance(name, MSHEET.NameSheet)
    #     assert isinstance(summary, MSHEET.SummarySheet)
    #     assert isinstance(title, MSHEET.TitleSheet)

    def test_set_fresh(self, new_id_args):
        """Confirm all attributes marked fresh.

        #. Case: Sheet fresh, ID info fresh
        #. Case: Sheet stale, ID info fresh
        #. Case: Sheet fresh, ID info stale
        #. Case: Sheet stale, ID info stale
        #. Case: Sheet fresh, topics stale
        #. Case: Sheet stale, topics stale

        :param new_id_args: fixture :func:`.new_id_args`.
        """
        # Setup
        ID_ARGS = new_id_args()
        target = MSHEET.Sheet(**ID_ARGS)
        # TEXT_TITLE = 'Something completely different'
        # target = MSHEET.Sheet(p_title=TEXT_TITLE)

        # N_TOPICS = 3
        # for i in range(N_TOPICS):
        #     topic = MTOPIC.Topic()
        #     topic.init_identity(p_name='Topic {}'.format(i))
        #     target.insert_topic_before(topic, None)
        # N_DESCEND = 2
        # parent = target._topics._gtk_model.get_iter_first()
        # for j in range(N_DESCEND):
        #     name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
        #     topic = MTOPIC.Topic()
        #     topic.init_identity(p_name=name)
        #     parent = target.insert_topic_child(topic, parent)
        # Test: Sheet fresh, ID info fresh
        target._stale = False
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet stale, ID info fresh
        target._stale = True
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet fresh, ID info stale
        target._stale = False
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet stale, ID info stale
        target._stale = True
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # # Test: Sheet fresh, topics stale
        # target._stale = False
        # target._infoid.set_stale()
        # for i, index in enumerate(target._topics.indices()):
        #     topic = target._topics.get_item(index)
        #     if i % 2:
        #         topic.set_stale()
        #     else:
        #         topic.set_fresh()
        # target.set_fresh()
        # assert not target._stale
        # assert target._infoid.is_fresh()
        # for index in target._topics.indices():
        #     topic = target._topics.get_item(index)
        #     assert topic.is_fresh()
        # # Test: Sheet stale, topics stale
        # target._stale = True
        # target._infoid.set_stale()
        # for i, index in enumerate(target._topics.indices()):
        #     topic = target._topics.get_item(index)
        #     if not i % 2:
        #         topic.set_stale()
        #     else:
        #         topic.set_fresh()
        # target.set_fresh()
        # assert not target._stale
        # assert target._infoid.is_fresh()
        # for index in target._topics.indices():
        #     topic = target._topics.get_item(index)
        #     assert topic.is_fresh()

    # @pytest.mark.skip(reason='No need to extend inherited method')
    # def test_set_stale(self):
    #     """Confirm all attributes set.
    #
    #     #. Case: Sheet fresh, ID info fresh, no topics.
    #     #. Case: Sheet stale, ID info fresh, no topics.
    #     #. Case: Sheet fresh, ID info stale, no topics.
    #     #. Case: Sheet stale, ID info stale, no topics.
    #     #. Case: Sheet fresh, ID info fresh, topics fresh
    #      """
    #     # # Setup
    #     # TEXT_TITLE = 'Something completely different'
    #     # target = MSHEET.Sheet(p_title=TEXT_TITLE)
    #     #
    #     # N_TOPICS = 3
    #     # for i in range(N_TOPICS):
    #     #     topic = MTOPIC.Topic()
    #     #     topic.init_identity(p_name='Topic {}'.format(i))
    #     #     target.insert_topic_before(topic, None)
    #     # N_DESCEND = 2
    #     # parent = target._topics._gtk_model.get_iter_first()
    #     # for j in range(N_DESCEND):
    #     #     name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
    #     #     topic = MTOPIC.Topic()
    #     #     topic.init_identity(p_name=name)
    #     #     parent = target.insert_topic_child(topic, parent)
    #     # # Test: Sheet fresh, ID info fresh, no topics.
    #     # target._stale = False
    #     # target._infoid.set_fresh()
    #     # target.set_stale()
    #     # assert target._stale
    #     # assert target._infoid.is_fresh()
    #     # # Test: Sheet stale, ID info fresh, no topics.
    #     # target._stale = True
    #     # target._infoid.set_fresh()
    #     # target.set_stale()
    #     # assert target._stale
    #     # assert target._infoid.is_fresh()
    #     # # Test: Sheet fresh, ID info stale, no topics.
    #     # target._stale = False
    #     # target._infoid.set_stale()
    #     # target.set_stale()
    #     # assert target._stale
    #     # assert target._infoid.is_stale()
    #     # # Test: Sheet stale, ID info stale, no topics.
    #     # target._stale = True
    #     # target._infoid.set_stale()
    #     # target.set_stale()
    #     # assert target._stale
    #     # assert target._infoid.is_stale()
    #     # # Test: Sheet fresh, ID info fresh, topics fresh.
    #     # target._stale = False
    #     # target._infoid.set_fresh()
    #     # for index in target._topics.indices():
    #     #     topic = target._topics.get_item(index)
    #     #     topic.set_fresh()
    #     # target.set_stale()
    #     # assert target._stale
    #     # assert target._infoid.is_fresh()
    #     # for index in target._topics.indices():
    #     #     topic = target._topics.get_item(index)
    #     #     assert topic.is_fresh()

    @pytest.mark.skip
    def test_topics(self):
        """Confirm iterations over topics."""
        # # Setup
        # TEXT_TITLE = 'Something completely different'
        # target = MSHEET.Sheet(p_title=TEXT_TITLE)
        # N_TOPICS = 3
        # TOPICS = list()
        # for i in range(N_TOPICS):
        #     topic = MTOPIC.Topic()
        #     topic.init_identity(p_name='Topic {}'.format(i))
        # parent = None
        # for topic in TOPICS:
        #     parent = target.insert_topic_child(topic, parent)
        # # Test
        # assert TOPICS == list(target.topics())
        # assert TOPICS[2:] == list(target.topics(parent))


class TestSheetTypes:
    """Unit tests for type hint definitions in :mod:`.sheet`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (MSHEET.Name, BUI.ModelTextMarkup),
        (MSHEET.DisplayName, BUI.DisplayTextMarkup),
        (MSHEET.FactoryDisplayName, BUI.FactoryDisplayTextMarkup),
        (MSHEET.EditorName, BUI.EditorTextMarkup),
        (MSHEET.FactoryEditorName, BUI.FactoryEditorTextMarkup),
        (MSHEET.Summary, BUI.ModelTextStyled),
        (MSHEET.DisplaySummary, BUI.DisplayTextStyled),
        (MSHEET.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (MSHEET.EditorSummary, BUI.EditorTextStyled),
        (MSHEET.FactoryEditorSummary, BUI.FactoryEditorTextStyled),
        (MSHEET.Title, BUI.ModelTextMarkup),
        (MSHEET.DisplayTitle, BUI.DisplayTextMarkup),
        (MSHEET.FactoryDisplayTitle, BUI.FactoryDisplayTextMarkup),
        (MSHEET.EditorTitle, BUI.EditorTextMarkup),
        (MSHEET.FactoryEditorTitle, BUI.FactoryEditorTextMarkup),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
