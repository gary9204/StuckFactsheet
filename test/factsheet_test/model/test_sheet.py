"""
Unit tests for factsheet-level model.  See :mod:`~factsheet.model`.
"""
# import logging
# from pathlib import Path
# import pickle
import pytest   # type: ignore[import]
# import re

# from factsheet.abc_types import abc_outline as ABC_OUTLINE
# from factsheet.adapt_gtk import adapt_sheet as ASHEET
# from factsheet.model import infoid as MINFOID
import factsheet.model.sheet as MSHEET
# from factsheet.model import topic as MTOPIC


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

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_get_set_state(self, tmp_path, interface_page_sheet):
        """Confirm conversion to and from pickle format."""
        # # Setup
        # path = Path(str(tmp_path / 'get_set.fsg'))
        #
        # TITLE_MODEL = 'Something completely different.'
        # source = MSHEET.Sheet(p_title=TITLE_MODEL)
        # source._stale = True
        #
        # topic = MTOPIC.Topic()
        # topic.init_identity(p_name='Killer Rabbit')
        # _index = source._topics.insert_child(topic, None)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     source.attach_page(page)
        # # Test
        # with path.open(mode='wb') as io_out:
        #     pickle.dump(source, io_out)
        #
        # with path.open(mode='rb') as io_in:
        #     target = pickle.load(io_in)
        #
        # assert source._infoid == target._infoid
        # assert source._topics == target._topics
        # assert not target._stale
        # assert isinstance(target._pages, dict)
        # assert not target._pages

    def test_init(self, new_kwargs_idcore):
        """Confirm initialization.

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        # Test
        target = MSHEET.Sheet(**KWARGS)
        assert KWARGS['p_name'] == target.name
        assert KWARGS['p_summary'] == target.summary
        assert KWARGS['p_title'] == target.title
        # assert isinstance(target._topics, ABC_OUTLINE.AbstractOutline)
        assert not target._stale

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = 'Unnamed'
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = MSHEET.Sheet()
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_attach_page(self, interface_page_sheet):
        """Confirm page addition.
        Case: page not attached initially
        """
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # assert pages[0].get_infoid().title != target._infoid.title
        # # Test
        # for page in pages:
        #     target.attach_page(page)
        #     assert target._infoid.title == page.get_infoid().title
        #     assert target._topics._gtk_model is (
        #         page._topics.gtk_view.get_model())
        #     assert target._pages[id(page)] is page
        # assert len(pages) == len(target._pages)

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_attach_page_warn(
            self, interface_page_sheet, PatchLogger, monkeypatch):
        """Confirm page addition.
        Case: page attached initially
        """
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # assert pages[0].get_infoid().title != target._infoid.title
        # for page in pages:
        #     target.attach_page(page)
        # assert N_PAGES == len(target._pages)
        # I_DUPLIDATE = 1
        # page_dup = pages[I_DUPLIDATE]
        #
        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = (
        #     'Duplicate page: {} (Sheet.attach_page)'
        #     ''.format(hex(id(page_dup))))
        # # Test
        # target.attach_page(page_dup)
        # assert len(pages) == len(target._pages)
        # assert patch_logger.called
        # assert PatchLogger.T_WARNING == patch_logger.level
        # assert log_message == patch_logger.message

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_attach_view_topics(self):
        """Confirm topics outline view addition."""
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        # # Test
        # target.attach_view_topics(VIEW_TOPICS)
        # assert target._topics._gtk_model is VIEW_TOPICS.gtk_view.get_model()

    @pytest.mark.skip
    def test_clear(self, monkeypatch, interface_page_sheet):
        """| Confirm topics outline removal."""
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

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_detach_all(self, monkeypatch, interface_page_sheet):
        """Confirm notifications and removals."""
        # # Setup
        # class PatchInfoIdModel:
        #     def __init__(self): self.n_calls = 0
        #
        #     def detach_view(self, _v): self.n_calls += 1
        #
        # patch_detach = PatchInfoIdModel()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_detach.detach_view)
        #
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     target.attach_page(page)
        # assert N_PAGES == len(target._pages)
        # # Test
        # target.detach_all()
        # assert not target._pages
        # assert N_PAGES == patch_detach.n_calls
        # for page in pages:
        #     assert page.called_close_page

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_detach_attribute_views(
            self, monkeypatch, interface_page_sheet):
        """Confirm removal of views."""
        # # Setup
        # class PatchInfoIdDetach:
        #     def __init__(self): self.called = False
        #
        #     def detach_view(self, _v): self.called = True
        #
        # patch_infoid = PatchInfoIdDetach()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)
        #
        # class PatchTopicsDetach:
        #     def __init__(self): self.called = False
        #
        #     def detach_view(self, _v): self.called = True
        #
        # patch_topics = PatchTopicsDetach()
        # monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic, 'detach_view',
        #                     patch_topics.detach_view)
        #
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # page = interface_page_sheet()
        # target.attach_page(page)
        # # Test
        # target._detach_attribute_views(page)
        # assert patch_infoid.called
        # assert patch_topics.called

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_detach_page(self, monkeypatch, interface_page_sheet):
        """Confirm page removal.
        Case: page attached initially
        """
        # # Setup
        # class PatchInfoIdModel:
        #     def __init__(self): self.n_calls = 0
        #
        #     def detach_view(self, _v): self.n_calls += 1
        #
        # patch_infoid = PatchInfoIdModel()
        # monkeypatch.setattr(
        #     MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)
        #
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     target.attach_page(page)
        # N_REMOVE = 1
        # I_REMOVE = 1
        # page_rem = pages.pop(I_REMOVE)
        # # Test
        # target.detach_page(page_rem)
        # assert N_REMOVE == patch_infoid.n_calls
        # assert len(pages) == len(target._pages)
        # for page in pages:
        #     assert target._pages[id(page)] is page

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_detach_page_warn(
            self, interface_page_sheet, PatchLogger, monkeypatch):
        """Confirm page removal.
        Case: page not attached initially
        """
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # assert pages[0].get_infoid().title != target._infoid.title
        # for page in pages:
        #     target.attach_page(page)
        # I_DUPLICATE = 1
        # page_dup = pages.pop(I_DUPLICATE)
        # target.detach_page(page_dup)
        # assert len(pages) == len(target._pages)
        #
        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = (
        #     'Missing page: {} (Sheet.detach_page)'
        #     ''.format(hex(id(page_dup))))
        # # Test
        # target.detach_page(page_dup)
        # assert len(pages) == len(target._pages)
        # assert patch_logger.called
        # assert PatchLogger.T_WARNING == patch_logger.level
        # assert log_message == patch_logger.message

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_detach_view_topics(self):
        """Confirm topics outline view removal."""
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # VIEW_TOPICS = ASHEET.AdaptTreeViewTopic()
        # target.attach_view_topics(VIEW_TOPICS)
        # # Test
        # target.detach_view_topics(VIEW_TOPICS)
        # assert VIEW_TOPICS.gtk_view.get_model() is None

    @pytest.mark.skip
    def test_extract_topic(self, monkeypatch, interface_page_sheet):
        """| Confirm method request relay to outline.
        | Case: relay index.
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
        """Confirm method passes request to outline."""
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
        """Confirm method passes request to outline."""
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
        """Confirm method passes request to outline."""
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

    def test_is_fresh(self, new_kwargs_idcore):
        """Confirm return is accurate.

        #. Case: Sheet stale, ID info fresh
        #. Case: Sheet fresh, ID info stale
        #. Case: Sheet fresh, ID info fresh

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        target = MSHEET.Sheet(**KWARGS)
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

    def test_is_stale(self, new_kwargs_idcore):
        """Confirm return is accurate.

        #. Case: Sheet stale, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info stale, topics fresh
        #. Case: Sheet fresh, ID info fresh, topics fresh
        #. Case: Sheet fresh, ID info fresh, leaf topic stale
        #. Case: Sheet fresh, ID info fresh, last topic stale

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        target = MSHEET.Sheet(**KWARGS)

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

    def test_new_model(self, new_kwargs_idcore):
        """Confirm store for identity components.

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        target = MSHEET.Sheet(**KWARGS)
        # Test
        name, summary, title = target._new_model()
        assert isinstance(name, MSHEET.NameSheet)
        assert isinstance(summary, MSHEET.SummarySheet)
        assert isinstance(title, MSHEET.TitleSheet)

    @pytest.mark.skip(reason='Method marked for deletion')
    def test_n_pages(self, interface_page_sheet):
        """Confrim reported number of pages."""
        # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # assert pages[0].get_infoid().title != target._infoid.title
        # # Test
        # for i, page in enumerate(pages):
        #     assert i == target.n_pages()
        #     target.attach_page(page)
        # assert N_PAGES == target.n_pages()

    @pytest.mark.skip
    def test_present_pages(self, interface_page_sheet):
        """Confirm all pages get present notice."""
        # # Setup
        # TITLE_MODEL = 'Something completely different.'
        # target = MSHEET.Sheet(p_title=TITLE_MODEL)
        #
        # N_PAGES = 3
        # pages = [interface_page_sheet() for _ in range(N_PAGES)]
        # for page in pages:
        #     target.attach_page(page)
        # NO_TIME = 0
        # # Test
        # target.present_pages(NO_TIME)
        # for page in pages:
        #     assert page.called_present

    def test_set_fresh(self, new_kwargs_idcore):
        """Confirm all attributes marked fresh.

        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet stale, identification information stale
        #. Case: Sheet fresh, topics stale
        #. Case: Sheet stale, topics stale

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        target = MSHEET.Sheet(**KWARGS)
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
        # Test: Sheet fresh, identification information fresh
        target._stale = False
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet stale, identification information fresh
        target._stale = True
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet fresh, identification information stale
        target._stale = False
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: Sheet stale, identification information stale
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

    @pytest.mark.skip(reason='No need to extend inherited method')
    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Sheet fresh, ID info fresh, no topics.
        #. Case: Sheet stale, ID info fresh, no topics.
        #. Case: Sheet fresh, ID info stale, no topics.
        #. Case: Sheet stale, ID info stale, no topics.
        #. Case: Sheet fresh, ID info fresh, topics fresh
         """
        # # Setup
        # TEXT_TITLE = 'Something completely different'
        # target = MSHEET.Sheet(p_title=TEXT_TITLE)
        #
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
        # # Test: Sheet fresh, ID info fresh, no topics.
        # target._stale = False
        # target._infoid.set_fresh()
        # target.set_stale()
        # assert target._stale
        # assert target._infoid.is_fresh()
        # # Test: Sheet stale, ID info fresh, no topics.
        # target._stale = True
        # target._infoid.set_fresh()
        # target.set_stale()
        # assert target._stale
        # assert target._infoid.is_fresh()
        # # Test: Sheet fresh, ID info stale, no topics.
        # target._stale = False
        # target._infoid.set_stale()
        # target.set_stale()
        # assert target._stale
        # assert target._infoid.is_stale()
        # # Test: Sheet stale, ID info stale, no topics.
        # target._stale = True
        # target._infoid.set_stale()
        # target.set_stale()
        # assert target._stale
        # assert target._infoid.is_stale()
        # # Test: Sheet fresh, ID info fresh, topics fresh.
        # target._stale = False
        # target._infoid.set_fresh()
        # for index in target._topics.indices():
        #     topic = target._topics.get_item(index)
        #     topic.set_fresh()
        # target.set_stale()
        # assert target._stale
        # assert target._infoid.is_fresh()
        # for index in target._topics.indices():
        #     topic = target._topics.get_item(index)
        #     assert topic.is_fresh()

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
